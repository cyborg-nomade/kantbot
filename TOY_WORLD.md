# Deterministic Strip World

## Run an observation replay

From the repository checkout:

```text
uv sync --locked --all-groups
uv run python -m kantbot.worlds --list
uv run python -m kantbot.worlds rightward
```

The last command prints a version-1 JSON observation sequence. It does not run
synthesis, apply a concept, or print a judgment. Its three observations supply
amber patches at `(t, x) = (0, 0), (1, 1), (2, 2)`, using the canonical
observation fields, including source and quality.

This is the final [Phase 2 deliverable](ROADMAP.md#phase-2--define-an-executable-formal-model).
Its sensor boundary is governed by
[accepted ADR 0008](docs/decisions/0008-deterministic-strip-sensor.md). Complete
cognitive-role implementations remain Phase 3 work.

## World, sensor, and cognition

**Engineering.** [`kantbot.worlds`](src/kantbot/worlds/__init__.py) lives outside
the canonical cognitive model. Its values are strict and recursively immutable
under [ADR 0006](docs/decisions/0006-canonical-model-representation.md).

```text
StripWorld: ordered snapshots with experimenter marker IDs
    |                               |
    | observe_world                 | evaluator_references
    v                               v
ObservationSequence             EvaluatorReference tuple
    |                               |
    v                               v
reception -> variant projection  external evaluation only
    |
    v
manifold -> synthesis -> object licensing -> schema -> judgment
           (cognitive-role implementations are Phase 3 work)
```

A `StripWorld` contains a public episode ID and nonempty, strictly ordered
`StripFrame` snapshots. Each frame has an integer temporal position, a
readability flag, and zero or more `MarkerState` values. A marker has a hidden
identity, a color string, and an integer strip coordinate. One identity cannot
occupy two marker records within one frame. Frames may contain gaps, arrivals,
departures, color changes, or arbitrary displacement: no physical law or
cognitive identity constraint is built into the world script.

`observe_world` applies the fixed `strip-patch-camera-v1` sensor:

- A readable frame yields one observation per distinct `(x, color)` pair,
  ordered by coordinate and then color. Each supplies exactly `color` and `x`.
- Coincident same-color markers produce one indistinguishable patch; hidden
  multiplicity cannot leak through sample count. Different colors at the same
  coordinate remain distinct samples. This symbolic sensor is not an optical
  rendering or occlusion model.
- Simultaneous patches share the frame's temporal position but have distinct
  observation IDs. Within-frame ordering is serialization order, not temporal
  succession or a candidate-identity preference.
- An empty readable frame yields one complete record with
  `patch-present: false`. An unreadable frame yields one impaired record with
  `frame-readable: false`, regardless of hidden marker count or content.
  Neither supplies invented color or coordinate content; neither disappears.

The sensor supplies instantaneous segmentation, not persistence. This is a
deliberate simplification relative to raw perception and the illustrative
frame-level format in [Worked Example Trace 3](WORKED_EXAMPLES.md#trace-3).
The current [field projection](SENSIBLE_PROCEDURES.md#inputs-and-receptive-admission)
can select scalar fields but cannot split a structured frame into several
intuitions. The accepted boundary exposes that limitation instead of silently adding
segmentation to projection. A supplied patch is still an
[observation](GLOSSARY.md#observation), not an intuition or licensed object.

## Reproducibility and isolation

Observation IDs are `strip-observation:<episode>:<position>:<slot>`. Slots are
local to one frame and computed from visible pairs, never hidden marker IDs,
storage order, or an earlier frame. Slot zero at two times does not mean the
same object. Appending future snapshots cannot change already emitted samples.

Repeated export yields the same observations and JSON bytes within this version
and the locked environment. There is no seed, clock, network, UUID, mutable
generator, or ambient state. Both world scripts and observation envelopes
support strict JSON round-trips; unknown versions are rejected. This format is
separate from [version-2 cognitive provenance](STRUCTURED_PROVENANCE.md).

Built-in scripts share public episode ID `strip-demo`, so controlled contrasts
preserve input IDs where position and slot agree. Compare them as separate
runs. Give independently combined episodes distinct IDs. A scenario's display
name and any expected result are absent from the sensor export.

`StripWorld.evaluator_references()` exports a separate typed tuple with IDs
`strip-evaluator:<episode>:<marker>`. The snapshots themselves remain external
evaluator data. Neither those references nor snapshots are fields of
`ObservationSequence`, `Observation`, or `ReceptionRequest`. The CLI exports
only observations. A replay driver must give a cycle only the observations
admitted for that cycle, not the script or unadmitted future observations.

This is an API and provenance boundary, not an operating-system sandbox. A
caller with the world value can inspect it. Cognitive code must not accept that
capability; the graph validator rejects promotion of registered evaluator
references into cognitive grounds. Hidden simulation state is not a noumenal
realm or a privileged cognition of things in themselves ([K-014](CLAIMS.md#k-014)).

## Scenario catalog

These names identify input fixtures, not promises of terminal outcomes.

| Name | Supplied variation | Intended comparison |
| --- | --- | --- |
| `rightward` | Amber at `x = 0, 1, 2` | [Trace 1](WORKED_EXAMPLES.md#trace-1), positive motion control |
| `stationary` | Amber at `x = 2, 2, 2` | [Trace 4](WORKED_EXAMPLES.md#trace-4), identity versus predication |
| `reordered-motion` | Amber at `x = 0, 2, 1`, still in temporal order | [BP-001](BEHAVIORAL_PREDICTIONS.md#bp-001), order-sensitive applicability |
| `ambiguous-middle` | Amber at `x = 0`; then `1` and `2` simultaneously; then `3` | [Traces 3–6](WORKED_EXAMPLES.md#trace-3), rival identity paths |
| `short-interval` | Only two ordered samples, `x = 0, 1` | [BP-008](BEHAVIORAL_PREDICTIONS.md#bp-008), insufficient evidence for a three-sample schema |
| `unreadable-middle` | Readable endpoints with an unreadable middle frame | Missing presentation content, not a negative color or motion result |
| `broken-color` | Amber, blue, amber at `x = 0, 1, 2` | [Sensible contracts](SENSIBLE_PROCEDURES.md), identity check versus increase |
| `empty-middle` | Readable endpoints and a complete empty middle frame | Observed absence versus sensor impairment |

For programmatic use:

```python
from kantbot.worlds import ObservationSequence, load_scenario, observe_world

world = load_scenario("ambiguous-middle")  # external experiment setup
sequence = observe_world(world)
restored = ObservationSequence.model_validate_json(sequence.model_dump_json())
assert restored == sequence

for observation in restored.observations:
    print(observation.position, observation.content)

evaluator_only = world.evaluator_references()  # never a reception argument
```

## Verification and deliberate gaps

The [testing strategy](INVARIANTS_AND_PROPERTY_TESTS.md) is extended with:

| Layer | Checks | Test source |
| --- | --- | --- |
| Unit and generated properties | Scenario oracles; strict immutable values; order/episode validation; JSON replay; hidden renaming, permutation, and multiplicity invariance; future-prefix stability | [world tests](tests/test_toy_world.py) |
| Contract integration | Sensor observations in hand-authored presentation/manifold traces; graph validation; exact evidence from color-constancy and three-sample-increase checks; missing-field and evaluator-ground rejection | [provenance tests](tests/test_toy_world_provenance.py) |
| CLI smoke | Every scenario exports parsable JSON; unknown names fail; output bytes agree across processes with different hash seeds | [CLI tests](tests/test_toy_world_cli.py) |
| Static contract | Exports fit reception requests without world-state arguments | [type witness](typechecks/toy_world.py) |

The coverage target is every sensor branch and boundary validator, with explicit
negative cases, plus the full existing suite and unchanged CI/Sonar gates. Run:

```text
uv run pytest tests/test_toy_world.py tests/test_toy_world_provenance.py tests/test_toy_world_cli.py -W error
```

Then run the [complete quality checks](CONTRIBUTING.md#python-readability-and-static-analysis).

Integration scaffolding is intentionally test-only. It does not select an
identity branch, implement the examples' complete displacement rule `I-1`, infer
objecthood from color constancy, or commit judgments. Two samples can satisfy
constancy while the three-sample motion requirement remains undecided. A
manifold with simultaneous patches is valid, but testing all its members as one
successive path fails temporal ordering; synthesis must preserve alternatives.

The default patch projection cannot project empty/unreadable status records
into colored-patch intuitions. These remain valid shared input. Phase 3 must
record projection refusal or explicit alternative handling rather than silently
discard a frame. This package manufactures no cognitive terminal outcome;
complete episode-level cognition remains untested.
