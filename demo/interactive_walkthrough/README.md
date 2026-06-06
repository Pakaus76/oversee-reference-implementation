# OVERSEE Interactive Walkthrough

This folder contains an isolated demonstration layer for explaining the OVERSEE architecture step by step.

## Purpose

The walkthrough is designed for live explanation. It helps a reviewer understand how the architecture in Figure 3 works:

1. Enterprise sources provide information through an API access layer.
2. Layer 1 produces a validated evidence package.
3. Layer 2 produces a contextualized decision profile.
4. Layer 3 produces a decision-ready case state.
5. Layer 4 produces a decision evaluation and recommendation record.
6. Layer 5 produces a governed recommendation package.

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

## Current usage

List available scenarios:

```powershell
python scripts\run_interactive_oversee_demo.py --list-scenarios
```

Run the default paper-aligned case with pauses:

```powershell
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
```

Run without pauses:

```powershell
python scripts\run_interactive_oversee_demo.py --scenario COMP-001 --no-pause
```

Run and show all copied artifacts:

```powershell
python scripts\run_interactive_oversee_demo.py --scenario COMP-001 --no-pause --show-artifacts
```

Run an alternative scenario in presentation mode:

```powershell
python scripts\run_interactive_oversee_demo.py --scenario COMP-002 --no-pause
```

## Current integration status

- Layers 1 to 5 are connected to the existing paper-aligned execution scripts for `COMP-001`.
- Alternative scenarios currently run in presentation mode.
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

## Current scenarios

- `COMP-001`: paper-aligned compressor case.
- `COMP-002`: lower-urgency compressor case.
- `PUMP-001`: resource-constrained pump case.
