from copy import deepcopy
from typing import Any
from uuid import uuid4
from app.model.situation import Situation
from app.model.state import State
from app.model.transition import Transition
from app.service.machine_service import create_machine, next_situations, run_machine


def test_create_machine_valid():
    # ARRANGE.
    transition_dicts = [
        {
            "name": "f-transition",
            "pattern": "f",
            "state1_name": "start",
            "state2_name": "f-state",
        },
        {
            "name": "oo-transition",
            "pattern": "oo",
            "state1_name": "f-state",
            "state2_name": "oo-state",
        },
        {
            "name": "end1-transition",
            "pattern": "",
            "state1_name": "oo-state",
            "state2_name": "end",
        },
        {
            "name": "b-transition",
            "pattern": "b",
            "state1_name": "oo-state",
            "state2_name": "b-state",
        },
        {
            "name": "a-transition",
            "pattern": "a",
            "state1_name": "b-state",
            "state2_name": "a-state",
        },
        {
            "name": "r-transition",
            "pattern": "r",
            "state1_name": "a-state",
            "state2_name": "r-state",
        },
        {
            "name": "end2-transition",
            "pattern": "",
            "state1_name": "r-state",
            "state2_name": "end",
        },
    ]
    transitions = [Transition(**t) for t in transition_dicts]

    states = {
        "start": State(**{
            "name": "start",
            "start": True,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "f-state": State(**{
            "name": "f-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "oo-state": State(**{
            "name": "oo-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a-state": State(**{
            "name": "a-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
            "start": False,
            "end": True,
            "data": None,
            "transform": None,
            "event": None
        }),
    }

    # ACT.
    machine = create_machine(transitions, states)

    assert machine
    assert "oo-state" in machine.graph.keys()


def test_next_situations():
    transition_dicts = [
        {
            "name": "f-transition",
            "pattern": "f",
            "state1_name": "start",
            "state2_name": "f-state",
        },
        {
            "name": "oo-transition",
            "pattern": "oo",
            "state1_name": "f-state",
            "state2_name": "oo-state",
        },
        {
            "name": "end1-transition",
            "pattern": "",
            "state1_name": "oo-state",
            "state2_name": "end",
        },
        {
            "name": "b-transition",
            "pattern": "b",
            "state1_name": "oo-state",
            "state2_name": "b-state",
        },
        {
            "name": "a-transition",
            "pattern": "a",
            "state1_name": "b-state",
            "state2_name": "a-state",
        },
        {
            "name": "r-transition",
            "pattern": "r",
            "state1_name": "a-state",
            "state2_name": "r-state",
        },
        {
            "name": "end2-transition",
            "pattern": "",
            "state1_name": "r-state",
            "state2_name": "end",
        },
    ]
    transitions = [Transition(**t) for t in transition_dicts]

    states = {
        "start": State(**{
            "name": "start",
            "start": True,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "f-state": State(**{
            "name": "f-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "oo-state": State(**{
            "name": "oo-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a-state": State(**{
            "name": "a-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
            "start": False,
            "end": True,
            "data": None,
            "transform": None,
            "event": None
        }),
    }
    machine = create_machine(transitions, states)

    initial_situation = Situation(**{
        "id": str(uuid4()),
        "input_complete": "foobar",
        "input_remainder": "foobar",
        "matched": "",
        "state": states["start"],
        "machine": machine,
        "history": [],
    })

    # ACT / ASSERT.
    situations = next_situations(initial_situation)
    assert situations
    assert len(situations) == 1
    assert situations[0].state.name == "f-state"

    # ACT / ASSERT.
    more_situations = next_situations(situations[0])
    assert more_situations
    assert len(more_situations) == 1
    assert more_situations[0].state.name == "oo-state"


def test_next_situations_regex():
    transition_dicts = [
        {
            "name": "f-transition",
            "pattern": "^f",
            "state1_name": "start",
            "state2_name": "^f-state",
        },
        {
            "name": "oo-transition",
            "pattern": "o+",
            "state1_name": "^f-state",
            "state2_name": "o+-state",
        },
        {
            "name": "end1-transition",
            "pattern": "",
            "state1_name": "o+-state",
            "state2_name": "end",
        },
        {
            "name": "b-transition",
            "pattern": "b",
            "state1_name": "o+-state",
            "state2_name": "b-state",
        },
        {
            "name": "a-transition",
            "pattern": "a+",
            "state1_name": "b-state",
            "state2_name": "a+-state",
        },
        {
            "name": "r-transition",
            "pattern": "r",
            "state1_name": "a+-state",
            "state2_name": "r-state",
        },
        {
            "name": "end2-transition",
            "pattern": "",
            "state1_name": "r-state",
            "state2_name": "end",
        },
    ]
    transitions = [Transition(**t) for t in transition_dicts]

    states = {
        "start": State(**{
            "name": "start",
            "start": True,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "^f-state": State(**{
            "name": "^f-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "o+-state": State(**{
            "name": "o+-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a+-state": State(**{
            "name": "a+-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "start": False,
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
            "start": False,
            "end": True,
            "data": None,
            "transform": None,
            "event": None
        }),
    }
    machine = create_machine(transitions, states)

    initial_situation = Situation(**{
        "id": str(uuid4()),
        "input_complete": "foobar",
        "input_remainder": "foobar",
        "matched": "",
        "state": states["start"],
        "machine": machine,
        "history": [],
    })

    # ACT / ASSERT.
    situations = next_situations(initial_situation)
    assert situations
    assert len(situations) == 1
    assert situations[0].state.name == "^f-state"

    # ACT / ASSERT.
    more_situations = next_situations(situations[0])
    assert more_situations
    assert len(more_situations) == 1
    assert more_situations[0].state.name == "o+-state"


def test_run_machine():
    def _transform(situation: Situation, transition: Transition) -> Any:
        data = deepcopy(situation.state.data)
        if situation.matched in ["f", "b", "r"]:
            data = data + "C"
        elif situation.matched in ["a", "e", "i", "o", "u"]:
            data = data + "V"
        elif situation.matched in ["aa", "ee", "ii", "oo", "uu"]:
            data = data + "VV"
        else:
            data = data + situation.matched
        return data


    transition_dicts = [
        {
            "name": "f-transition",
            "pattern": "^f",
            "state1_name": "start",
            "state2_name": "^f-state",
            "transform": _transform,
        },
        {
            "name": "oo-transition",
            "pattern": "o+",
            "state1_name": "^f-state",
            "state2_name": "o+-state",
            "transform": _transform,
        },
        {
            "name": "end1-transition",
            "pattern": "",
            "state1_name": "o+-state",
            "state2_name": "end",
            "transform": _transform,
        },
        {
            "name": "b-transition",
            "pattern": "b",
            "state1_name": "o+-state",
            "state2_name": "b-state",
            "transform": _transform,
        },
        {
            "name": "a-transition",
            "pattern": "a+",
            "state1_name": "b-state",
            "state2_name": "a+-state",
            "transform": _transform,
        },
        {
            "name": "r-transition",
            "pattern": "r",
            "state1_name": "a+-state",
            "state2_name": "r-state",
            "transform": _transform,
        },
        {
            "name": "end2-transition",
            "pattern": "",
            "state1_name": "r-state",
            "state2_name": "end",
            "transform": _transform,
        },
    ]
    transitions = [Transition(**t) for t in transition_dicts]

    states = {
        "start": State(**{
            "name": "start",
            "start": True,
            "end": False,
            "data": "",
            "transform": None,
            "event": None
        }),
        "^f-state": State(**{
            "name": "^f-state",
            "start": False,
            "end": False,
            "transform": None,
            "event": None
        }),
        "o+-state": State(**{
            "name": "o+-state",
            "start": False,
            "end": False,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "start": False,
            "end": False,
            "transform": None,
            "event": None
        }),
        "a+-state": State(**{
            "name": "a+-state",
            "start": False,
            "end": False,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "start": False,
            "end": False,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
            "start": False,
            "end": True,
            "transform": None,
            "event": None
        }),
    }
    machine = create_machine(transitions, states)

    start_situation = Situation(**{
        "id": str(uuid4()),
        "input_complete": "foobar",
        "input_remainder": "foobar",
        "matched": "",
        "state": states["start"],
        "machine": machine,
        "history": [],
    })

    end_situations = run_machine(machine, start_situation)

    assert end_situations
    assert len(end_situations) == 1
    final_situation = end_situations[0]
    assert final_situation.state.name == "end"
    assert len(final_situation.history) == 7
    assert final_situation.history[1].state.name == "^f-state"
    assert final_situation.history[2].state.name == "o+-state"
    assert final_situation.history[4].state.name == "a+-state"
    assert final_situation.history[5].state.name == "r-state"
    assert final_situation.history[6].state.name == "end"

    assert final_situation.state.data == "CVVCVC"

