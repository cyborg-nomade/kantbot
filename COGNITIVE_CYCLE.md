# Executable Cognitive Cycle

## Run the library

The first Phase 3 deliverable implements the cycle as a library in
[`kantbot.cycle`](src/kantbot/cycle/__init__.py). It composes the accepted
[role interfaces](ROLE_INTERFACES.md), [checked transitions](STATE_TRANSITION_MODEL.md),
and [replayable provenance](STRUCTURED_PROVENANCE.md). Its bounded execution
choices are proposed for review in
[ADR 0009](docs/decisions/0009-bounded-policy-cycle.md).

```python
from kantbot.cycle import run_cycle, strip_plan
from kantbot.worlds import load_scenario, observe_world

observations = observe_world(load_scenario("rightward"))
execution = run_cycle(observations.observations, strip_plan(observations.episode_id))
assert execution.outcomes[0].kind.value == "judgment-committed"
assert execution.trace.judgments[0].warrant.unity_check.passed
```

The world and sensor remain external. `run_cycle` receives only the admitted
observation tuple and a frozen plan. The world name, hidden marker identities,
evaluator references, and unadmitted future snapshots are absent from its inputs.
The existing `python -m kantbot.worlds` command still exports observations only.
The cycle CLI and dedicated human-readable trace presentation remain separate
Roadmap deliverables.

## Operations and ownership

**Engineering.** Domain representations remain strict immutable values under
[ADR 0006](docs/decisions/0006-canonical-model-representation.md). Each role
callable takes explicit requests and returns new values. The runner constructs
and validates a new graph prefix after each stage; earlier prefixes and the
supplied observations remain unchanged.

```text
observations + frozen plan
    -> shared presentation -> declared projection -> manifold
    -> licensed retention -> all admissible identity paths
    -> object licenses -> schema results -> proposal
    -> common unity checks + selected policy -> commitment -> critique
```

| Component | Mechanical work | Ownership |
| --- | --- | --- |
| `strip_understanding` | Supplies general rules, a concept, and its schema without seeing observations | Understanding |
| `present_observation`, `project_intuition`, `form_manifold` | Preserve input, replay field selection under form, record refusal or a formed plurality | Shared reception and sensibility |
| `retain_episode`, `EnumerateCandidates` | Reproduce earlier intuitions under `R-1`; enumerate complete paths using actual sensible content | Imagination under supplied rules |
| `constitute_object` | Recompute identity and constitutive conditions before objecthood | Object gate |
| `apply_concept` | Run the selected schema, keeping failed and undecided conditions | Power of judgment |
| `propose_judgment` | Assemble the proposition with its actual observation, projection, synthesis, and rule grounds | Proposal gate |
| `check_unity` | Traverse complete ancestry, check rival identities, authorities, context, forms, warrant coverage, and modality | Apperception |
| `commit_judgment` | Construct a commitment after unity; graph certification and checked transitions still govern admission | Commitment gate |
| `critique_and_report` | Expose the typed result using the existing outcome codec | Critique |

`CycleExecution` returns a validated `graph`, canonical `trace`, terminal
`outcomes` and `terminal_states`, executed `operations`, and reports from the
selected critique callable. Its terminal paths must match the graph's certified
outcomes. Multiple terminal paths preserve branch-specific failures together
with any stronger result reached elsewhere.

Input shape, episode, duplicate-identity, and ordering errors return
`input-error` before reception. Incoherent role implementations raise validation
or transition errors. They do not become philosophical refusals. A valid failed
or underdetermined procedure instead produces the corresponding typed limit.

## Frozen plan and replaceable policies

`CyclePlan` holds the scope, configuration identity, forms, projection,
understanding repertoire, selected retention/identity/constitutive rules,
target concept and schema, synthesis variant, ambiguity treatment, and execution
budgets. Form definitions and their availability to this episode are separate:
`available_form_ids=None` preserves the original request contract that all
required forms are available. An explicit subset restricts projection. For
example, `strip_plan(episode_id, available_form_ids=("strip-space",))` preserves
shared reception but refuses temporal intuition. The runner checks this
availability around replacement projectors too. Each cycle tests one declared
predicate. A different concept/schema can be supplied through the same plan
contract.

`CyclePolicies` provides the concrete callable implementations. For example,
this ablation removes access to earlier moments while keeping the observations:

```python
from kantbot.cycle import CyclePolicies, retain_current

ablated = run_cycle(
    observations.observations,
    strip_plan(observations.episode_id, experiment_id="retention-disabled"),
    policies=CyclePolicies(retain=retain_current),
)
assert ablated.outcomes[0].kind.value == "synthesis-failed"
```

Earlier samples must be marked `reproduced`, with the plan's retention rule;
only the final admitted moment is current, and all presentations at that moment
must remain available. Recognition reads the retained IDs
through `ProvenanceView`, rather than falling back to the raw batch. Changing
retention therefore changes the material available for identity formation.

Replacement roles preserve the common contracts: reception and application are
graph-validated, candidate completeness is checked within the declared bounded
path domain, and common unity checks run before an additional unity policy.
Additional successful unity conditions remain in the committed warrant. An
experimental policy can impose further constraints, while changing a common
licensing requirement calls for an explicit new decision and model revision.
These are ordinary Python callables, not code imported from a serialized trace.
Experiments must name their changed policies and revise configuration identity
when a configuration changes; the identity field is not a hash of Python code.
The strip preset accepts `experiment_id` for this purpose.

