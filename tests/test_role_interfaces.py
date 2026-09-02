"""Runtime invariants at the understanding-to-role boundary."""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from kantbot.interfaces import UnderstandingRepertoire
from kantbot.model import (
    Condition,
    Rule,
    RuleAuthority,
    Schema,
    Scope,
)


def _rule(
    scope: Scope,
    *,
    rule_id: str = "U-1",
    authority: RuleAuthority = RuleAuthority.CONSTITUTIVE,
) -> Rule:
    return Rule(
        rule_id=rule_id,
        name="candidate unity",
        description="one compatible identity branch forms a candidate",
        authority=authority,
        scope=scope,
    )


def test_understanding_supplies_one_validated_repertoire(
    successful_trace: SimpleNamespace,
) -> None:
    repertoire = UnderstandingRepertoire(
        rules=(_rule(successful_trace.scope),),
        concepts=(successful_trace.concept,),
        schemas=(successful_trace.schema,),
        scope=successful_trace.scope,
        configuration=successful_trace.configuration,
    )

    assert repertoire.schemas[0].concept_id == repertoire.concepts[0].concept_id
    with pytest.raises(ValidationError, match="frozen"):
        repertoire.rules = ()


def test_understanding_rejects_regulative_object_level_resources(
    successful_trace: SimpleNamespace,
) -> None:
    with pytest.raises(ValidationError, match="must be constitutive"):
        UnderstandingRepertoire(
            rules=(
                _rule(
                    successful_trace.scope,
                    authority=RuleAuthority.REGULATIVE,
                ),
            ),
            concepts=(successful_trace.concept,),
            schemas=(successful_trace.schema,),
            scope=successful_trace.scope,
            configuration=successful_trace.configuration,
        )


def test_understanding_rejects_schema_for_an_unavailable_concept(
    successful_trace: SimpleNamespace,
) -> None:
    foreign_schema = Schema(
        schema_id="S-foreign",
        concept_id="foreign-concept",
        name="foreign schema",
        procedure="a procedure whose concept is absent",
        condition_ids=("foreign-condition",),
        sensible_form_ids=("time-total",),
        scope=successful_trace.scope,
        authority=RuleAuthority.CONSTITUTIVE,
    )

    with pytest.raises(ValidationError, match="unavailable concept"):
        UnderstandingRepertoire(
            rules=(_rule(successful_trace.scope),),
            concepts=(successful_trace.concept,),
            schemas=(foreign_schema,),
            scope=successful_trace.scope,
            configuration=successful_trace.configuration,
        )


def test_understanding_rejects_schema_conditions_absent_from_its_concept(
    successful_trace: SimpleNamespace,
) -> None:
    unknown_condition = Condition(
        condition_id="unknown-condition",
        description="not declared by the concept",
        required=True,
        authority=RuleAuthority.CONSTITUTIVE,
    )
    schema = Schema(
        schema_id="S-unknown-condition",
        concept_id=successful_trace.concept.concept_id,
        name="invalid condition schema",
        procedure="attempt to use an undeclared condition",
        condition_ids=(unknown_condition.condition_id,),
        sensible_form_ids=("time-total",),
        scope=successful_trace.scope,
        authority=RuleAuthority.CONSTITUTIVE,
    )

    with pytest.raises(ValidationError, match="unavailable conditions"):
        UnderstandingRepertoire(
            rules=(_rule(successful_trace.scope),),
            concepts=(successful_trace.concept,),
            schemas=(schema,),
            scope=successful_trace.scope,
            configuration=successful_trace.configuration,
        )


def test_understanding_rejects_resources_from_another_scope(
    successful_trace: SimpleNamespace,
) -> None:
    other_scope = successful_trace.scope.model_copy(update={"scope_id": "other-scope"})

    with pytest.raises(ValidationError, match="share one cycle scope"):
        UnderstandingRepertoire(
            rules=(_rule(other_scope),),
            concepts=(successful_trace.concept,),
            schemas=(successful_trace.schema,),
            scope=successful_trace.scope,
            configuration=successful_trace.configuration,
        )
