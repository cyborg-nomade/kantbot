"""External, scripted strip world and an anonymous patch sensor.

World marker identity belongs to the experimenter, never to reception. This
module produces observations, not intuitions, objects, or cognitive outcomes.
"""

from itertools import pairwise
from typing import Annotated, Literal, Self

from pydantic import Field, model_validator

from kantbot.model import (
    ContentField,
    EvaluatorReference,
    Observation,
    ObservationQuality,
    SemanticModel,
)
from kantbot.model.common import Identifier, NonEmptyText, require_unique

STRIP_SENSOR: Literal["strip-patch-camera-v1"] = "strip-patch-camera-v1"


class MarkerState(SemanticModel):
    """An experimenter's marker at one moment, not a cognitive object."""

    marker_id: Identifier
    color: NonEmptyText
    x: int


class StripFrame(SemanticModel):
    """One scripted moment; unreadability hides all its marker content."""

    position: Annotated[int, Field(ge=0)]
    markers: tuple[MarkerState, ...] = ()
    readable: bool = True

    @model_validator(mode="after")
    def marker_identities_are_unique(self) -> Self:
        require_unique(tuple(marker.marker_id for marker in self.markers), "marker IDs")
        return self


class StripWorld(SemanticModel):
    """A finite world script, including evaluator-only identity across time.

    Snapshots specify what happens; there is no inferred physics or stochastic
    generator. Cognitive callers receive only ``observe_world(self)``.
    """

    format_version: Literal[1] = 1
    episode_id: Identifier
    frames: tuple[StripFrame, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def frames_are_strictly_ordered(self) -> Self:
        positions = tuple(frame.position for frame in self.frames)
        if any(earlier >= later for earlier, later in pairwise(positions)):
            raise ValueError("world frames must have strictly increasing positions")
        return self

    def evaluator_references(self) -> tuple[EvaluatorReference, ...]:
        """Export hidden identities separately, in an evaluator-only namespace."""

        marker_ids = sorted(
            {marker.marker_id for frame in self.frames for marker in frame.markers}
        )
        return tuple(
            EvaluatorReference(
                evaluator_reference_id=f"strip-evaluator:{self.episode_id}:{marker_id}",
                description=f"External strip-world marker {marker_id}; not a ground",
            )
            for marker_id in marker_ids
        )


class ObservationSequence(SemanticModel):
    """Versioned sensor export with no world state or interpretation policy.

    Positions may repeat for simultaneous samples. Their order is preserved,
    never repaired by sorting during parsing.
    """

    format_version: Literal[1] = 1
    episode_id: Identifier
    source: Literal["strip-patch-camera-v1"] = STRIP_SENSOR
    observations: tuple[Observation, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def observations_share_the_boundary(self) -> Self:
        require_unique(
            tuple(item.observation_id for item in self.observations), "observation IDs"
        )
        for item in self.observations:
            if item.episode_id != self.episode_id or item.source != self.source:
                raise ValueError(
                    "observations must share the sequence episode and sensor"
                )
        positions = tuple(item.position for item in self.observations)
        if any(earlier > later for earlier, later in pairwise(positions)):
            raise ValueError("observations must preserve nondecreasing positions")
        return self


def _observation(
    episode_id: str,
    frame: StripFrame,
    slot: int,
    content: tuple[ContentField, ...],
) -> Observation:
    quality = ObservationQuality.COMPLETE
    quality_notes = None
    if not frame.readable:
        quality = ObservationQuality.IMPAIRED
        quality_notes = "The frame is unreadable; no patch content is supplied."
    return Observation(
        observation_id=f"strip-observation:{episode_id}:{frame.position}:{slot}",
        episode_id=episode_id,
        position=frame.position,
        source=STRIP_SENSOR,
        content=content,
        quality=quality,
        quality_notes=quality_notes,
    )


def _observe_frame(episode_id: str, frame: StripFrame) -> tuple[Observation, ...]:
    if not frame.readable:
        return (
            _observation(
                episode_id,
                frame,
                0,
                (ContentField(name="frame-readable", value=False),),
            ),
        )

    # Only visible coordinates and colors determine ordering and multiplicity.
    # Coincident same-color markers are one indistinguishable sensor patch.
    patches = sorted({(marker.x, marker.color) for marker in frame.markers})
    if not patches:
        return (
            _observation(
                episode_id, frame, 0, (ContentField(name="patch-present", value=False),)
            ),
        )
    return tuple(
        _observation(
            episode_id,
            frame,
            slot,
            (ContentField(name="color", value=color), ContentField(name="x", value=x)),
        )
        for slot, (x, color) in enumerate(patches)
    )


def observe_world(world: StripWorld) -> ObservationSequence:
    """Replay anonymous observations without exposing identity or future state.

    The returned sequence is a complete episode for an external replay driver.
    Each individual sample depends only on its frame and the public episode ID.
    """

    return ObservationSequence(
        episode_id=world.episode_id,
        observations=tuple(
            observation
            for frame in world.frames
            for observation in _observe_frame(world.episode_id, frame)
        ),
    )
