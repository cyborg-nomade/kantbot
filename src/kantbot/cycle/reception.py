"""Reception and variant projection, before any candidate identity is assigned."""

from kantbot.cycle._support import derive, ground, outcome_context
from kantbot.interfaces import (
    ManifoldRequest,
    ProjectionRequest,
    ProjectionResult,
    ReceptionRequest,
)
from kantbot.model import (
    GroundKind,
    Intuition,
    ManifoldOfIntuition,
    NotPresentable,
    OutcomeKind,
    PresentedElement,
)
from kantbot.procedures import project_content


def present_observation(request: ReceptionRequest, /) -> PresentedElement:
    """Preserve every supplied field and its observation identity."""

    observation = request.observation
    return PresentedElement(
        presented_element_id=f"presented:{observation.observation_id}",
        observation_id=observation.observation_id,
        episode_id=observation.episode_id,
        position=observation.position,
        source=observation.source,
        content=observation.content,
        derivation=derive(
            request.context,
            "shared reception",
            (ground(observation.observation_id, GroundKind.OBSERVATION),),
        ),
    )


def project_intuition(request: ProjectionRequest, /) -> ProjectionResult:
    """Apply the declared projection, preserving a typed refusal on failure."""

    presented = request.presented_element
    projection = request.projection
    grounds = (
        ground(presented.presented_element_id, GroundKind.PRESENTED_ELEMENT),
        ground(projection.projection_id, GroundKind.VARIANT_PROJECTION),
    )
    unavailable = tuple(
        form.form_id
        for form in projection.required_forms
        if request.available_form_ids is not None
        and form.form_id not in request.available_form_ids
    )
    try:
        if unavailable:
            raise ValueError("required forms are unavailable for this episode")
        content = project_content(presented, projection)
    except ValueError:
        supplied_names = {item.name for item in presented.content}
        missing = tuple(
            f"projection-form:{form_id}" for form_id in unavailable
        ) + tuple(
            f"projection-field:{name}"
            for name in projection.procedure.fields
            if name not in supplied_names
        ) or ("projection-receptive-conditions",)
        label = f"projection-refusal:{presented.presented_element_id}"
        return NotPresentable(
            outcome_id=f"outcome:{label}",
            presented_element_ids=(presented.presented_element_id,),
            failed_condition_ids=missing,
            context=outcome_context(
                request.context,
                OutcomeKind.NOT_PRESENTABLE,
                label,
                grounds,
                missing=missing,
            ),
        )
    return Intuition(
        intuition_id=f"intuition:{projection.projection_id}:{presented.presented_element_id}",
        presented_element_id=presented.presented_element_id,
        projection_id=projection.projection_id,
        episode_id=presented.episode_id,
        position=presented.position,
        content=content,
        form_ids=tuple(form.form_id for form in projection.required_forms),
        derivation=derive(
            request.context, "project supplied content under form", grounds
        ),
    )


def form_manifold(request: ManifoldRequest, /) -> ManifoldOfIntuition:
    """Make the complete ordered plurality available without synthesizing identity."""

    positions = tuple(item.position for item in request.intuitions)
    if positions != tuple(sorted(positions)):
        raise ValueError("manifold input must already be temporally ordered")
    forms = request.intuitions[0].form_ids
    if any(item.form_ids != forms for item in request.intuitions):
        raise ValueError("manifold intuitions must share declared forms")
    return ManifoldOfIntuition(
        manifold_id=f"manifold:{request.context.scope.episode_id}",
        episode_id=request.context.scope.episode_id,
        intuition_ids=tuple(item.intuition_id for item in request.intuitions),
        form_ids=forms,
        derivation=derive(
            request.context,
            "formed plurality before synthesis",
            tuple(
                ground(item.intuition_id, GroundKind.INTUITION)
                for item in request.intuitions
            ),
        ),
    )
