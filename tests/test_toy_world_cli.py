"""Small observation-export CLI: stable output and no cognitive claims."""

import os
import subprocess
import sys

import pytest

from kantbot.worlds import (
    SCENARIO_NAMES,
    ObservationSequence,
    load_scenario,
    observe_world,
)
from kantbot.worlds.__main__ import main

INVALID_ARGUMENT_EXIT_CODE = 2


@pytest.mark.parametrize("name", SCENARIO_NAMES)
def test_cli_exports_only_the_selected_observation_sequence(
    name: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["kantbot.worlds", name])
    main()
    output = capsys.readouterr()
    assert not output.err
    assert ObservationSequence.model_validate_json(output.out) == observe_world(
        load_scenario(name)
    )


def test_cli_lists_names(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["kantbot.worlds", "--list"])
    main()
    assert capsys.readouterr().out.splitlines() == list(SCENARIO_NAMES)


def test_cli_rejects_unknown_name(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["kantbot.worlds", "missing"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == INVALID_ARGUMENT_EXIT_CODE
    assert "invalid choice" in capsys.readouterr().err


def test_replay_bytes_are_independent_of_process_hash_seed() -> None:
    outputs = tuple(
        subprocess.run(
            [sys.executable, "-m", "kantbot.worlds", "ambiguous-middle"],
            env={**os.environ, "PYTHONHASHSEED": seed},
            check=True,
            capture_output=True,
        ).stdout
        for seed in ("1", "927")
    )
    assert outputs[0] == outputs[1]
    assert ObservationSequence.model_validate_json(outputs[0]) == observe_world(
        load_scenario("ambiguous-middle")
    )
