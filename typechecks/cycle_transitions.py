"""Static witness that a successful cycle composes only through legal stages."""

from typing import NamedTuple

from kantbot.interfaces import RoleContext
from kantbot.model import (
    ApplicationResult,
    CandidateRepresentation,
    CommittedJudgment,
    Intuition,
    JudgmentCommitted,
    ManifoldOfIntuition,
    ObjectCandidate,
    Observation,
    PresentedElement,
    ProposedJudgment,
    RetainedSequence,
    UnityCheck,
)
from kantbot.model.common import Identifier
from kantbot.transitions import (
    CandidateRecognized,
    CommitmentCompleted,
    ConceptApplied,
    CycleTerminated,
    JudgmentProposed,
    ManifoldFormed,
    ObjectConstituted,
    ProjectionCompleted,
    ReceptionCompleted,
    RetentionCompleted,
    UnityAccepted,
    open_cycle,
    record_application,
    record_commitment,
    record_critique,
    record_manifold,
    record_object_formation,
    record_projection,
    record_reception,
    record_recognition,
    record_retention,
    record_unity,
    resolve_application,
)


class SuccessfulPathValues(NamedTuple):
    cycle_id: Identifier
    context: RoleContext
    observations: tuple[Observation, ...]
    presented_elements: tuple[PresentedElement, ...]
    intuitions: tuple[Intuition, ...]
    manifold: ManifoldOfIntuition
    retained_sequence: RetainedSequence
    candidate: CandidateRepresentation
    object_candidate: ObjectCandidate
    application: ApplicationResult
    proposal: ProposedJudgment
    unity_check: UnityCheck
    judgment: CommittedJudgment
    outcome: JudgmentCommitted


def compose_successful_path(values: SuccessfulPathValues) -> CycleTerminated:
    """Demonstrate stage narrowing for adapters that orchestrate the roles."""

    opened = open_cycle(values.cycle_id, values.observations, values.context)
    presented: ReceptionCompleted = record_reception(opened, values.presented_elements)

    projection_result = record_projection(presented, values.intuitions)
    assert isinstance(projection_result, ProjectionCompleted)
    projected: ProjectionCompleted = projection_result

    formed: ManifoldFormed = record_manifold(projected, values.manifold)
    retention_result = record_retention(formed, values.retained_sequence)
    assert isinstance(retention_result, RetentionCompleted)
    retained: RetentionCompleted = retention_result

    recognition_result = record_recognition(retained, (values.candidate,))
    assert isinstance(recognition_result, tuple)
    recognized: CandidateRecognized = recognition_result[0]

    object_result = record_object_formation(recognized, values.object_candidate)
    assert isinstance(object_result, ObjectConstituted)
    constituted: ObjectConstituted = object_result

    applied: ConceptApplied = record_application(constituted, values.application)
    proposal_result = resolve_application(applied, values.proposal)
    assert isinstance(proposal_result, JudgmentProposed)
    proposed: JudgmentProposed = proposal_result

    unity_result = record_unity(proposed, values.unity_check)
    assert isinstance(unity_result, UnityAccepted)
    united: UnityAccepted = unity_result

    commitment_result = record_commitment(united, values.judgment)
    assert isinstance(commitment_result, CommitmentCompleted)
    committed: CommitmentCompleted = commitment_result
    return record_critique(committed, values.outcome)
