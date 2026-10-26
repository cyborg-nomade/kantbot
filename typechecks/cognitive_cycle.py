"""The production role functions satisfy the already accepted callable ports."""

from kantbot.cycle import CycleExecution, CyclePlan, run_cycle, strip_understanding
from kantbot.cycle.judgment import (
    apply_concept,
    commit_judgment,
    constitute_object,
    critique_and_report,
    propose_judgment,
)
from kantbot.cycle.reception import (
    form_manifold,
    present_observation,
    project_intuition,
)
from kantbot.cycle.synthesis import EnumerateCandidates, retain_episode
from kantbot.cycle.unity import check_unity
from kantbot.interfaces import (
    ApplyConcept,
    CheckUnity,
    CommitJudgment,
    ConstituteObject,
    CritiqueAndReport,
    FormManifold,
    PresentObservation,
    ProjectIntuition,
    ProposeJudgment,
    RecognizeCandidates,
    RetainIntuitions,
    SupplyUnderstanding,
)
from kantbot.model import Observation

present: PresentObservation = present_observation
project: ProjectIntuition = project_intuition
manifold: FormManifold = form_manifold
understanding: SupplyUnderstanding = strip_understanding
retain: RetainIntuitions = retain_episode
recognize: RecognizeCandidates = EnumerateCandidates()
constitute: ConstituteObject = constitute_object
apply: ApplyConcept = apply_concept
propose: ProposeJudgment = propose_judgment
unity: CheckUnity = check_unity
commit: CommitJudgment = commit_judgment
critique: CritiqueAndReport = critique_and_report


def execute(observations: tuple[Observation, ...], plan: CyclePlan) -> CycleExecution:
    return run_cycle(observations, plan)
