from uuid import uuid4
from app.model.situation import Situation
from app.model.state import State
from app.model.transition import Transition
from app.service.machine_service import create_machine, next_situations, run_machine


def test_create_machine():
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
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "f-state": State(**{
            "name": "f-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "oo-state": State(**{
            "name": "oo-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a-state": State(**{
            "name": "a-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
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
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "f-state": State(**{
            "name": "f-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "oo-state": State(**{
            "name": "oo-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a-state": State(**{
            "name": "a-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
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
        "state_name": "start",
        "machine": machine,
    })

    # ACT / ASSERT.
    situations = next_situations(initial_situation)
    assert situations
    assert len(situations) == 1
    assert situations[0].state_name == "f-state"

    # ACT / ASSERT.
    more_situations = next_situations(situations[0])
    assert more_situations
    assert len(more_situations) == 1
    assert more_situations[0].state_name == "oo-state"


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
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "f-state": State(**{
            "name": "^f-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "oo-state": State(**{
            "name": "o+-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a-state": State(**{
            "name": "a+-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
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
        "state_name": "start",
        "machine": machine,
    })

    # ACT / ASSERT.
    situations = next_situations(initial_situation)
    assert situations
    assert len(situations) == 1
    assert situations[0].state_name == "^f-state"

    # ACT / ASSERT.
    more_situations = next_situations(situations[0])
    assert more_situations
    assert len(more_situations) == 1
    assert more_situations[0].state_name == "o+-state"


def test_run_machine():
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
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "^f-state": State(**{
            "name": "^f-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "o+-state": State(**{
            "name": "o+-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "b-state": State(**{
            "name": "b-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "a+-state": State(**{
            "name": "a+-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "r-state": State(**{
            "name": "r-state",
            "end": False,
            "data": None,
            "transform": None,
            "event": None
        }),
        "end": State(**{
            "name": "end",
            "end": True,
            "data": None,
            "transform": None,
            "event": None
        }),
    }
    machine = create_machine(transitions, states)

    start_situation = Situation(**{
        "id": str(uuid4()),
        "input_complete": "foobar",
        "input_remainder": "foobar",
        "state_name": "start",
        "machine": machine,
    })

    end_situations = run_machine(machine, start_situation)

    assert end_situations
    assert len(end_situations) == 1

