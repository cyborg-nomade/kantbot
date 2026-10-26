"""Licensed retention and exhaustive, bounded recognition of temporal paths."""

from dataclasses import dataclass
from itertools import groupby, product
from math import prod
from typing import Protocol

from kantbot.cycle._support import derive, ground, outcome_context, rule_ground
from kantbot.interfaces import (
    ProvenanceView,
    RecognitionRequest,
    RecognitionResult,
    RetainIntuitions,
    RetentionRequest,
    RetentionResult,
)
from kantbot.model import (
    CandidateRepresentation,
    ConditionResult,
    GroundKind,
    Intuition,
    OutcomeKind,
    RetainedIntuition,
    RetainedSequence,
    RetentionStatus,
    Rule,
    SynthesisFailed,
    SynthesisPolicy,
)
from kantbot.procedures import evaluate_procedure


class SearchCapacityExceeded(ValueError):
    """An engineering search bound, never a proof of failed cognition."""


def _retain(request: RetentionRequest, reproduce: bool) -> RetainedSequence:
    if (
        tuple(item.intuition_id for item in request.intuitions)
        != request.manifold.intuition_ids
    ):
        raise ValueError("retention must receive its exact ordered manifold")
    latest = request.intuitions[-1].position
    items: list[RetainedIntuition] = []
    for item in request.intuitions:
        if item.position == latest:
            items.append(
                RetainedIntuition(
                    intuition_id=item.intuition_id, status=RetentionStatus.CURRENT
                )
            )
        elif reproduce:
            items.append(
                RetainedIntuition(
                    intuition_id=item.intuition_id,
                    status=RetentionStatus.REPRODUCED,
                    retention_rule_id=request.retention_rule.rule_id,
                )
            )
    return RetainedSequence(
        retained_sequence_id=f"retained:{request.manifold.manifold_id}",
        manifold_id=request.manifold.manifold_id,
        items=tuple(items),
        derivation=derive(
            request.context,
            "reproduce earlier intuitions"
            if reproduce
            else "retain current moment only",
            (
                ground(request.manifold.manifold_id, GroundKind.MANIFOLD),
                rule_ground(request.retention_rule),
            ),
        ),
    )


def retain_episode(request: RetentionRequest, /) -> RetentionResult:
    """Reproduce earlier moments under the selected episode retention rule."""

    return _retain(request, reproduce=True)


def retain_current(request: RetentionRequest, /) -> RetentionResult:
    """Ablation policy: prior moments are unavailable to recognition."""

    return _retain(request, reproduce=False)


def evaluate_rules(
    rules: tuple[Rule, ...],
    intuitions: tuple[Intuition, ...],
    provenance: ProvenanceView,
) -> tuple[ConditionResult, ...]:
    """Apply exactly the registered rule procedures to the selected sequence."""

    forms = tuple(
        dict.fromkeys(
            form
            for item in intuitions
            for form in provenance.forms_for(item.intuition_id)
        )
    )
    results: list[ConditionResult] = []
    for rule in rules:
        if provenance.rule_for(rule.rule_id) != rule:
            raise ValueError("requested rule differs from registered understanding")
        if rule.sensible_procedure is None:
            raise ValueError("object rule lacks a sensible procedure")
        results.extend(
            evaluate_procedure(
                rule.sensible_procedure, rule.conditions, intuitions, forms
            )
        )
    return tuple(results)


def _recognition_failure(
    request: RecognitionRequest, failed_rule_ids: tuple[str, ...]
) -> SynthesisFailed:
    retained = request.retained_sequence
    label = f"recognition-failed:{retained.retained_sequence_id}"
    return SynthesisFailed(
        outcome_id=f"outcome:{label}",
        manifold_id=retained.manifold_id,
        failed_rule_ids=failed_rule_ids,
        context=outcome_context(
            request.context,
            OutcomeKind.SYNTHESIS_FAILED,
            label,
            (ground(retained.retained_sequence_id, GroundKind.RETAINED_SEQUENCE),),
            missing=("admissible-complete-identity-path",),
        ),
    )


