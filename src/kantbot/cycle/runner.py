"""Pure orchestration of role callables, checked transitions, and closed graphs."""

from dataclasses import dataclass, replace
from itertools import pairwise
from typing import Annotated

from pydantic import Field, TypeAdapter, ValidationError

from kantbot.cycle._support import (
    derive,
    extend_trace,
    ground,
    outcome_context,
    replace_value,
    rule_ground,
)
from kantbot.cycle.configuration import AmbiguityPolicy, CyclePlan
from kantbot.cycle.judgment import (
    apply_concept,
    commit_judgment,
    constitute_object,
    critique_and_report,
    object_conditions,
    propose_judgment,
)
from kantbot.cycle.reception import (
    form_manifold,
    present_observation,
    project_intuition,
)
from kantbot.cycle.synthesis import (
    EnumerateCandidates,
    FigurativePolicy,
    FigurativeRequest,
    FigurativeSynthesis,
    SearchCapacityExceeded,
    retain_episode,
)
from kantbot.cycle.unity import ancestry, check_unity
from kantbot.interfaces import (
    ApplicationRequest,
    ApplyConcept,
    CheckUnity,
    CommitJudgment,
    CommitmentRequest,
    ConstituteObject,
    CritiqueAndReport,
    FormManifold,
    ManifoldRequest,
    ObjectFormationRequest,
    PresentObservation,
    ProjectIntuition,
    ProjectionRequest,
    ProposalRequest,
    ProposeJudgment,
    ReceptionRequest,
    RecognitionRequest,
    RecognitionResult,
    RecognizeCandidates,
    RetainIntuitions,
    RetentionRequest,
    UnityRequest,
)
from kantbot.model import (
    ApplicationResult,
    ApplicationStatus,
    ApplicationUnderdetermined,
    AssembledWarrant,
    CognitiveGround,
    ConceptNotApplicable,
    GroundKind,
    InputError,
    Intuition,
    JudgmentCommitted,
    JudgmentWithheld,
    Modality,
    ObjectCandidate,
    Observation,
    OutcomeKind,
    Proposition,
    RetainedSequence,
    RetentionStatus,
    SemanticModel,
    SynthesisAmbiguous,
    SynthesisFailed,
    SynthesisPolicy,
    TerminalOutcome,
    UnityCheck,
)
from kantbot.model.common import NonEmptyText
from kantbot.provenance import ExternalInputReference, ProvenanceGraph, ProvenanceTrace
from kantbot.transitions import (
    CandidateRecognized,
    CommitmentCompleted,
    ConceptApplied,
    CycleOpened,
    CycleTerminated,
    InvalidTransition,
    ManifoldFormed,
    ObjectConstituted,
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
    reject_input,
    resolve_application,
    withhold_rival_applications,
)


@dataclass(frozen=True)
class CyclePolicies:
    """Replace only the live boundaries needed by a declared experiment."""

    present: PresentObservation = present_observation
    project: ProjectIntuition = project_intuition
    manifold: FormManifold = form_manifold
    retain: RetainIntuitions = retain_episode
    recognize: RecognizeCandidates | None = None
    figurative: FigurativeSynthesis | None = None
    constitute: ConstituteObject = constitute_object
    apply: ApplyConcept = apply_concept
    propose: ProposeJudgment = propose_judgment
    unity: CheckUnity = check_unity
    commit: CommitJudgment = commit_judgment
    critique: CritiqueAndReport = critique_and_report


class OperationRecord(SemanticModel):
    """Executed role operation with links to related canonical artifacts."""

    operation: NonEmptyText
    artifacts: tuple[CognitiveGround, ...] = ()


