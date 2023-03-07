import re
from collections import deque
from copy import deepcopy
from typing import Dict, List
from uuid import uuid4
from app.model.machine import Machine
from app.model.situation import Situation
from app.model.state import State
from app.model.transition import Transition


def _transitions_of_state(machine: Machine, state_name: str) -> Dict[str, Transition]:
    """
    Gets the set of transitions of a given source state.

    Args:
        machine (Machine): The machine from which to get the set of transitions.
        state_name (str): The name of the state which is the source of the transitions.

    Raises:
        LookupError: Raised if the given state_name cannot be found among the keys of the graph of the machine.

    Returns:
        Dict[str, Transition]: The dict of transitions emerging from the given state.
    """
    if state_name not in machine.graph.keys():
        raise LookupError(f"State name not found in machine graph: '{state_name}'. Available state names: '{machine.graph.keys()}'.")
    return machine.graph[state_name]


def create_machine(transitions: List[Transition], states: Dict[str, State]) -> Machine:
    """
    Creates a new finite-state machine and adds a list of transitions.
    The transition contains both the source and destination states, so the needed states can be added for both source and destination.

    Args:
        transitions (List[Transition]): The list of transitions (including source and destination states) to add to the machine.
        states (Dict[str, State]): The dict of states with their details.

    Returns:
        Machine: The resultant machine with the transitions added.
    """

    # Validate that the transition names are unique among the list of transitions.
    counts = dict()
    invalid = False
    for t in transitions:
        counts[t.name] = counts[t.name]+1 if t.name in counts.keys() else 1
        if counts[t.name] > 1:
            invalid = True
    if invalid:
        reused_transition_names = [name for name in counts.keys() if counts[name] > 1]
        raise Exception(f"Invalid list of transitions: reused transition name: '{reused_transition_names}'.")

    graph = dict()

    def _add_transition(transition: Transition):
        if transition.state1_name not in graph.keys():
            graph[transition.state1_name] = dict()
        graph[transition.state1_name][transition.name] = transition

        if transition.state2_name not in graph.keys():
            graph[transition.state2_name] = dict()

    for transition in transitions:
        _add_transition(transition)

    # TODO: Validate the state names with the graph.

    machine = Machine(graph=graph, states=states)
    
    return machine


def next_situations(situation: Situation) -> List[Situation]:
    """
    Gets the list of reachable situations given the provided situation.
    Cases where the input_remainder is empty (we're done), but the pattern is non-empty are omitted,
    ruling out the failed analyses (impossible trails).

    Args:
        situation (Situation): The given situation that is the starting point for movement.

    Returns:
        List[Situation]: The situations that derive from the provided situation.
    """
    # These are the transitions flowing out of the state given by the provided situation.
    # So, no need to filter transitions by transition.state1_name==situation.state_name.
    transitions = _transitions_of_state(situation.machine, situation.state.name)
    # situation: input, state (==state1)
    # transition: state1, pattern -> state2
    situations = []
    for transition in transitions.values():
        # Omit new situations that involves non-empty pattern, but empty input_remainder.
        # That means we ran out of input, at least for this transition.
        if situation.input_remainder == "" and transition.pattern != "":
            continue

        # Does the input match with the transition's pattern? Then take this transition.
        # TODO: Does this handle when pattern is empty? It should. Seems to.
        match = re.match(transition.pattern, situation.input_remainder)
        if match:
            match_length = len(match.group(0))
            new_remainder = situation.input_remainder[match_length:] if match_length < len(situation.input_remainder) else ""  # Deepcopy??
            new_state = deepcopy(situation.machine.states[transition.state2_name]) # The situation needs its own instance copy of the state, since states may be revisited.

            new_machine = deepcopy(situation.machine)

            # Execute a transformation specified on the transition. transform(prev situation, next situation, transition) => data structure of your choice (but consistent), saved in state.
            # prev situation: situation (function arg). next situation: new_situation (below).
            # transform can use the states, or the given transition (the one actually taken), or the history of the situations, or anything, to produce a new/updated data structure.
            # It can then save that new data structure in the new state, in the state collection.
            # TODO: BUT the trail could revisit the state!! So, no, we cannot use the state dict as the collection of state "instances", i.e., state visits. Each situation has a state instance. ***

            # if transition.transform:
            #     transform = transition.transform

            new_history = deepcopy(situation.history)
            if new_history:
                new_history.append(situation)
            else:
                new_history = [situation]

            new_situation_dict = {
                "id": str(uuid4()),
                "input_complete": situation.input_complete,
                "input_remainder": new_remainder,
                "state": new_state,
                "machine": new_machine,
                "history": new_history,
            }
            new_situation = Situation(**new_situation_dict)
            situations.append(new_situation)
    
    return situations


def situation_is_end(situation: Situation, machine: Machine):
    state = machine.states[situation.state.name]
    no_more_input = situation.input_remainder == ""
    return state.end and no_more_input


def run_machine(machine: Machine, start_situation: Situation) -> List[Situation]:
    """
    Run the provided machine on the specified starting situation
    and generate the list of ending state names.

    Args:
        machine (Machine): The machine that will process the situations.
        start_situation (Situation): The starting situation.

    Returns:
        List[Situation]: The list of situations stopped at an end state.
    """
    end_situations = []
    
    situation_queue = deque()
    situation_queue.append(start_situation)

    while len(situation_queue) > 0:
        situation = situation_queue.popleft()

        if situation_is_end(situation, machine):
            situation.history.append(situation)
            end_situations.append(situation)

        else:
            new_situations = next_situations(situation)
            situation_queue.extend(new_situations)
    
    return end_situations
