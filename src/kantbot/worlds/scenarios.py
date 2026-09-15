"""Named world scripts: sensor inputs, not precomputed cognitive answers."""

from kantbot.worlds.strip import MarkerState, StripFrame, StripWorld

SCENARIO_NAMES = (
    "rightward",
    "stationary",
    "reordered-motion",
    "ambiguous-middle",
    "short-interval",
    "unreadable-middle",
    "broken-color",
    "empty-middle",
)


def _marker(x: int, color: str = "amber", marker_id: str = "target-17") -> MarkerState:
    return MarkerState(marker_id=marker_id, color=color, x=x)


def _single_marker_frames(xs: tuple[int, ...]) -> tuple[StripFrame, ...]:
    return tuple(
        StripFrame(position=position, markers=(_marker(x),))
        for position, x in enumerate(xs)
    )


def load_scenario(name: str) -> StripWorld:
    """Build a fresh immutable script; names never become judgment labels.

    Every built-in shares the public episode ID ``strip-demo`` so controlled
    contrasts can preserve observation identity while changing supplied content.
    An experiment that combines episodes must assign distinct episode IDs.
    """

    match name:
        case "rightward":
            frames = _single_marker_frames((0, 1, 2))
        case "stationary":
            frames = _single_marker_frames((2, 2, 2))
        case "reordered-motion":
            frames = _single_marker_frames((0, 2, 1))
        case "ambiguous-middle":
            frames = (
                StripFrame(position=0, markers=(_marker(0),)),
                StripFrame(
                    position=1, markers=(_marker(1), _marker(2, marker_id="rival"))
                ),
                StripFrame(position=2, markers=(_marker(3),)),
            )
        case "short-interval":
            frames = _single_marker_frames((0, 1))
        case "unreadable-middle":
            frames = (
                StripFrame(position=0, markers=(_marker(0),)),
                StripFrame(position=1, markers=(_marker(1),), readable=False),
                StripFrame(position=2, markers=(_marker(2),)),
            )
        case "broken-color":
            frames = (
                StripFrame(position=0, markers=(_marker(0),)),
                StripFrame(position=1, markers=(_marker(1, color="blue"),)),
                StripFrame(position=2, markers=(_marker(2),)),
            )
        case "empty-middle":
            frames = (
                StripFrame(position=0, markers=(_marker(0),)),
                StripFrame(position=1),
                StripFrame(position=2, markers=(_marker(2),)),
            )
        case _:
            raise ValueError(f"unknown strip scenario: {name!r}")
    return StripWorld(episode_id="strip-demo", frames=frames)