@dataclass(frozen=True)
class CycleExecution:
    """A validated graph and terminal paths, with execution order for inspection."""

    graph: ProvenanceGraph
    terminal_states: tuple[CycleTerminated, ...]
    operations: tuple[OperationRecord, ...]
    reports: tuple[str, ...]

    def __post_init__(self) -> None:
        outcomes = tuple(state.outcome for state in self.terminal_states)
        if not outcomes or len(self.reports) != len(outcomes):
            raise ValueError("execution requires reported terminal paths")
        if len(outcomes) != len(self.trace.outcomes) or set(outcomes) != set(
            self.trace.outcomes
        ):
            raise ValueError("terminal paths must match the certified outcomes")
        if any(
            state.cycle_id != self.trace.cycle_id
            or state.context.scope != self.trace.scope
            or state.context.configuration != self.trace.configuration
            for state in self.terminal_states
        ):
            raise ValueError("terminal paths must share the certified cycle context")

    @property
    def trace(self) -> ProvenanceTrace:
        return self.graph.trace

    @property
    def outcomes(self) -> tuple[TerminalOutcome, ...]:
        return tuple(state.outcome for state in self.terminal_states)


@dataclass(frozen=True)
class _Run:
    plan: CyclePlan
    policies: CyclePolicies
    trace: ProvenanceTrace
    operations: tuple[OperationRecord, ...] = ()

    def add(self, **collections: tuple[SemanticModel, ...]) -> "_Run":
        trace = extend_trace(self.trace, **collections)
        ProvenanceGraph(trace)
        return replace(self, trace=trace)

    def record(
        self, operation: str, artifacts: tuple[CognitiveGround, ...] = ()
    ) -> "_Run":
        return replace(
            self,
            operations=(
                *self.operations,
                OperationRecord(operation=operation, artifacts=artifacts),
            ),
        )

    def finish(self, states: tuple[CycleTerminated, ...]) -> CycleExecution:
        run = self
        for state in states:
            outcome = state.outcome
            report = outcome.context.limit_report
            if report not in run.trace.limit_reports:
                run = run.add(limit_reports=(report,))
            if outcome not in run.trace.outcomes:
                run = run.add(outcomes=(outcome,))
        graph = ProvenanceGraph(run.trace)
        for state in states:
            if isinstance(state.outcome, JudgmentCommitted):
                committed = CommitmentCompleted(
                    cycle_id=self.plan.cycle_id,
                    context=self.plan.context,
                    judgment=state.outcome.judgment,
                )
                record_critique(committed, state.outcome, graph)
        reports = tuple(self.policies.critique(state.outcome) for state in states)
        return CycleExecution(
            graph,
            states,
            (*run.operations, OperationRecord(operation="critique")),
            reports,
        )


_OBSERVATIONS: TypeAdapter[Annotated[tuple[Observation, ...], Field(min_length=1)]] = (
    TypeAdapter(Annotated[tuple[Observation, ...], Field(min_length=1)])
)


def _open(run: _Run, supplied: object) -> CycleOpened | CycleExecution:
    try:
        observations = _OBSERVATIONS.validate_python(supplied, strict=True)
        opened = open_cycle(run.plan.cycle_id, observations, run.plan.context)
    except ValidationError as error:
        errors = tuple(
            f"{item['loc']}: {item['msg']}"
            for item in error.errors(include_input=False)
        )
        return _input_error(run, errors)
    if any(left.position > right.position for left, right in pairwise(observations)):
        return _input_error(
            run, ("Observation positions must already be nondecreasing",)
        )
    if len(observations) > run.plan.observation_budget:
        raise SearchCapacityExceeded(
            "observation count exceeds the declared cycle budget"
        )
    return opened


def _input_error(run: _Run, errors: tuple[str, ...]) -> CycleExecution:
    input_id = f"input:{run.plan.cycle_id}"
    outcome = InputError(
        outcome_id=f"outcome:{input_id}",
        invalid_input_ids=(input_id,),
        errors=errors,
        context=outcome_context(
            run.plan.context,
            OutcomeKind.INPUT_ERROR,
            input_id,
            (ground(input_id, GroundKind.EXTERNAL_INPUT),),
        ),
    )
    run = run.add(
        external_inputs=(
            ExternalInputReference(
                input_id=input_id, description="Rejected observation batch"
            ),
        )
    )
    return run.finish((reject_input(run.plan.cycle_id, run.plan.context, outcome),))


