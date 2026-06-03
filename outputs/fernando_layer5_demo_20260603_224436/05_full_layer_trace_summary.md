# Fernando full five-layer OVERSEE trace summary

## Layer 1 - Integration, aggregation and validation

- Receives a predictive alert through a simulated API endpoint.
- Receives raw sensor context together with the alert.
- Calls simulated enterprise APIs for asset metadata, CMMS history, MES context, inventory/resources and policy governance.
- Evidence package valid: True

## Layer 2 - DMN-like contextualization

- Applies explicit if-then rules to derive contextual decision factors.
- Layer 2 ready: True
- Derived technical urgency: high

## Layer 3 - CMMN-inspired lifecycle

- Lifecycle stage: decision_ready
- Decision ready: True

## Layer 4 - Decision and recommendation logic

- Final priority: high
- Recommended execution mode: controlled_planning
- Recommendation path count: 2
- Live generative model call successful: True
- Priority alignment: True
- Action alignment: different

## Layer 5 - Governed package

- Package ID: governed_package_FERNANDO_ALERT-COMP-001-20260603
- Traceability count: 6
- Final output is a governed package, not an uncontrolled model answer.