@dataclass(frozen=True)
class EnumerateCandidates:
    """Preserve every admissible whole-interval path within an explicit budget.

    Each path selects one sample per supplied moment; sample order never selects
    a winner. In the B-led operation objective unity also constrains formation.
    """

    path_budget: int = 4096
    include_objective_unity: bool = False

    def __call__(
        self, request: RecognitionRequest, provenance: ProvenanceView, /
    ) -> RecognitionResult:
        intuitions = tuple(
            provenance.intuition_for(item.intuition_id)
            for item in request.retained_sequence.items
        )
        groups = tuple(
            tuple(group)
            for _, group in groupby(intuitions, key=lambda item: item.position)
        )
        if prod(len(group) for group in groups) > self.path_budget:
            raise SearchCapacityExceeded(
                "complete identity search exceeds the declared path budget"
            )
        rules = request.identity_rules
        if self.include_objective_unity:
            rules += request.constitutive_rules
        paths: list[tuple[Intuition, ...]] = []
        rejected: set[str] = set()
        for path in product(*groups):
            failed = tuple(
                rule.rule_id
                for rule in rules
                if not all(
                    result.passed
                    for result in evaluate_rules((rule,), path, provenance)
                )
            )
            if failed:
                rejected.update(failed)
            else:
                paths.append(path)
        if not paths:
            return _recognition_failure(
                request,
                tuple(rule.rule_id for rule in rules if rule.rule_id in rejected),
            )
        retained_id = request.retained_sequence.retained_sequence_id
        candidate_ids = tuple(
            f"candidate:{retained_id}:{index}" for index in range(len(paths))
        )
        return tuple(
            CandidateRepresentation(
                candidate_representation_id=candidate_id,
                retained_sequence_id=retained_id,
                intuition_ids=tuple(item.intuition_id for item in path),
                policy=request.policy,
                identity_rule_ids=tuple(
                    rule.rule_id for rule in request.identity_rules
                ),
                constitutive_rule_ids=tuple(
                    rule.rule_id for rule in request.constitutive_rules
                ),
                alternative_candidate_ids=tuple(
                    other for other in candidate_ids if other != candidate_id
                ),
                derivation=derive(
                    request.context,
                    "figurative synthesis under objective unity"
                    if self.include_objective_unity
                    else "recognize complete identity paths",
                    (
                        ground(retained_id, GroundKind.RETAINED_SEQUENCE),
                        *(
                            rule_ground(rule)
                            for rule in request.identity_rules
                            + request.constitutive_rules
                        ),
                    ),
                    tuple(other for other in candidate_ids if other != candidate_id),
                ),
            )
            for candidate_id, path in zip(candidate_ids, paths, strict=True)
        )


@dataclass(frozen=True)
class FigurativeRequest:
    retention: RetentionRequest
    identity_rules: tuple[Rule, ...]
    constitutive_rules: tuple[Rule, ...]


@dataclass(frozen=True)
class SynthesisBundle:
    retention: RetentionResult
    recognition: RecognitionResult | None


class FigurativeSynthesis(Protocol):
    def __call__(
        self, request: FigurativeRequest, provenance: ProvenanceView, /
    ) -> SynthesisBundle: ...


@dataclass(frozen=True)
class FigurativePolicy:
    """One operation jointly reproduces and forms candidates under unity rules."""

    retain: RetainIntuitions = retain_episode
    path_budget: int = 4096

    def __call__(
        self, request: FigurativeRequest, provenance: ProvenanceView, /
    ) -> SynthesisBundle:
        retained = self.retain(request.retention)
        if isinstance(retained, SynthesisFailed):
            return SynthesisBundle(retention=retained, recognition=None)
        recognition = EnumerateCandidates(
            self.path_budget, include_objective_unity=True
        )(
            RecognitionRequest(
                retained_sequence=retained,
                identity_rules=request.identity_rules,
                constitutive_rules=request.constitutive_rules,
                policy=SynthesisPolicy.B_LED_FIGURATIVE,
                context=request.retention.context,
            ),
            provenance,
        )
        return SynthesisBundle(retention=retained, recognition=recognition)