def _check_retention(request: RetentionRequest, retained: RetainedSequence) -> None:
    """Earlier data must enter through actual reproduction under the selected rule."""

    available = {item.intuition_id: item for item in request.intuitions}
    latest = request.intuitions[-1].position
    current_ids = {
        item.intuition_id for item in request.intuitions if item.position == latest
    }
    if not current_ids <= {item.intuition_id for item in retained.items}:
        raise InvalidTransition("retention must preserve every current presentation")
    for item in retained.items:
        intuition = available.get(item.intuition_id)
        if intuition is None:
            raise InvalidTransition("retention introduced unavailable sensible content")
        current = intuition.position == latest
        if current != (item.status is RetentionStatus.CURRENT):
            raise InvalidTransition("earlier intuitions must be explicitly reproduced")
        if not current and item.retention_rule_id != request.retention_rule.rule_id:
            raise InvalidTransition(
                "reproduction must cite the selected retention rule"
            )


def _synthesize(
    run: _Run, current: ManifoldFormed
) -> tuple[_Run, tuple[CandidateRecognized, ...] | CycleTerminated]:
    plan = run.plan
    rules = {rule.rule_id: rule for rule in plan.repertoire.rules}
    request = RetentionRequest(
        manifold=current.manifold,
        intuitions=run.trace.intuitions,
        retention_rule=rules[plan.retention_rule_id],
        context=plan.context,
    )
    identity = tuple(rules[item] for item in plan.identity_rule_ids)
    constitutive = tuple(rules[item] for item in plan.constitutive_rule_ids)
    if plan.synthesis_policy is SynthesisPolicy.B_LED_FIGURATIVE:
        if run.policies.recognize is not None:
            raise ValueError("B-led recognition belongs to the figurative policy")
        policy = run.policies.figurative or FigurativePolicy(
            run.policies.retain, plan.path_budget
        )
        bundle = policy(
            FigurativeRequest(request, identity, constitutive),
            ProvenanceGraph(run.trace),
        )
        retained = bundle.retention
        recognition = bundle.recognition
        run = run.record("figurative-synthesis")
    else:
        # Traversal is explicit and checked before reproduction can supply memory.
        if (
            tuple(item.intuition_id for item in request.intuitions)
            != current.manifold.intuition_ids
        ):
            raise ValueError("apprehension must traverse the declared manifold")
        run = run.record(
            "apprehension",
            tuple(
                ground(item.intuition_id, GroundKind.INTUITION)
                for item in request.intuitions
            ),
        )
        retained = run.policies.retain(request)
        recognition = None
        run = run.record("reproduction")
    if isinstance(retained, RetainedSequence):
        _check_retention(request, retained)
    retained_state = record_retention(current, retained)
    if isinstance(retained_state, CycleTerminated):
        return run, retained_state
    run = run.add(retained_sequences=(retained_state.retained_sequence,))
    if plan.synthesis_policy is SynthesisPolicy.A_ANALYSIS_B_CONSTRAINT:
        recognizer = run.policies.recognize or EnumerateCandidates(plan.path_budget)
        recognition = recognizer(
            RecognitionRequest(
                retained_sequence=retained_state.retained_sequence,
                identity_rules=identity,
                constitutive_rules=constitutive,
                policy=plan.synthesis_policy,
                context=plan.context,
            ),
            ProvenanceGraph(run.trace),
        )
        run = run.record("recognition")
    if recognition is None:
        raise ValueError("figurative synthesis omitted recognition after retention")
    request_for_check = RecognitionRequest(
        retained_sequence=retained_state.retained_sequence,
        identity_rules=identity,
        constitutive_rules=constitutive,
        policy=plan.synthesis_policy,
        context=plan.context,
    )
    run = _certify_recognition(run, request_for_check, recognition)
    if (
        isinstance(recognition, tuple)
        and len(recognition) > 1
        and plan.ambiguity_policy is AmbiguityPolicy.STOP
    ):
        ids = tuple(item.candidate_representation_id for item in recognition)
        label = "recognition-ambiguity"
        context = outcome_context(
            plan.context,
            OutcomeKind.SYNTHESIS_AMBIGUOUS,
            label,
            (
                ground(
                    retained_state.retained_sequence.retained_sequence_id,
                    GroundKind.RETAINED_SEQUENCE,
                ),
            ),
        )
        context = replace_value(
            context,
            limit_report=replace_value(context.limit_report, alternative_ids=ids),
        )
        recognition = SynthesisAmbiguous(
            outcome_id=f"outcome:{label}",
            candidate_representation_ids=ids,
            context=context,
        )
    return run, record_recognition(retained_state, recognition)


