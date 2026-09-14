"""Print a deterministic sensor episode, with no hidden evaluator payload."""

import argparse

from kantbot.worlds import SCENARIO_NAMES, load_scenario, observe_world


def main() -> None:
    """Export observation JSON or list the available world scripts."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scenario", choices=SCENARIO_NAMES, nargs="?", default="rightward"
    )
    parser.add_argument("--list", action="store_true", help="list available scenarios")
    args = parser.parse_args()
    if args.list:
        print("\n".join(SCENARIO_NAMES))
        return
    print(observe_world(load_scenario(args.scenario)).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
