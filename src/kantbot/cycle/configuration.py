"""Frozen cycle resources and the bounded strip experiment's repertoire."""

from enum import StrEnum
from typing import Annotated, Self

from pydantic import Field, model_validator

from kantbot.interfaces import RoleContext, UnderstandingRepertoire
from kantbot.model import (
    BoundedDisplacement,
    Concept,
    ConceptKind,
    Condition,
    ConfigurationIdentity,
    FieldConstant,
    FieldProjection,
    Form,
    FormKind,
    Rule,
    RuleAuthority,
    RuleKind,
    Schema,
    Scope,
    SemanticModel,
    SensibleProcedure,
    StrictIncrease,
    SynthesisPolicy,
    TemporalOrder,
    VariantProjection,
)
from kantbot.model.common import Identifier, require_unique


class AmbiguityPolicy(StrEnum):
    STOP = "stop-at-synthesis"
    CONTINUE = "continue-branches"


class CyclePlan(SemanticModel):
    """One frozen experiment: resources, selected predicate, and search bound."""

    cycle_id: Identifier
    context: RoleContext
    forms: tuple[Form, ...] = Field(min_length=1)
    available_form_ids: tuple[Identifier, ...] | None = None
    projection: VariantProjection
    repertoire: UnderstandingRepertoire
    reserved_rules: tuple[Rule, ...] = ()
    retention_rule_id: Identifier
    identity_rule_ids: tuple[Identifier, ...] = Field(min_length=1)
    constitutive_rule_ids: tuple[Identifier, ...] = Field(min_length=1)
    concept_id: Identifier
    schema_id: Identifier
    synthesis_policy: SynthesisPolicy = SynthesisPolicy.A_ANALYSIS_B_CONSTRAINT
    ambiguity_policy: AmbiguityPolicy = AmbiguityPolicy.STOP
    path_budget: Annotated[int, Field(ge=1)] = 256
    observation_budget: Annotated[int, Field(ge=1)] = 64

    @model_validator(mode="after")
    def resources_match_the_plan(self) -> Self:
        if (
            self.repertoire.scope != self.context.scope
            or self.repertoire.configuration != self.context.configuration
            or self.projection.variant_id != self.context.configuration.variant_id
        ):
            raise ValueError("plan resources must share its frozen context")
        require_unique(tuple(form.form_id for form in self.forms), "plan form IDs")
        forms = {form.form_id: form for form in self.forms}
        if self.available_form_ids is not None:
            require_unique(self.available_form_ids, "available form IDs")
            if not set(self.available_form_ids) <= forms.keys():
                raise ValueError("available forms must be registered definitions")
        if any(
            forms.get(form.form_id) != form for form in self.projection.required_forms
        ):
            raise ValueError("projection forms must be registered exactly")
        require_unique(
            tuple(rule.rule_id for rule in self.repertoire.rules + self.reserved_rules),
            "available rule IDs",
        )
        if any(
            rule.scope != self.context.scope
            or rule.authority is RuleAuthority.CONSTITUTIVE
            for rule in self.reserved_rules
        ):
            raise ValueError("reserved rules must be scoped non-constitutive metadata")
        return self

    @model_validator(mode="after")
    def selected_rules_match_roles(self) -> Self:
        require_unique(self.identity_rule_ids + self.constitutive_rule_ids, "rule IDs")
        rules = {rule.rule_id: rule for rule in self.repertoire.rules}
        if self.retention_rule_id not in rules:
            raise ValueError("retention rule is unavailable")
        if rules[self.retention_rule_id].kind is not RuleKind.GENERAL:
            raise ValueError(
                "retention must select a general rule, not an object license"
            )
        for ids, kind in (
            (self.identity_rule_ids, RuleKind.IDENTITY),
            (self.constitutive_rule_ids, RuleKind.CATEGORY_INSPIRED),
        ):
            for rule_id in ids:
                if rule_id not in rules or rules[rule_id].kind is not kind:
                    raise ValueError("selected rule is absent or has the wrong role")
        conditions = tuple(
            condition.condition_id
            for rule_id in self.identity_rule_ids + self.constitutive_rule_ids
            for condition in rules[rule_id].conditions
        )
        require_unique(conditions, "selected object condition IDs")
        if not any(
            concept.concept_id == self.concept_id
            for concept in self.repertoire.concepts
        ):
            raise ValueError("selected concept is unavailable")
        if not any(
            schema.schema_id == self.schema_id and schema.concept_id == self.concept_id
            for schema in self.repertoire.schemas
        ):
            raise ValueError("selected schema is unavailable for this concept")
        return self


def _condition(condition_id: str, description: str) -> Condition:
    return Condition(
        condition_id=condition_id,
        description=description,
        required=True,
        authority=RuleAuthority.CONSTITUTIVE,
    )