def _certify_recognition(
    run: _Run, request: RecognitionRequest, result: RecognitionResult
) -> _Run:
    """Verify completeness against the bounded domain declared by this library."""

    expected = EnumerateCandidates(
        run.plan.path_budget,
        include_objective_unity=request.policy is SynthesisPolicy.B_LED_FIGURATIVE,
    )(request, ProvenanceGraph(run.trace))
    if isinstance(expected, SynthesisFailed):
        if not isinstance(result, SynthesisFailed) or set(
            result.failed_rule_ids
        ) != set(expected.failed_rule_ids):
            raise InvalidTransition("recognition contradicts the declared rule results")
        return run
    if not isinstance(expected, tuple):
        raise InvalidTransition("recognition kernel returned an unsupported result")
    if isinstance(result, SynthesisAmbiguous):
        expected_ids = {item.candidate_representation_id for item in expected}
        if set(result.candidate_representation_ids) != expected_ids:
            raise InvalidTransition("ambiguity omitted an admissible candidate")
        return run.add(candidates=expected)
    if not isinstance(result, tuple):
        raise InvalidTransition("recognition omitted admissible identity paths")
    if len(result) != len(expected) or {item.intuition_ids for item in result} != {
        item.intuition_ids for item in expected
    }:
        raise InvalidTransition(
            "recognition omitted or invented admissible identity paths"
        )
    for candidate in result:
        if (
            candidate.policy,
            candidate.identity_rule_ids,
            candidate.constitutive_rule_ids,
        ) != (
            request.policy,
            run.plan.identity_rule_ids,
            run.plan.constitutive_rule_ids,
        ):
            raise InvalidTransition(
                "recognition changed the selected interpretation or rules"
            )
    return run.add(candidates=result)


def _objects(
    run: _Run, candidates: tuple[CandidateRecognized, ...]
) -> tuple[_Run, tuple[ObjectConstituted, ...], tuple[CycleTerminated, ...]]:
    objects: list[ObjectConstituted] = []
    stopped: list[CycleTerminated] = []
    for current in candidates:
        graph = ProvenanceGraph(run.trace)
        identity, constitutive = object_conditions(current.candidate, graph)
        result = run.policies.constitute(
            ObjectFormationRequest(
                candidate=current.candidate,
                identity_results=identity,
                constitutive_results=constitutive,
                context=run.plan.context,
            ),
            graph,
        )
        state = record_object_formation(current, result)
        if isinstance(state, CycleTerminated):
            stopped.append(state)
        else:
            run = run.add(object_candidates=(state.object_candidate,)).record(
                "object-formation",
                (
                    ground(
                        state.object_candidate.object_candidate_id,
                        GroundKind.OBJECT_CANDIDATE,
                    ),
                ),
            )
            objects.append(state)
    return run, tuple(objects), tuple(stopped)


