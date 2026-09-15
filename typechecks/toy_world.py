"""The toy-world export fits reception without a world-state capability."""

from kantbot.interfaces import ReceptionRequest, RoleContext
from kantbot.model import Observation
from kantbot.worlds import ObservationSequence, StripWorld, observe_world


def sensor_input(world: StripWorld) -> tuple[Observation, ...]:
    return observe_world(world).observations


def reception_inputs(
    sequence: ObservationSequence, context: RoleContext
) -> tuple[ReceptionRequest, ...]:
    return tuple(
        ReceptionRequest(observation=item, context=context)
        for item in sequence.observations
    )
