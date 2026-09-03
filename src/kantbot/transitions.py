"""Pure, checked transitions for one bounded cognitive-cycle path.

The canonical values describe what each cognitive artifact means.  This module
describes when an artifact may become the next licensed state.  It performs no
cognitive operation itself: callers supply results produced through the role
interfaces, and these functions check their cross-stage fit before returning a
new immutable snapshot.
"""

from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import Field, TypeAdapter, model_validator

from kantbot.interfaces import (
    CommitmentResult,
    ObjectFormationResult,
    ProposalResult,
    RecognitionResult,
    RetentionResult,
    RoleContext,
    UnityResult,
)
from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    ApplicationUnderdetermined,
    CandidateRepresentation,
    CommittedJudgment,
    ConceptNotApplicable,
    ConditionStatus,
    InputError,
    Intuition,
    JudgmentCommitted,
    JudgmentWithheld,
    ManifoldOfIntuition,
    NotPresentable,
    ObjectCandidate,
    Observation,
    OutcomeKind,
    Overreach,
    PresentedElement,
    ProposedJudgment,
    RetainedSequence,
    SemanticModel,
    SynthesisAmbiguous,
    SynthesisFailed,
    TerminalOutcome,
    UnityCheck,
    UnityConflict,
)
from kantbot.model.common import (
    ConfigurationIdentity,
    Derivation,
    GroundKind,
    Identifier,
    Scope,
    require_unique,
)


class InvalidTransition(ValueError):
    """A programming error that attempts to bypass a cognitive boundary.

    Cognitive failures are represented by ``TerminalOutcome`` values.  This
    exception is reserved for incompatible IDs, contexts, or stage results.
    """


class CycleStage(StrEnum):
    """Non-terminal positions whose differences remain inspectable."""

    OPENED = "opened"
    PRESENTED = "presented"
    PROJECTED = "projected"
    MANIFOLD_FORMED = "manifold-formed"
    RETAINED = "retained"
    CANDIDATE_RECOGNIZED = "candidate-recognized"
    OBJECT_CONSTITUTED = "object-constituted"
    CONCEPT_APPLIED = "concept-applied"
    JUDGMENT_PROPOSED = "judgment-proposed"
    UNITY_ACCEPTED = "unity-accepted"
    COMMITMENT_COMPLETED = "commitment-completed"
    TERMINAL = "terminal"


class CycleBoundary(StrEnum):
    """Operation boundary at which a terminal result became strongest."""

    INPUT_VALIDATION = "input-validation"
    VARIANT_PROJECTION = "variant-projection"
    RETENTION = "retention"
    RECOGNITION = "recognition"
    OBJECT_FORMATION = "object-formation"
    APPLICATION = "application"
    PROPOSAL = "proposal"
    UNITY = "unity"
    COMMITMENT = "commitment"
    CRITIQUE = "critique"


def _context_matches(
    context: RoleContext,
    scope: Scope,
    configuration: ConfigurationIdentity,
    label: str,
) -> None:
    if context.scope != scope or context.configuration != configuration:
        raise ValueError(f"{label} must share the cycle context")


def _derivation_matches(
    context: RoleContext, derivation: Derivation, label: str
) -> None:
    _context_matches(context, derivation.scope, derivation.configuration, label)


class _CycleStateBase(SemanticModel):
    cycle_id: Identifier
    stage: CycleStage
    context: RoleContext