def _application_limit(run: _Run, current: ConceptApplied) -> CycleTerminated:
    application = current.application
    missing = tuple(
        item.condition_id
        for item in application.condition_results
        if item.required and not item.passed
    )
    label = f"application-limit:{application.application_result_id}"
    grounds = (
        ground(application.application_result_id, GroundKind.APPLICATION_RESULT),
    )
    outcome: ConceptNotApplicable | ApplicationUnderdetermined
    if application.status is ApplicationStatus.NOT_APPLICABLE:
        outcome = ConceptNotApplicable(
            outcome_id=f"outcome:{label}",
            object_candidate_id=application.object_candidate_id,
            application_result_id=application.application_result_id,
            failed_condition_ids=missing,
            context=outcome_context(
                run.plan.context,
                OutcomeKind.CONCEPT_NOT_APPLICABLE,
                label,
                grounds,
                missing=missing,
            ),
        )
    else:
        outcome = ApplicationUnderdetermined(
            outcome_id=f"outcome:{label}",
            object_candidate_id=application.object_candidate_id,
            application_result_id=application.application_result_id,
            undecided_condition_ids=missing,
            context=outcome_context(
                run.plan.context,
                OutcomeKind.APPLICATION_UNDERDETERMINED,
                label,
                grounds,
                missing=missing,
            ),
        )
    result = resolve_application(current, outcome)
    if not isinstance(result, CycleTerminated):
        raise ValueError("application limit did not terminate its path")
    return result


def _warrant(run: _Run, application: ApplicationResult) -> AssembledWarrant:
    graph = ProvenanceGraph(run.trace)
    lineage = ancestry(
        ground(application.application_result_id, GroundKind.APPLICATION_RESULT), graph
    )

    def of_kind(*kinds: GroundKind) -> tuple[CognitiveGround, ...]:
        return tuple(item for item in lineage if item.kind in kinds)

    return AssembledWarrant(
        observation_grounds=of_kind(GroundKind.OBSERVATION),
        presentation_form_ids=tuple(
            form.form_id for form in run.plan.projection.required_forms
        ),
        projection_grounds=of_kind(GroundKind.VARIANT_PROJECTION),
        synthesis_grounds=of_kind(
            GroundKind.MANIFOLD,
            GroundKind.RETAINED_SEQUENCE,
            GroundKind.CANDIDATE_REPRESENTATION,
            GroundKind.OBJECT_CANDIDATE,
        ),
        identity_rule_grounds=tuple(
            rule_ground(graph.rule_for(item)) for item in run.plan.identity_rule_ids
        ),
        constitutive_rule_grounds=tuple(
            rule_ground(graph.rule_for(item))
            for item in (run.plan.retention_rule_id, *run.plan.constitutive_rule_ids)
        ),
        concept_ground=ground(application.concept_id, GroundKind.CONCEPT),
        schema_ground=ground(application.schema_id, GroundKind.SCHEMA),
        application_ground=ground(
            application.application_result_id, GroundKind.APPLICATION_RESULT
        ),
        scope=run.plan.context.scope,
        configuration=run.plan.context.configuration,
    )


def _commit_path(
    run: _Run, current: ConceptApplied, obj: ObjectCandidate
) -> tuple[_Run, CycleTerminated]:
    application = current.application
    concept = next(
        item
        for item in run.plan.repertoire.concepts
        if item.concept_id == application.concept_id
    )
    proposal = run.policies.propose(
        ProposalRequest(
            object_candidate=obj,
            application=application,
            proposition=Proposition(
                subject_candidate_id=obj.object_candidate_id,
                predicate_concept_id=concept.concept_id,
                text=(
                    f"The selected candidate satisfies {concept.name} "
                    "within the supplied episode"
                ),
                modality=Modality.ASSERTORIC,
            ),
            warrant=_warrant(run, application),
            context=run.plan.context,
        )
    )
    proposed = resolve_application(current, proposal)
    if isinstance(proposed, CycleTerminated):
        return run, proposed
    run = run.add(proposals=(proposed.proposal,)).record(
        "judgment-proposal",
        (ground(proposed.proposal.proposed_judgment_id, GroundKind.JUDGMENT),),
    )
    unity_request = UnityRequest(proposal=proposed.proposal, context=run.plan.context)
    graph = ProvenanceGraph(run.trace)
    unity = check_unity(unity_request, graph)
    if isinstance(unity, UnityCheck) and run.policies.unity is not check_unity:
        selected = run.policies.unity(unity_request, graph)
        if isinstance(selected, UnityCheck):
            conditions = {item.condition_id: item for item in unity.condition_results}
            for condition in selected.condition_results:
                previous = conditions.get(condition.condition_id)
                if previous is not None and previous != condition:
                    raise ValueError("unity policy rewrote a mandatory condition")
                conditions[condition.condition_id] = condition
            selected = replace_value(
                selected, condition_results=tuple(conditions.values())
            )
        unity = selected
    accepted = record_unity(proposed, unity)
    run = run.record("cycle-wide-unity")
    if isinstance(accepted, CycleTerminated):
        return run, accepted
    run = run.add(unity_checks=(accepted.unity_check,))
    return _commit_accepted(run, accepted)