def strip_understanding(context: RoleContext, /) -> UnderstandingRepertoire:
    """Supply general strip rules and a concept without inspecting observations."""

    authority = RuleAuthority.CONSTITUTIVE
    retention = Rule(
        rule_id="R-1",
        name="episode retention",
        description="Reproduce earlier episode intuitions",
        authority=authority,
        scope=context.scope,
    )
    identity_conditions = (
        _condition("I-color", "Color remains constant across the path"),
        _condition(
            "I-displacement", "Displacement is at most two strip units per tick"
        ),
    )
    identity = Rule(
        rule_id="I-1",
        name="strip identity",
        description="Same color, bounded displacement",
        kind=RuleKind.IDENTITY,
        authority=authority,
        scope=context.scope,
        conditions=identity_conditions,
        sensible_procedure=SensibleProcedure(
            temporal_form_id="strip-time",
            checks=(
                FieldConstant(condition_id="I-color", field="color"),
                BoundedDisplacement(
                    condition_id="I-displacement",
                    field="x",
                    spatial_form_id="strip-space",
                    maximum_per_tick=2,
                ),
            ),
        ),
    )
    unity = Rule(
        rule_id="U-1",
        name="local successive unity",
        description="One selected sample at each successive moment",
        kind=RuleKind.CATEGORY_INSPIRED,
        authority=authority,
        scope=context.scope,
        conditions=(
            _condition(
                "U-successive", "Selected samples occupy distinct ordered moments"
            ),
        ),
        sensible_procedure=SensibleProcedure(
            temporal_form_id="strip-time",
            checks=(TemporalOrder(condition_id="U-successive"),),
        ),
    )
    concept = Concept(
        concept_id="moving-right",
        name="moving right",
        kind=ConceptKind.EMPIRICAL,
        applicability_conditions=(
            _condition("S-right-increase", "x increases across at least three samples"),
        ),
        scope=context.scope,
        authority=authority,
    )
    schema = Schema(
        schema_id="S-right",
        concept_id=concept.concept_id,
        name="successive rightward motion",
        procedure=SensibleProcedure(
            temporal_form_id="strip-time",
            checks=(
                StrictIncrease(
                    condition_id="S-right-increase", field="x", minimum_samples=3
                ),
            ),
        ),
        condition_ids=("S-right-increase",),
        sensible_form_ids=("strip-time", "strip-space"),
        scope=context.scope,
        authority=authority,
    )
    return UnderstandingRepertoire(
        rules=(retention, identity, unity),
        concepts=(concept,),
        schemas=(schema,),
        scope=context.scope,
        configuration=context.configuration,
    )


def strip_plan(
    episode_id: str,
    *,
    synthesis_policy: SynthesisPolicy = SynthesisPolicy.A_ANALYSIS_B_CONSTRAINT,
    ambiguity_policy: AmbiguityPolicy = AmbiguityPolicy.STOP,
    available_form_ids: tuple[str, ...] | None = None,
    experiment_id: str = "default",
) -> CyclePlan:
    """Declare the worked examples' bounded experiment independently of a world."""

    availability = "all"
    if available_form_ids is not None:
        availability = ".".join(sorted(available_form_ids)) or "none"
    context = RoleContext(
        scope=Scope(
            scope_id=f"scope:{episode_id}",
            episode_id=episode_id,
            description="Supplied strip episode only",
            presentation_conditions=("total temporal order", "one dimensional strip"),
            excluded_claims=("hidden marker identity", "future motion", "causality"),
        ),
        configuration=ConfigurationIdentity(
            configuration_id=(
                f"strip-config:{synthesis_policy.value}:"
                f"{ambiguity_policy.value}:forms:{availability}:{experiment_id}"
            ),
            variant_id=synthesis_policy.value,
        ),
    )
    forms = (
        Form(
            form_id="strip-time",
            kind=FormKind.TEMPORAL,
            description="Ordered episode positions",
        ),
        Form(
            form_id="strip-space",
            kind=FormKind.SPATIAL,
            description="Ordered strip coordinates",
        ),
    )
    projection = VariantProjection(
        projection_id="strip-projection",
        variant_id=context.configuration.variant_id,
        name="Supplied patch under temporal and spatial form",
        representation_kind="intuition",
        required_forms=forms,
        conditions=("singular", "preconceptual", "temporal-order"),
        procedure=FieldProjection(fields=("color", "x")),
    )
    return CyclePlan(
        cycle_id=f"cycle:{episode_id}",
        context=context,
        forms=forms,
        available_form_ids=available_form_ids,
        projection=projection,
        repertoire=strip_understanding(context),
        retention_rule_id="R-1",
        identity_rule_ids=("I-1",),
        constitutive_rule_ids=("U-1",),
        concept_id="moving-right",
        schema_id="S-right",
        synthesis_policy=synthesis_policy,
        ambiguity_policy=ambiguity_policy,
    )
