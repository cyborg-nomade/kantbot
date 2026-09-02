"""Static witnesses that plain functions can satisfy every role contract."""

from kantbot.interfaces import (
    ApplicationRequest,
    ApplyConcept,
    CheckUnity,
    CommitJudgment,
    CommitmentRequest,
    CommitmentResult,
    ConstituteObject,
    CritiqueAndReport,
    FormManifold,
    ManifoldRequest,
    ObjectFormationRequest,
    ObjectFormationResult,
    PresentObservation,
    ProjectIntuition,
    ProjectionRequest,
    ProjectionResult,
    ProposalRequest,
    ProposalResult,
    ProposeJudgment,
    ProvenanceView,
    ReceptionRequest,
    RecognitionRequest,
    RecognitionResult,
    RecognizeCandidates,
    RetainIntuitions,
    RetentionRequest,
    RetentionResult,
    RoleContext,
    SupplyUnderstanding,
    UnderstandingRepertoire,
    UnityRequest,
    UnityResult,
)
from kantbot.model import (
    ApplicationResult,
    ConfigurationIdentity,
    ManifoldOfIntuition,
    PresentedElement,
    Scope,
    dump_terminal_outcome,
)
from kantbot.model.common import CognitiveGround, Identifier


class _Provenance:
    def resolves(self, ground: CognitiveGround, /) -> bool:
        raise NotImplementedError

    def immediate_grounds(
        self, entity_id: Identifier, /
    ) -> tuple[CognitiveGround, ...]:
        raise NotImplementedError

    def scope_for(self, entity_id: Identifier, /) -> Scope:
        raise NotImplementedError

    def configuration_for(self, entity_id: Identifier, /) -> ConfigurationIdentity:
        raise NotImplementedError


def _present(request: ReceptionRequest, /) -> PresentedElement:
    raise NotImplementedError


def _project(request: ProjectionRequest, /) -> ProjectionResult:
    raise NotImplementedError


def _form_manifold(request: ManifoldRequest, /) -> ManifoldOfIntuition:
    raise NotImplementedError


def _supply_understanding(context: RoleContext, /) -> UnderstandingRepertoire:
    raise NotImplementedError


def _retain(request: RetentionRequest, /) -> RetentionResult:
    raise NotImplementedError


def _recognize(
    request: RecognitionRequest,
    provenance: ProvenanceView,
    /,
) -> RecognitionResult:
    raise NotImplementedError


def _constitute(
    request: ObjectFormationRequest,
    provenance: ProvenanceView,
    /,
) -> ObjectFormationResult:
    raise NotImplementedError


def _apply(
    request: ApplicationRequest,
    provenance: ProvenanceView,
    /,
) -> ApplicationResult:
    raise NotImplementedError


def _propose(request: ProposalRequest, /) -> ProposalResult:
    raise NotImplementedError


def _check_unity(
    request: UnityRequest,
    provenance: ProvenanceView,
    /,
) -> UnityResult:
    raise NotImplementedError


def _commit(request: CommitmentRequest, /) -> CommitmentResult:
    raise NotImplementedError


provenance: ProvenanceView = _Provenance()
present: PresentObservation = _present
project: ProjectIntuition = _project
form_manifold: FormManifold = _form_manifold
supply_understanding: SupplyUnderstanding = _supply_understanding
retain: RetainIntuitions = _retain
recognize: RecognizeCandidates = _recognize
constitute: ConstituteObject = _constitute
apply_concept: ApplyConcept = _apply
propose: ProposeJudgment = _propose
check_unity: CheckUnity = _check_unity
commit: CommitJudgment = _commit
report: CritiqueAndReport = dump_terminal_outcome
