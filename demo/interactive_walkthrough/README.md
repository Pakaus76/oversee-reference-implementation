# OVERSEE Interactive Walkthrough

This folder contains an isolated demonstration layer for explaining the OVERSEE architecture step by step.

The walkthrough is designed for live explanation. It helps a reviewer understand how enterprise evidence becomes a governed recommendation package through the OVERSEE five-layer architecture.

---

## Purpose

The walkthrough follows this path:

```text
Enterprise sources
-> API access layer
-> Layer 1: validated evidence package
-> Layer 2: contextualized decision profile
-> Layer 3: case lifecycle state
-> Layer 4: decision evaluation and recommendation record
-> Layer 5: governed recommendation package
```

At v0.6.0, the walkthrough is connected to the executable multi-scenario all-layers runner. This means that executable scenarios are not presentation placeholders: they are executed through the real Layer 1 to Layer 5 path and then presented step by step.

---

## Boundary

This package is only a presentation layer. It must not be imported by `src/oversee`.

The dependency direction is:

```text
demo -> src/oversee
```

Never:

```text
src/oversee -> demo
```

If this folder is removed, the OVERSEE core should continue to work.

---

## Current usage

List available scenarios:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --list-scenarios
```

Run the default paper-aligned master case with pauses:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
```

Run without pauses:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario DATA-001 --no-pause
```

Run and show copied artifacts:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario SENSOR-001 --no-pause --show-artifacts
```

---

## Current integration status

At v0.6.0:

- All 20 scenarios contain `executable_inputs`.
- All 20 scenarios can execute through the real multi-scenario all-layers runner.
- The interactive walkthrough executes the selected scenario once and then presents the generated artifacts layer by layer.
- The demo remains isolated from `src/oversee`.

Generated artifacts are written to:

```text
outputs/interactive_demo_YYYYMMDD_HHMMSS/
```

Each run writes:

```text
demo_walkthrough_summary.md
demo_run_manifest.json
```

The full artifact list is hidden by default during the console walkthrough. Use `--show-artifacts` for expert inspection.

---

## Scenario groups

### Master cases

These are the preferred cases for manuals and guided explanation:

| Scenario | Purpose |
|---|---|
| `COMP-001` | Critical compressor risk with feasible controlled planning. |
| `COMP-002` | Early warning case where standard planning is enough. |
| `PUMP-001` | High-risk case constrained by missing resources. |
| `CONV-001` | Production-maintenance conflict case. |
| `DATA-001` | Evidence-quality stop case requiring diagnostic review. |

### Coverage cases

These broaden the industrial validation space:

```text
FAN-001
MOTOR-001
GEAR-001
ROBOT-001
CHILLER-001
BOILER-001
VALVE-001
AGV-001
PACK-001
CIP-001
HVAC-001
PUMP-002
COMP-003
SENSOR-001
MIXER-001
```

---

## Recommended walkthrough sequence

For a short reviewer-facing session:

1. `COMP-001`: show the normal high-value paper-aligned case.
2. `PUMP-001`: show that high risk may still be constrained by resources.
3. `DATA-001`: show that poor evidence triggers diagnostic review instead of blind execution.

For a deeper session:

1. `COMP-001`
2. `COMP-002`
3. `PUMP-001`
4. `CONV-001`
5. `DATA-001`

---

## Validation

Run the full test suite:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee -q
```

Expected at v0.6.0:

```text
88 passed
```