## Two synthesis variants

The default implements [ADR 0002](docs/decisions/0002-a-b-synthesis.md) with
distinct apprehension, reproduction, and recognition operations. It traverses
the declared manifold, retains earlier moments, and recognizes paths under
identity conditions; the object gate then tests constitutive unity.

The B-led variant calls one `FigurativePolicy`. This operation jointly retains
the sensible sequence and checks both identity and objective-unity rules while
forming candidates. Its canonical retained sequence and candidates still carry
all evidence, but its execution history has one figurative-synthesis operation.
The final unity gate applies to both variants.

```python
from kantbot.model import SynthesisPolicy

b_led = run_cycle(
    observations.observations,
    strip_plan(
        observations.episode_id,
        synthesis_policy=SynthesisPolicy.B_LED_FIGURATIVE,
    ),
)
```

The difference has mechanical consequences. If a declared constitutive
condition requires a fourth sample, a three-sample A-led run can retain its
recognized candidate and fail object formation. The B-led operation rejects that
combination during formation. Both refuse commitment and preserve their
respective strongest representations. Neither variant survives removal of
licensed reproduction by reading earlier raw observations directly.

## The initial strip interpretation

**Engineering.** A path selects one intuition per retained temporal moment
across the whole available interval. Recognition tests every combination within
the declared budget and preserves all admitted rivals. These are candidate
identity paths, not tracks supplied by the sensor. This experiment does not
infer births, deaths, maximal subintervals, or occluded trajectories.

`I-1` uses `FieldConstant(color)` and the new `BoundedDisplacement(x)` instruction:
absolute coordinate change must be at most two units times elapsed temporal
ticks. Both temporal and spatial forms must be registered and available to the
selected intuitions. At least two samples are required. Missing fields,
nonnumeric values, or absent spatial form leave this check undecided; an
observed excessive displacement fails it. Exact rational arithmetic avoids
overflow when comparing finite numeric inputs. `U-1` requires distinct ordered
moments. These operational constraints make no claim to exhaust substance or
causality.

The empirical `moving-right` schema independently requires at least three
samples with strictly increasing `x`. A stationary candidate therefore passes
object formation and fails this predicate. A two-sample candidate can pass
object formation while its application remains underdetermined.

The default ambiguity policy stops with `synthesis-ambiguous`. To continue the
branches through object formation and application:

```python
from kantbot.cycle import AmbiguityPolicy

rivals = observe_world(load_scenario("ambiguous-middle"))
continued = run_cycle(
    rivals.observations,
    strip_plan(rivals.episode_id, ambiguity_policy=AmbiguityPolicy.CONTINUE),
)
assert continued.outcomes[0].kind.value == "judgment-withheld"
```

Successful application on both branches does not choose one singular subject.
Even one applicable branch among several licensed objects cannot win merely
because its predicate passed. Candidate and application alternatives remain
explicit. Non-constitutive rules can be registered as reserved metadata;
promoting them into a proposed warrant produces `overreach` at unity.

Empty and unreadable frames remain received records. Missing patch fields
produce explicit projection refusals; other successful projections remain in
the trace. This first implementation stops the episode before synthesis when
any presentation cannot enter the configured patch projection. Continuing
unaffected paths or inferring hidden content would require an explicit revised
projection/branching contract.

## Verification, budgets, and limits

The default plan permits 64 observations and 256 possible identity combinations.
It checks the complete combination count before searching; it never truncates
alternatives to fit a budget. Exceeding either budget raises
`SearchCapacityExceeded`, an engineering limit rather than `synthesis-failed`.
Budgets can be changed explicitly on a validated plan. Rebuilding graphs and
preserving mutual alternative links can be quadratic; larger experiments should
revisit representation and execution costs before increasing these bounds.

The tests necessary to validate this library item cover:

- all eight sensor episodes under both synthesis variants, with repeatable
  complete graphs and warrants;
- retention ablation, rival continuation, failed identity, failed and undecided
  application, merged identities, missing warrant roles, and excessive modality;
- regulative metadata invariance and rejection of illicit promotion;
- forged reception/application results, hidden-world input rejection, and
  replacement policies that erase alternatives or reinterpret earlier samples;
- an independent arithmetic oracle for displacement, spatial-form failures,
  exact evidence, and imported-license replay; and
- static compatibility with the accepted callable protocols.

See [cycle tests](tests/test_cognitive_cycle.py),
[policy tests](tests/test_cycle_policies.py),
[displacement tests](tests/test_displacement.py), and
[static witnesses](typechecks/cognitive_cycle.py). Run the full
[quality suite](CONTRIBUTING.md#python-readability-and-static-analysis).

The new instruction extends the version-2 procedure vocabulary additively.
Existing version-2 traces retain their meaning; older readers reject the new
operation when encountered. No callable is deserialized. Graph replay certifies
agreement with declared instructions, while the executed role and policy tests
assess the additional library behavior. Philosophical adequacy and comparisons
with alternative accounts still require the later evaluation phase.
