"""Multi-sample licenses: temporal content must matter before and after objecthood."""

import pytest

from kantbot.model import (
    ApplicationStatus,
    CognitiveGround,
    ConditionStatus,
    ContentField,
    FieldConstant,
    GroundKind,
    RetainedIntuition,
    RetentionStatus,
    SemanticModel,
    SensibleProcedure,
    StrictIncrease,
)
from kantbot.provenance import InvalidProvenance, ProvenanceGraph, ProvenanceTrace


def _change[T: SemanticModel](value: T, **updates: object) -> T:
    return type(value).model_validate({**value.model_dump(mode="python"), **updates})


def _ground(entity_id: str, kind: GroundKind) -> CognitiveGround:
    return CognitiveGround(ground_id=entity_id, kind=kind)


def _motion_trace(trace: ProvenanceTrace, xs: tuple[int, ...]) -> ProvenanceTrace:
    """Hand-author structural records and a separate arithmetic expectation."""

    observations = tuple(
        _change(
            trace.observations[0],
            observation_id=f"obs-{index}",
            position=index,
            content=(
                ContentField(name="color", value="amber"),
                ContentField(name="x", value=x),
            ),
        )
        for index, x in enumerate(xs)
    )
    presentations = tuple(
        _change(
            trace.presented_elements[0],
            presented_element_id=f"pe-{index}",
            observation_id=observation.observation_id,
            position=index,
            content=observation.content,
            derivation=_change(
                trace.presented_elements[0].derivation,
                grounds=(_ground(observation.observation_id, GroundKind.OBSERVATION),),
            ),
        )
        for index, observation in enumerate(observations)
    )
    intuitions = tuple(
        _change(
            trace.intuitions[0],
            intuition_id=f"intuition-{index}",
            presented_element_id=presented.presented_element_id,
            position=index,
            content=presented.content,
            derivation=_change(
                trace.intuitions[0].derivation,
                grounds=(
                    _ground(
                        presented.presented_element_id, GroundKind.PRESENTED_ELEMENT
                    ),
                    _ground(
                        trace.projections[0].projection_id,
                        GroundKind.VARIANT_PROJECTION,
                    ),
                ),
            ),
        )
        for index, presented in enumerate(presentations)
    )
    ids = tuple(item.intuition_id for item in intuitions)
    evidence = tuple(_ground(item, GroundKind.INTUITION) for item in ids)
    manifold = _change(
        trace.manifolds[0],
        intuition_ids=ids,
        derivation=_change(trace.manifolds[0].derivation, grounds=evidence),
    )
    retained = _change(
        trace.retained_sequences[0],
        items=tuple(
            RetainedIntuition(intuition_id=item, status=RetentionStatus.CURRENT)
            for item in ids
        ),
    )
    candidate = _change(trace.candidates[0], intuition_ids=ids)
    identity_rule = _change(
        trace.rules[0],
        description="preserve supplied color across at least two samples",
        sensible_procedure=SensibleProcedure(
            temporal_form_id="time-total",
            checks=(FieldConstant(condition_id="identity-passes", field="color"),),
        ),
    )
    obj = trace.object_candidates[0]
    obj = _change(
        obj,
        identity_results=(_change(obj.identity_results[0], evidence=evidence),),
        constitutive_results=(_change(obj.constitutive_results[0], evidence=evidence),),
    )
    condition = _change(
        trace.concepts[0].applicability_conditions[0],
        condition_id="positive-change",
        description="x increases at every successive sample",
    )
    concept = _change(
        trace.concepts[0],
        concept_id="moving-right",
        name="moving right",
        applicability_conditions=(condition,),
        inferential_consequences=(),
    )
    schema = _change(
        trace.schemas[0],
        schema_id="S-right",
        concept_id=concept.concept_id,
        name="successive positive changes",
        procedure=SensibleProcedure(
            temporal_form_id="time-total",
            checks=(StrictIncrease(condition_id=condition.condition_id, field="x"),),
        ),
        condition_ids=(condition.condition_id,),
    )
    condition_status = ConditionStatus.SATISFIED
    application_status = ApplicationStatus.APPLICABLE
    if any(xs[index] >= xs[index + 1] for index in range(len(xs) - 1)):
        condition_status = ConditionStatus.FAILED
        application_status = ApplicationStatus.NOT_APPLICABLE
    application = trace.applications[0]
    application = _change(
        application,
        concept_id=concept.concept_id,
        schema_id=schema.schema_id,
        status=application_status,
        condition_results=(
            _change(
                application.condition_results[0],
                condition_id=condition.condition_id,
                status=condition_status,
                evidence=evidence,
            ),
        ),
        derivation=_change(
            application.derivation,
            grounds=(
                _ground(obj.object_candidate_id, GroundKind.OBJECT_CANDIDATE),
                _ground(concept.concept_id, GroundKind.CONCEPT),
                _ground(schema.schema_id, GroundKind.SCHEMA),
            ),
        ),
    )
    return _change(
        trace,
        observations=observations,
        presented_elements=presentations,
        intuitions=intuitions,
        manifolds=(manifold,),
        retained_sequences=(retained,),
        candidates=(candidate,),
        rules=(identity_rule, trace.rules[1]),
        object_candidates=(obj,),
        concepts=(concept,),
        schemas=(schema,),
        applications=(application,),
        proposals=(),
        unity_checks=(),
        judgments=(),
        limit_reports=(),
        outcomes=(),
    )