def _commit_accepted(
    run: _Run, accepted: UnityAccepted
) -> tuple[_Run, CycleTerminated]:
    proposal = accepted.proposal
    context = outcome_context(
        run.plan.context,
        OutcomeKind.JUDGMENT_COMMITTED,
        f"committed:{proposal.proposed_judgment_id}",
        (ground(proposal.proposed_judgment_id, GroundKind.JUDGMENT),),
    )
    result = run.policies.commit(
        CommitmentRequest(
            proposal=proposal,
            unity_check=accepted.unity_check,
            limit_report=context.limit_report,
            derivation=derive(
                run.plan.context,
                "commit after objective unity",
                (ground(proposal.proposed_judgment_id, GroundKind.JUDGMENT),),
            ),
            context=run.plan.context,
        )
    )
    if isinstance(result, JudgmentWithheld):
        state = record_commitment(accepted, result, ProvenanceGraph(run.trace))
        if not isinstance(state, CycleTerminated):
            raise ValueError("withheld commitment did not terminate")
        return run, state
    run = run.add(limit_reports=(context.limit_report,), judgments=(result,)).record(
        "commitment", (ground(result.judgment_id, GroundKind.JUDGMENT),)
    )
    committed = record_commitment(accepted, result, ProvenanceGraph(run.trace))
    if not isinstance(committed, CommitmentCompleted):
        raise ValueError("commitment unexpectedly withheld")
    outcome = JudgmentCommitted(
        outcome_id=f"outcome:{result.judgment_id}", judgment=result, context=context
    )
    run = run.add(outcomes=(outcome,))
    state = record_critique(committed, outcome, ProvenanceGraph(run.trace))
    return run, state


def _judge(
    run: _Run,
    objects: tuple[ObjectConstituted, ...],
    stopped: tuple[CycleTerminated, ...],
) -> CycleExecution:
    plan = run.plan
    concept = next(
        item for item in plan.repertoire.concepts if item.concept_id == plan.concept_id
    )
    schema = next(
        item for item in plan.repertoire.schemas if item.schema_id == plan.schema_id
    )
    applicable: list[ConceptApplied] = []
    terminal = list(stopped)
    applications: list[ApplicationResult] = []
    for obj in objects:
        application = run.policies.apply(
            ApplicationRequest(
                object_candidate=obj.object_candidate,
                concept=concept,
                concept_schema=schema,
                context=plan.context,
            ),
            ProvenanceGraph(run.trace),
        )
        record_application(obj, application)
        applications.append(application)
    application_ids = tuple(item.application_result_id for item in applications)
    linked = tuple(
        replace_value(
            item,
            alternative_application_ids=tuple(
                dict.fromkeys(
                    (
                        *item.alternative_application_ids,
                        *(
                            other
                            for other in application_ids
                            if other != item.application_result_id
                        ),
                    )
                )
            ),
        )
        for item in applications
    )
    run = run.add(applications=linked)
    for obj, application in zip(objects, linked, strict=True):
        current = record_application(obj, application)
        run = run.record(
            "schema-application",
            (ground(application.application_result_id, GroundKind.APPLICATION_RESULT),),
        )
        if not application.applicable:
            terminal.append(_application_limit(run, current))
        else:
            applicable.append(current)
    if len(objects) > 1 and applicable:
        terminal.append(_withhold_rivals(run, tuple(applicable)))
    elif applicable:
        run, state = _commit_path(run, applicable[0], objects[0].object_candidate)
        terminal.append(state)
    return run.finish(tuple(terminal))