class CycleOpened(_CycleStateBase):
    stage: Literal[CycleStage.OPENED] = CycleStage.OPENED
    observations: tuple[Observation, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def observations_belong_to_the_episode(self) -> Self:
        require_unique(
            tuple(item.observation_id for item in self.observations),
            "cycle observation IDs",
        )
        if any(
            item.episode_id != self.context.scope.episode_id
            for item in self.observations
        ):
            raise ValueError("cycle observations must belong to the scoped episode")
        return self


class ReceptionCompleted(_CycleStateBase):
    stage: Literal[CycleStage.PRESENTED] = CycleStage.PRESENTED
    presented_elements: tuple[PresentedElement, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def presentations_share_the_context(self) -> Self:
        require_unique(
            tuple(item.presented_element_id for item in self.presented_elements),
            "presented element IDs",
        )
        for item in self.presented_elements:
            _derivation_matches(self.context, item.derivation, "presented elements")
        return self


class ProjectionCompleted(_CycleStateBase):
    stage: Literal[CycleStage.PROJECTED] = CycleStage.PROJECTED
    intuitions: tuple[Intuition, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def intuitions_share_the_context(self) -> Self:
        require_unique(
            tuple(item.intuition_id for item in self.intuitions), "intuition IDs"
        )
        for item in self.intuitions:
            _derivation_matches(self.context, item.derivation, "intuitions")
        return self


class ManifoldFormed(_CycleStateBase):
    stage: Literal[CycleStage.MANIFOLD_FORMED] = CycleStage.MANIFOLD_FORMED
    manifold: ManifoldOfIntuition

    @model_validator(mode="after")
    def manifold_shares_the_context(self) -> Self:
        _derivation_matches(self.context, self.manifold.derivation, "manifold")
        return self


class RetentionCompleted(_CycleStateBase):
    stage: Literal[CycleStage.RETAINED] = CycleStage.RETAINED
    retained_sequence: RetainedSequence

    @model_validator(mode="after")
    def retention_shares_the_context(self) -> Self:
        _derivation_matches(
            self.context, self.retained_sequence.derivation, "retained sequence"
        )
        return self


class CandidateRecognized(_CycleStateBase):
    stage: Literal[CycleStage.CANDIDATE_RECOGNIZED] = CycleStage.CANDIDATE_RECOGNIZED
    manifold_id: Identifier
    candidate: CandidateRepresentation

    @model_validator(mode="after")
    def candidate_shares_the_context(self) -> Self:
        _derivation_matches(self.context, self.candidate.derivation, "candidate")
        return self


class ObjectConstituted(_CycleStateBase):
    stage: Literal[CycleStage.OBJECT_CONSTITUTED] = CycleStage.OBJECT_CONSTITUTED
    object_candidate: ObjectCandidate

    @model_validator(mode="after")
    def object_shares_the_context(self) -> Self:
        _derivation_matches(
            self.context, self.object_candidate.derivation, "object candidate"
        )
        return self


class ConceptApplied(_CycleStateBase):
    stage: Literal[CycleStage.CONCEPT_APPLIED] = CycleStage.CONCEPT_APPLIED
    application: ApplicationResult

    @model_validator(mode="after")
    def application_shares_the_context(self) -> Self:
        _derivation_matches(self.context, self.application.derivation, "application")
        return self


class JudgmentProposed(_CycleStateBase):
    stage: Literal[CycleStage.JUDGMENT_PROPOSED] = CycleStage.JUDGMENT_PROPOSED
    proposal: ProposedJudgment

    @model_validator(mode="after")
    def proposal_shares_the_context(self) -> Self:
        _derivation_matches(self.context, self.proposal.derivation, "proposal")
        return self


class UnityAccepted(_CycleStateBase):
    stage: Literal[CycleStage.UNITY_ACCEPTED] = CycleStage.UNITY_ACCEPTED
    proposal: ProposedJudgment
    unity_check: UnityCheck

    @model_validator(mode="after")
    def unity_shares_the_context_and_passes(self) -> Self:
        _derivation_matches(self.context, self.proposal.derivation, "proposal")
        _context_matches(
            self.context,
            self.unity_check.scope,
            self.unity_check.configuration,
            "unity check",
        )
        if not self.unity_check.passed:
            raise ValueError("only a successful unity check may enter unity-accepted")
        return self


class CommitmentCompleted(_CycleStateBase):
    stage: Literal[CycleStage.COMMITMENT_COMPLETED] = CycleStage.COMMITMENT_COMPLETED
    judgment: CommittedJudgment

    @model_validator(mode="after")
    def judgment_shares_the_context(self) -> Self:
        _derivation_matches(self.context, self.judgment.derivation, "judgment")
        return self


_ALLOWED_TERMINAL_BOUNDARIES: dict[OutcomeKind, frozenset[CycleBoundary]] = {
    OutcomeKind.INPUT_ERROR: frozenset({CycleBoundary.INPUT_VALIDATION}),
    OutcomeKind.NOT_PRESENTABLE: frozenset({CycleBoundary.VARIANT_PROJECTION}),
    OutcomeKind.SYNTHESIS_FAILED: frozenset(
        {
            CycleBoundary.RETENTION,
            CycleBoundary.RECOGNITION,
            CycleBoundary.OBJECT_FORMATION,
        }
    ),
    OutcomeKind.SYNTHESIS_AMBIGUOUS: frozenset({CycleBoundary.RECOGNITION}),
    OutcomeKind.CONCEPT_NOT_APPLICABLE: frozenset({CycleBoundary.APPLICATION}),
    OutcomeKind.APPLICATION_UNDERDETERMINED: frozenset({CycleBoundary.APPLICATION}),
    OutcomeKind.UNITY_CONFLICT: frozenset({CycleBoundary.UNITY}),
    OutcomeKind.JUDGMENT_WITHHELD: frozenset(
        {CycleBoundary.PROPOSAL, CycleBoundary.COMMITMENT}
    ),
    OutcomeKind.JUDGMENT_COMMITTED: frozenset({CycleBoundary.CRITIQUE}),
    OutcomeKind.OVERREACH: frozenset({CycleBoundary.UNITY}),
}


class CycleTerminated(_CycleStateBase):
    stage: Literal[CycleStage.TERMINAL] = CycleStage.TERMINAL
    boundary: CycleBoundary
    outcome: TerminalOutcome

    @model_validator(mode="after")
    def outcome_matches_context_and_boundary(self) -> Self:
        _context_matches(
            self.context,
            self.outcome.context.limit_report.scope,
            self.outcome.context.configuration,
            "terminal outcome",
        )
        allowed = _ALLOWED_TERMINAL_BOUNDARIES[self.outcome.kind]
        if self.boundary not in allowed:
            raise ValueError(
                f"{self.outcome.kind.value} cannot terminate at {self.boundary.value}"
            )
        return self


CycleState = Annotated[
    CycleOpened
    | ReceptionCompleted
    | ProjectionCompleted
    | ManifoldFormed
    | RetentionCompleted
    | CandidateRecognized
    | ObjectConstituted
    | ConceptApplied
    | JudgmentProposed
    | UnityAccepted
    | CommitmentCompleted
    | CycleTerminated,
    Field(discriminator="stage"),
]

ApplicationResolution = (
    ProposalResult | ConceptNotApplicable | ApplicationUnderdetermined
)

_MINIMUM_RIVAL_COUNT = 2

_CYCLE_STATE_ADAPTER: TypeAdapter[CycleState] = TypeAdapter(CycleState)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidTransition(message)


def _terminal(
    current: _CycleStateBase,
    boundary: CycleBoundary,
    outcome: TerminalOutcome,
) -> CycleTerminated:
    return CycleTerminated(
        cycle_id=current.cycle_id,
        context=current.context,
        boundary=boundary,
        outcome=outcome,
    )


def reject_input(
    cycle_id: Identifier,
    context: RoleContext,
    outcome: InputError,
) -> CycleTerminated:
    """End before cognition when external validation produced ``input-error``."""

    return CycleTerminated(
        cycle_id=cycle_id,
        context=context,
        boundary=CycleBoundary.INPUT_VALIDATION,
        outcome=outcome,
    )


def open_cycle(
    cycle_id: Identifier,
    observations: tuple[Observation, ...],
    context: RoleContext,
) -> CycleOpened:
    """Freeze a valid observation episode, scope, and configuration."""

    return CycleOpened(
        cycle_id=cycle_id,
        observations=observations,
        context=context,
    )


def record_reception(
    current: CycleOpened,
    presented_elements: tuple[PresentedElement, ...],
) -> ReceptionCompleted:
    """Record one shared presentation for every admitted observation."""

    observation_ids = {item.observation_id for item in current.observations}
    presented_observation_ids = {item.observation_id for item in presented_elements}
    _require(
        presented_observation_ids == observation_ids,
        "reception must account for every and only the cycle observations",
    )
    _require(
        len(presented_elements) == len(current.observations),
        "shared reception must produce one element per observation",
    )
    return ReceptionCompleted(
        cycle_id=current.cycle_id,
        context=current.context,
        presented_elements=presented_elements,
    )


def record_projection(
    current: ReceptionCompleted,
    result: tuple[Intuition, ...] | NotPresentable,
) -> ProjectionCompleted | CycleTerminated:
    """Record a complete variant projection or its typed refusal."""

    presented_ids = {item.presented_element_id for item in current.presented_elements}
    if isinstance(result, NotPresentable):
        _require(
            set(result.presented_element_ids) <= presented_ids,
            "not-presentable must identify elements at the projection boundary",
        )
        return _terminal(current, CycleBoundary.VARIANT_PROJECTION, result)

    projected_presented_ids = {item.presented_element_id for item in result}
    _require(
        projected_presented_ids == presented_ids,
        "projection must account for every and only the presented elements",
    )
    return ProjectionCompleted(
        cycle_id=current.cycle_id,
        context=current.context,
        intuitions=result,
    )


def record_manifold(
    current: ProjectionCompleted,
    manifold: ManifoldOfIntuition,
) -> ManifoldFormed:
    """Make exactly the path's projected intuitions available together."""

    intuition_ids = {item.intuition_id for item in current.intuitions}
    _require(
        set(manifold.intuition_ids) == intuition_ids,
        "manifold must contain every and only the projected intuitions",
    )
    return ManifoldFormed(
        cycle_id=current.cycle_id,
        context=current.context,
        manifold=manifold,
    )


def record_retention(
    current: ManifoldFormed,
    result: RetentionResult,
) -> RetentionCompleted | CycleTerminated:
    """Record licensed retention or stop with ``synthesis-failed``."""

    if isinstance(result, SynthesisFailed):
        _require(
            result.manifold_id == current.manifold.manifold_id,
            "retention failure must identify the current manifold",
        )
        return _terminal(current, CycleBoundary.RETENTION, result)

    _require(
        result.manifold_id == current.manifold.manifold_id,
        "retained sequence must identify the current manifold",
    )
    return RetentionCompleted(
        cycle_id=current.cycle_id,
        context=current.context,
        retained_sequence=result,
    )


def _check_recognized_alternatives(
    candidates: tuple[CandidateRepresentation, ...],
) -> None:
    candidate_ids = {item.candidate_representation_id for item in candidates}
    _require(
        len(candidate_ids) == len(candidates),
        "recognition must not return duplicate candidate IDs",
    )
    if len(candidates) < _MINIMUM_RIVAL_COUNT:
        return
    for candidate in candidates:
        other_candidate_ids = candidate_ids - {candidate.candidate_representation_id}
        _require(
            other_candidate_ids <= set(candidate.alternative_candidate_ids),
            "continued rival candidates must identify one another as alternatives",
        )


def record_recognition(
    current: RetentionCompleted,
    result: RecognitionResult,
) -> tuple[CandidateRecognized, ...] | CycleTerminated:
    """Fork explicit candidate paths, or retain typed failure or ambiguity."""

    if isinstance(result, SynthesisFailed):
        _require(
            result.manifold_id == current.retained_sequence.manifold_id,
            "recognition failure must identify the retained manifold",
        )
        return _terminal(current, CycleBoundary.RECOGNITION, result)
    if isinstance(result, SynthesisAmbiguous):
        _require(
            result.context.derivation.has_ground(
                current.retained_sequence.retained_sequence_id,
                GroundKind.RETAINED_SEQUENCE,
            ),
            "recognition ambiguity must identify the current retained sequence",
        )
        return _terminal(current, CycleBoundary.RECOGNITION, result)

    _require(bool(result), "recognition must return at least one candidate")
    _check_recognized_alternatives(result)
    for candidate in result:
        _require(
            candidate.retained_sequence_id
            == current.retained_sequence.retained_sequence_id,
            "recognized candidate must identify the current retained sequence",
        )
    return tuple(
        CandidateRecognized(
            cycle_id=current.cycle_id,
            context=current.context,
            manifold_id=current.retained_sequence.manifold_id,
            candidate=candidate,
        )
        for candidate in result
    )


def record_object_formation(
    current: CandidateRecognized,
    result: ObjectFormationResult,
) -> ObjectConstituted | CycleTerminated:
    """Record local objecthood without applying a concept."""

    if isinstance(result, SynthesisFailed):
        _require(
            result.manifold_id == current.manifold_id,
            "object-formation failure must identify the path's manifold",
        )
        return _terminal(current, CycleBoundary.OBJECT_FORMATION, result)

    _require(
        result.candidate_representation_id
        == current.candidate.candidate_representation_id,
        "object candidate must identify the recognized candidate",
    )
    return ObjectConstituted(
        cycle_id=current.cycle_id,
        context=current.context,
        object_candidate=result,
    )


def record_application(
    current: ObjectConstituted,
    application: ApplicationResult,
) -> ConceptApplied:
    """Record applicability independently of proposal or commitment."""

    _require(
        application.object_candidate_id == current.object_candidate.object_candidate_id,
        "application must identify the constituted object candidate",
    )
    return ConceptApplied(
        cycle_id=current.cycle_id,
        context=current.context,
        application=application,
    )


def _required_condition_ids(
    application: ApplicationResult, status: ConditionStatus
) -> set[str]:
    return {
        item.condition_id
        for item in application.condition_results
        if item.required and item.status is status
    }


def resolve_application(
    current: ConceptApplied,
    result: ApplicationResolution,
) -> JudgmentProposed | CycleTerminated:
    """Propose only from applicability, otherwise expose the matching limit."""

    application = current.application
    if isinstance(result, ConceptNotApplicable):
        failed_ids = _required_condition_ids(application, ConditionStatus.FAILED)
        _require(
            application.status is ApplicationStatus.NOT_APPLICABLE,
            "concept-not-applicable requires a failed application",
        )
        _require(
            result.object_candidate_id == application.object_candidate_id
            and result.application_result_id == application.application_result_id,
            "concept-not-applicable must identify the current application",
        )
        _require(
            failed_ids <= set(result.failed_condition_ids),
            "concept-not-applicable must expose every required failed condition",
        )
        return _terminal(current, CycleBoundary.APPLICATION, result)

    if isinstance(result, ApplicationUnderdetermined):
        undecided_ids = _required_condition_ids(application, ConditionStatus.UNDECIDED)
        _require(
            application.status is ApplicationStatus.UNDERDETERMINED,
            "application-underdetermined requires an undecided application",
        )
        _require(
            result.object_candidate_id == application.object_candidate_id
            and result.application_result_id == application.application_result_id,
            "application-underdetermined must identify the current application",
        )
        _require(
            undecided_ids <= set(result.undecided_condition_ids),
            "application-underdetermined must expose every required "
            "undecided condition",
        )
        return _terminal(current, CycleBoundary.APPLICATION, result)

    if isinstance(result, JudgmentWithheld):
        _require(
            application.status is ApplicationStatus.APPLICABLE,
            "proposal withholding after application requires applicability",
        )
        _require(
            application.application_result_id in result.strongest_representation_ids,
            "withholding must preserve the successful application",
        )
        return _terminal(current, CycleBoundary.PROPOSAL, result)

    _require(
        application.status is ApplicationStatus.APPLICABLE,
        "only an applicable result may ground a proposal",
    )
    _require(
        result.proposition.subject_candidate_id == application.object_candidate_id,
        "proposal subject must identify the application object",
    )
    _require(
        result.warrant.application_result_id == application.application_result_id,
        "proposal warrant must identify the current application",
    )
    return JudgmentProposed(
        cycle_id=current.cycle_id,
        context=current.context,
        proposal=result,
    )


def withhold_rival_applications(
    current: tuple[ConceptApplied, ...],
    outcome: JudgmentWithheld,
) -> CycleTerminated:
    """Converge successful rival paths without inventing a singular subject."""

    _require(
        len(current) >= _MINIMUM_RIVAL_COUNT,
        "rival-path withholding requires at least two application paths",
    )
    first = current[0]
    _require(
        all(
            item.cycle_id == first.cycle_id and item.context == first.context
            for item in current
        ),
        "rival application paths must belong to one cycle context",
    )
    application_ids = {item.application.application_result_id for item in current}
    _require(
        len(application_ids) == len(current),
        "rival application paths must have distinct application IDs",
    )
    _require(
        all(
            item.application.status is ApplicationStatus.APPLICABLE for item in current
        ),
        "rival-path withholding requires successful applications",
    )
    _require(
        application_ids <= set(outcome.strongest_representation_ids),
        "withholding must preserve every rival application",
    )
    return _terminal(first, CycleBoundary.PROPOSAL, outcome)


def record_unity(
    current: JudgmentProposed,
    result: UnityResult,
) -> UnityAccepted | CycleTerminated:
    """Accept cycle-wide unity or preserve its typed conflict or overreach."""

    proposal_id = current.proposal.proposed_judgment_id
    if isinstance(result, UnityConflict):
        _require(
            result.proposed_judgment_id == proposal_id,
            "unity conflict must identify the current proposal",
        )
        return _terminal(current, CycleBoundary.UNITY, result)
    if isinstance(result, Overreach):
        _require(
            result.context.derivation.has_ground(proposal_id, GroundKind.JUDGMENT),
            "overreach must remain grounded in the rejected proposal",
        )
        return _terminal(current, CycleBoundary.UNITY, result)

    _require(result.passed, "failed unity requires a unity-conflict outcome")
    proposal_is_evidence = any(
        evidence.ground_id == proposal_id and evidence.kind is GroundKind.JUDGMENT
        for condition in result.condition_results
        for evidence in condition.evidence
    )
    _require(
        proposal_is_evidence,
        "successful unity must identify the proposal among its evidence",
    )
    return UnityAccepted(
        cycle_id=current.cycle_id,
        context=current.context,
        proposal=current.proposal,
        unity_check=result,
    )


def record_commitment(
    current: UnityAccepted,
    result: CommitmentResult,
) -> CommitmentCompleted | CycleTerminated:
    """Commit after successful unity or retain a typed withholding."""

    proposal_id = current.proposal.proposed_judgment_id
    if isinstance(result, JudgmentWithheld):
        _require(
            proposal_id in result.strongest_representation_ids,
            "commitment withholding must preserve the proposal",
        )
        return _terminal(current, CycleBoundary.COMMITMENT, result)

    _require(
        result.proposed_judgment_id == proposal_id,
        "committed judgment must identify the unity-checked proposal",
    )
    _require(
        result.warrant.unity_check == current.unity_check,
        "committed judgment must use the accepted unity check",
    )
    return CommitmentCompleted(
        cycle_id=current.cycle_id,
        context=current.context,
        judgment=result,
    )


def record_critique(
    current: CommitmentCompleted,
    outcome: JudgmentCommitted,
) -> CycleTerminated:
    """Close a successful path with its scoped warrant and limit report."""

    _require(
        outcome.judgment == current.judgment,
        "judgment-committed must contain the path's committed judgment",
    )
    return _terminal(current, CycleBoundary.CRITIQUE, outcome)


def validate_cycle_state(value: object) -> CycleState:
    """Validate an untrusted snapshot through the discriminated state union."""

    return _CYCLE_STATE_ADAPTER.validate_python(value)


def validate_cycle_state_json(value: str | bytes) -> CycleState:
    """Validate a serialized snapshot while preserving strict scalar types."""

    return _CYCLE_STATE_ADAPTER.validate_json(value)


def dump_cycle_state(state: CycleState) -> str:
    """Return deterministic compact JSON for one immutable cycle snapshot."""

    return _CYCLE_STATE_ADAPTER.dump_json(state).decode("utf-8")