def test_bp001_reordered_content_changes_application_without_destroying_object(
    complete_trace: ProvenanceTrace,
) -> None:
    increasing = _motion_trace(complete_trace, (0, 1, 2))
    reordered = _motion_trace(complete_trace, (0, 2, 1))
    assert ProvenanceGraph(increasing).trace.applications[0].applicable
    assert not ProvenanceGraph(reordered).trace.applications[0].applicable
    assert increasing.object_candidates == reordered.object_candidates
    application = reordered.applications[0]
    fabricated = _change(
        application,
        status=ApplicationStatus.APPLICABLE,
        condition_results=(
            _change(application.condition_results[0], status=ConditionStatus.SATISFIED),
        ),
    )
    with pytest.raises(InvalidProvenance, match="procedure replay"):
        ProvenanceGraph(_change(reordered, applications=(fabricated,)))


def test_temporal_identity_failure_blocks_objecthood_before_empirical_application(
    complete_trace: ProvenanceTrace,
) -> None:
    trace = _motion_trace(complete_trace, (0, 1, 2))
    content = (
        ContentField(name="color", value="blue"),
        ContentField(name="x", value=1),
    )
    observations = (
        trace.observations[0],
        _change(trace.observations[1], content=content),
        trace.observations[2],
    )
    presented = (
        trace.presented_elements[0],
        _change(trace.presented_elements[1], content=content),
        trace.presented_elements[2],
    )
    intuitions = (
        trace.intuitions[0],
        _change(trace.intuitions[1], content=content),
        trace.intuitions[2],
    )
    trace = _change(
        trace,
        observations=observations,
        presented_elements=presented,
        intuitions=intuitions,
        applications=(),
    )
    with pytest.raises(InvalidProvenance, match="procedure replay"):
        ProvenanceGraph(trace)
    # The failed object license does not invalidate the sensible candidate itself.
    ProvenanceGraph(_change(trace, object_candidates=()))


@pytest.mark.parametrize("stage", ["manifold", "retention", "candidate"])
def test_graph_does_not_silently_reorder_a_sensible_sequence(
    complete_trace: ProvenanceTrace, stage: str
) -> None:
    trace = _motion_trace(complete_trace, (0, 1, 2))
    if stage == "manifold":
        manifold = trace.manifolds[0]
        trace = _change(
            trace,
            manifolds=(
                _change(
                    manifold, intuition_ids=tuple(reversed(manifold.intuition_ids))
                ),
            ),
        )
    elif stage == "retention":
        retained = trace.retained_sequences[0]
        trace = _change(
            trace,
            retained_sequences=(
                _change(retained, items=tuple(reversed(retained.items))),
            ),
        )
    else:
        candidate = trace.candidates[0]
        trace = _change(
            trace,
            candidates=(
                _change(
                    candidate, intuition_ids=tuple(reversed(candidate.intuition_ids))
                ),
            ),
        )
    with pytest.raises(InvalidProvenance, match="order"):
        ProvenanceGraph(trace)