def _withhold_rivals(run: _Run, paths: tuple[ConceptApplied, ...]) -> CycleTerminated:
    ids = tuple(item.application.application_result_id for item in paths)
    missing = ("unambiguous-singular-subject",)
    context = outcome_context(
        run.plan.context,
        OutcomeKind.JUDGMENT_WITHHELD,
        "rival-subjects",
        tuple(ground(item, GroundKind.APPLICATION_RESULT) for item in ids),
        missing=missing,
    )
    context = replace_value(
        context,
        limit_report=replace_value(
            context.limit_report,
            alternative_ids=tuple(
                item.candidate_representation_id for item in run.trace.candidates
            ),
        ),
    )
    outcome = JudgmentWithheld(
        outcome_id="outcome:rival-subjects",
        strongest_representation_ids=ids,
        unmet_condition_ids=missing,
        context=context,
    )
    if len(paths) > 1:
        return withhold_rival_applications(paths, outcome)
    result = resolve_application(paths[0], outcome)
    if not isinstance(result, CycleTerminated):
        raise ValueError("unresolved subject did not withhold judgment")
    return result


def run_cycle(
    supplied: object, plan: CyclePlan, *, policies: CyclePolicies | None = None
) -> CycleExecution:
    """Execute one admitted batch under a frozen plan, without world capabilities.

    ``supplied`` is a tuple of canonical observations (or strict Python records).
    External shape/episode/order errors produce input-error. Incoherent role
    implementations still raise programming errors; they cannot forge warrant.
    """

    trace = ProvenanceTrace(
        cycle_id=plan.cycle_id,
        scope=plan.context.scope,
        configuration=plan.context.configuration,
        forms=plan.forms,
        projections=(plan.projection,),
        rules=plan.repertoire.rules + plan.reserved_rules,
        concepts=plan.repertoire.concepts,
        schemas=plan.repertoire.schemas,
    )
    run = _Run(plan, policies or CyclePolicies(), trace)
    ProvenanceGraph(trace)
    opened = _open(run, supplied)
    if isinstance(opened, CycleExecution):
        return opened
    run = run.add(observations=opened.observations)
    presentations = tuple(
        run.policies.present(ReceptionRequest(observation=item, context=plan.context))
        for item in opened.observations
    )
    received = record_reception(opened, presentations)
    run = run.add(presented_elements=presentations).record(
        "shared-reception",
        tuple(
            ground(item.presented_element_id, GroundKind.PRESENTED_ELEMENT)
            for item in presentations
        ),
    )
    results = tuple(
        run.policies.project(
            ProjectionRequest(
                presented_element=item,
                projection=plan.projection,
                context=plan.context,
                available_form_ids=plan.available_form_ids,
            )
        )
        for item in presentations
    )
    intuitions = tuple(item for item in results if isinstance(item, Intuition))
    if plan.available_form_ids is not None and any(
        not set(item.form_ids) <= set(plan.available_form_ids) for item in intuitions
    ):
        raise InvalidTransition("projection used forms unavailable to this episode")
    refusals = tuple(item for item in results if not isinstance(item, Intuition))
    run = run.add(intuitions=intuitions).record(
        "variant-projection",
        tuple(ground(item.intuition_id, GroundKind.INTUITION) for item in intuitions),
    )
    if refusals:
        states = tuple(record_projection(received, refusal) for refusal in refusals)
        return run.finish(
            tuple(state for state in states if isinstance(state, CycleTerminated))
        )
    projected = record_projection(received, intuitions)
    if isinstance(projected, CycleTerminated):
        raise ValueError("successful projection unexpectedly refused")
    manifold = run.policies.manifold(
        ManifoldRequest(intuitions=intuitions, context=plan.context)
    )
    formed = record_manifold(projected, manifold)
    run = run.add(manifolds=(manifold,)).record(
        "manifold-formation", (ground(manifold.manifold_id, GroundKind.MANIFOLD),)
    )
    run, recognition = _synthesize(run, formed)
    if isinstance(recognition, CycleTerminated):
        return run.finish((recognition,))
    run, objects, stopped = _objects(run, recognition)
    return _judge(run, objects, stopped)
