# Informe en castellano de la estructura del proyecto OVERSEE

Generado: `2026-06-07 09:27:59`  
Rama Git: `main`  
Commit: `993a9d4`  
Tags en HEAD: `sin tag en HEAD`

## 1. Objetivo del informe

Este informe explica la estructura del repositorio OVERSEE carpeta por carpeta.

Su objetivo es ayudar a una persona que revisa la demo a entender:

- que hay dentro del repositorio;
- para que sirve cada carpeta;
- donde esta el codigo principal;
- donde estan los escenarios;
- donde estan los scripts de ejecucion;
- donde estan los tests;
- donde estan los manuales y reportes;
- como se relaciona todo con la demo ejecutable de OVERSEE.

El informe se basa en los ficheros versionados en Git mediante `git ls-files`. Por tanto, describe la estructura realmente versionada del repositorio, no carpetas temporales locales.

## 2. Lectura general del repositorio

El repositorio tiene cuatro bloques principales:

1. `src/oversee/`: el core de OVERSEE.
2. `demo/`: la capa de demostracion e interaccion.
3. `scripts/`: comandos ejecutables para correr escenarios y demos.
4. `tests/`: validacion automatizada.

Ademas, `docs/` contiene el material explicativo para la demo, incluyendo manuales, guias, resumenes y reportes.

La regla arquitectonica mas importante es:

```text
demo -> src/oversee
```

y nunca al reves:

```text
src/oversee -> demo
```

Esto significa que la demo puede usar el core, pero el core no debe depender de la demo.

## 3. Vision rapida de carpetas de primer nivel

| Carpeta | Funcion principal |
|---|---|
| `.github/` | Carpeta del proyecto. |
| `demo/` | Contiene elementos de demostracion. No debe ser dependencia del core. La direccion correcta es demo -> src/oversee. |
| `docs/` | Documentacion del proyecto, manuales, guias de demo, resumenes de release e informes. |
| `knowledge_base/` | Carpeta del proyecto. |
| `outputs/` | Carpeta de salidas generadas durante ejecuciones locales. Normalmente no debe versionarse salvo que haya una razon concreta. |
| `scripts/` | Scripts ejecutables desde consola. Incluye runners para ejecutar escenarios, demos y flujos completos. |
| `src/` | Carpeta principal de codigo fuente Python. |
| `tests/` | Suite de tests automatizados. |

Ficheros principales en la raiz:

- `.gitignore`
- `CHANGELOG.md`
- `README.md`
- `pyproject.toml`
- `requirements.txt`

## 4. Arbol resumido del repositorio versionado

El siguiente arbol usa solo caracteres ASCII para evitar problemas de codificacion en Windows o visores Markdown.

```text
.
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- demo/
|   |-- interactive_walkthrough/
|   |   |-- adapters/
|   |   |-- presenters/
|   |   |-- scenarios/
|   |   |-- DEMO_MANUAL.md
|   |   |-- README.md
|   |   |-- __init__.py
|   |   |-- demo_state.py
|   |   |-- display.py
|   |   |-- output_manager.py
|   |   |-- pause.py
|   |   |-- scenario_catalog.py
|   |   `-- walkthrough.py
|   `-- __init__.py
|-- docs/
|   |-- reports/
|   |   |-- v0_6_2_scenario_results_summary.csv
|   |   |-- v0_6_2_scenario_results_summary.json
|   |   `-- v0_6_2_scenario_results_summary.md
|   |-- advanced_workbench_demo_guide.md
|   |-- implementation_status.md
|   |-- master_cases_demo_guide.md
|   |-- master_cases_results_comparison.md
|   |-- oversee_architecture_comp001_deep_dive_manual.md
|   |-- oversee_architecture_comp001_deep_dive_manual.pdf
|   |-- paper_aligned_all_layers_demo_guide.md
|   |-- release_v0_6_1_summary.md
|   |-- reviewer_demo_walkthrough.md
|   `-- scenario_coverage_matrix.md
|-- knowledge_base/
|   `-- maintenance_guidance_seed.md
|-- outputs/
|   |-- deterministic_generative_comparison_20260602_171115/
|   |   |-- 01_digital_factory_scenarios.json
|   |   |-- 02_oversee_input_candidates.json
|   |   |-- 03_deterministic_anchor_results.json
|   |   |-- 04_live_generative_path_results.json
|   |   |-- 05_deterministic_generative_comparison.csv
|   |   |-- 05_deterministic_generative_comparison.json
|   |   |-- 06_comparison_summary.json
|   |   |-- 07_reviewer_summary.md
|   |   |-- 08_traceability_index.json
|   |   `-- 09_execution_manifest.json
|   |-- five_layer_layer1_layer2_20260602_234133/
|   |   |-- 01_external_source_payloads.json
|   |   `-- 02_canonical_case_context.json
|   |-- five_layer_layer3_case_lifecycle_20260602_235324/
|   |   |-- 01_external_source_payloads.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   `-- 03_case_management_state.json
|   |-- five_layer_layer4_decision_rules_20260603_000055/
|   |   |-- 01_external_source_payloads.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   |-- 04_dmn_decision_evaluation.json
|   |   `-- 04_recommendation_path_outputs.json
|   |-- five_layer_layer5_governed_package_20260603_000648/
|   |   |-- 01_external_source_payloads.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   |-- 04_dmn_decision_evaluation.json
|   |   |-- 04_recommendation_path_outputs.json
|   |   |-- 05_execution_manifest.json
|   |   |-- 05_governed_recommendation_package.json
|   |   |-- 05_reviewer_summary.md
|   |   `-- 05_traceability_index.json
|   |-- generative_digital_factory_workbench_20260603_173209/
|   |   |-- 00_generative_factory_parsed_sources.json
|   |   |-- 00_generative_factory_prompt.txt
|   |   |-- 00_generative_factory_raw_response.txt
|   |   |-- 00_generative_factory_result.json
|   |   |-- 01_external_source_payloads.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   |-- 04_deterministic_vs_generative_comparison.json
|   |   |-- 04_dmn_decision_evaluation.json
|   |   |-- 04_live_generative_recommendation.json
|   |   |-- 04_recommendation_path_outputs.json
|   |   |-- 05_execution_manifest.json
|   |   |-- 05_governed_recommendation_package.json
|   |   |-- 05_reviewer_summary.md
|   |   `-- 05_traceability_index.json
|   |-- live_generative_oversee_20260603_154534/
|   |   |-- 01_external_source_payloads.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   |-- 04_deterministic_vs_generative_comparison.json
|   |   |-- 04_dmn_decision_evaluation.json
|   |   |-- 04_live_generative_recommendation.json
|   |   |-- 04_recommendation_path_outputs.json
|   |   |-- 05_execution_manifest.json
|   |   |-- 05_governed_recommendation_package.json
|   |   |-- 05_reviewer_summary.md
|   |   `-- 05_traceability_index.json
|   |-- paper_aligned_all_layers_demo_20260603_225140/
|   |   |-- 00_predictive_alert_request.json
|   |   |-- 01_aggregated_evidence_package.json
|   |   |-- 01_enterprise_api_calls.json
|   |   |-- 01_received_predictive_alert.json
|   |   |-- 01_validation_report.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 02_context_enrichment_summary.md
|   |   |-- 02_contextualization_rule_trace.json
|   |   |-- 02_layer2_contextualization_result.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   |-- 03_layer3_case_lifecycle_summary.md
|   |   |-- 04_deterministic_vs_generative_comparison.json
|   |   |-- 04_dmn_decision_evaluation.json
|   |   |-- 04_layer4_decision_summary.md
|   |   |-- 04_live_generative_recommendation.json
|   |   |-- 04_recommendation_path_outputs.json
|   |   |-- 05_execution_manifest.json
|   |   |-- 05_full_layer_trace_summary.md
|   |   |-- 05_governed_recommendation_package.json
|   |   |-- 05_reviewer_summary.md
|   |   `-- 05_traceability_index.json
|   |-- paper_aligned_layer1_demo_20260603_220254/
|   |   |-- 00_predictive_alert_request.json
|   |   |-- 01_aggregated_evidence_package.json
|   |   |-- 01_enterprise_api_calls.json
|   |   |-- 01_received_predictive_alert.json
|   |   `-- 01_validation_report.json
|   |-- paper_aligned_layer2_demo_20260603_221341/
|   |   |-- 00_predictive_alert_request.json
|   |   |-- 01_aggregated_evidence_package.json
|   |   |-- 01_enterprise_api_calls.json
|   |   |-- 01_received_predictive_alert.json
|   |   |-- 01_validation_report.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 02_context_enrichment_summary.md
|   |   |-- 02_contextualization_rule_trace.json
|   |   `-- 02_layer2_contextualization_result.json
|   |-- paper_aligned_layer3_demo_20260603_221947/
|   |   |-- 00_predictive_alert_request.json
|   |   |-- 01_aggregated_evidence_package.json
|   |   |-- 01_enterprise_api_calls.json
|   |   |-- 01_received_predictive_alert.json
|   |   |-- 01_validation_report.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 02_context_enrichment_summary.md
|   |   |-- 02_contextualization_rule_trace.json
|   |   |-- 02_layer2_contextualization_result.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   `-- 03_layer3_case_lifecycle_summary.md
|   |-- paper_aligned_layer4_demo_20260603_223308/
|   |   |-- 00_predictive_alert_request.json
|   |   |-- 01_aggregated_evidence_package.json
|   |   |-- 01_enterprise_api_calls.json
|   |   |-- 01_received_predictive_alert.json
|   |   |-- 01_validation_report.json
|   |   |-- 02_canonical_case_context.json
|   |   |-- 02_context_enrichment_summary.md
|   |   |-- 02_contextualization_rule_trace.json
|   |   |-- 02_layer2_contextualization_result.json
|   |   |-- 03_case_lifecycle_trace.json
|   |   |-- 03_case_management_state.json
|   |   |-- 03_layer3_case_lifecycle_summary.md
|   |   |-- 04_deterministic_vs_generative_comparison.json
|   |   |-- 04_dmn_decision_evaluation.json
|   |   |-- 04_layer4_decision_summary.md
|   |   |-- 04_live_generative_recommendation.json
|   |   `-- 04_recommendation_path_outputs.json
|   `-- paper_aligned_layer5_demo_20260603_224436/
|       |-- 00_predictive_alert_request.json
|       |-- 01_aggregated_evidence_package.json
|       |-- 01_enterprise_api_calls.json
|       |-- 01_received_predictive_alert.json
|       |-- 01_validation_report.json
|       |-- 02_canonical_case_context.json
|       |-- 02_context_enrichment_summary.md
|       |-- 02_contextualization_rule_trace.json
|       |-- 02_layer2_contextualization_result.json
|       |-- 03_case_lifecycle_trace.json
|       |-- 03_case_management_state.json
|       |-- 03_layer3_case_lifecycle_summary.md
|       |-- 04_deterministic_vs_generative_comparison.json
|       |-- 04_dmn_decision_evaluation.json
|       |-- 04_layer4_decision_summary.md
|       |-- 04_live_generative_recommendation.json
|       |-- 04_recommendation_path_outputs.json
|       |-- 05_execution_manifest.json
|       |-- 05_full_layer_trace_summary.md
|       |-- 05_governed_recommendation_package.json
|       |-- 05_reviewer_summary.md
|       `-- 05_traceability_index.json
|-- scripts/
|   |-- run_deterministic_anchor_smoke.py
|   |-- run_deterministic_generative_comparison.py
|   |-- run_digital_factory_deterministic_anchor_smoke.py
|   |-- run_digital_factory_live_generative_path_offline_smoke.py
|   |-- run_generative_digital_factory_workbench_smoke.py
|   |-- run_interactive_oversee_demo.py
|   |-- run_layer1_layer2_compressor_smoke.py
|   |-- run_layer1_paper_aligned_demo.py
|   |-- run_layer2_paper_aligned_demo.py
|   |-- run_layer3_case_lifecycle_smoke.py
|   |-- run_layer3_paper_aligned_demo.py
|   |-- run_layer4_decision_rules_smoke.py
|   |-- run_layer4_paper_aligned_demo.py
|   |-- run_layer5_governed_package_smoke.py
|   |-- run_layer5_paper_aligned_demo.py
|   |-- run_live_generative_oversee_smoke.py
|   |-- run_live_generative_path_offline_smoke.py
|   |-- run_oversee_reviewer_demo.py
|   |-- run_paper_aligned_all_layers_demo.py
|   `-- run_scenario_all_layers_demo.py
|-- src/
|   `-- oversee/
|       |-- case_context/
|       |-- case_management/
|       |-- comparison/
|       |-- config/
|       |-- decision_rules/
|       |-- deterministic_anchor/
|       |-- digital_factory/
|       |-- domain/
|       |-- external_sources/
|       |-- governance/
|       |-- grounded_model_path/
|       |-- integration/
|       |-- live_generative_path/
|       |-- model_backed_anchor/
|       |-- reporting/
|       |-- retrieval/
|       |-- upstream/
|       |-- utils/
|       `-- __init__.py
|-- tests/
|   `-- oversee/
|       |-- case_context/
|       |-- case_management/
|       |-- comparison/
|       |-- decision_rules/
|       |-- deterministic_anchor/
|       |-- integration/
|       |-- layers/
|       |-- live_generative_path/
|       `-- reporting/
|-- .gitignore
|-- CHANGELOG.md
|-- README.md
|-- pyproject.toml
`-- requirements.txt
```

## 5. Explicacion carpeta por carpeta

### Repository root

Raiz del repositorio. Contiene la documentacion principal, la configuracion del proyecto, los scripts de ejecucion, el codigo fuente, las demos y los tests.

Subcarpetas directas:

- `.github/`: Subcarpeta del proyecto.
- `demo/`: Contiene elementos de demostracion. No debe ser dependencia del core. La direccion correcta es demo -> src/oversee.
- `docs/`: Documentacion del proyecto, manuales, guias de demo, resumenes de release e informes.
- `knowledge_base/`: Subcarpeta del proyecto.
- `outputs/`: Carpeta de salidas generadas durante ejecuciones locales. Normalmente no debe versionarse salvo que haya una razon concreta.
- `scripts/`: Scripts ejecutables desde consola. Incluye runners para ejecutar escenarios, demos y flujos completos.
- `src/`: Carpeta principal de codigo fuente Python.
- `tests/`: Suite de tests automatizados.

Ficheros directos principales:

- `.gitignore`
- `CHANGELOG.md`
- `README.md`
- `pyproject.toml`
- `requirements.txt`

### `src/`

Carpeta principal de codigo fuente Python.

Subcarpetas directas:

- `oversee/`: Paquete principal de OVERSEE. Contiene la logica del artefacto: contexto de caso, gestion de caso, reglas, integraciones, gobernanza, reporting y utilidades.

### `src/oversee/`

Paquete principal de OVERSEE. Contiene la logica del artefacto: contexto de caso, gestion de caso, reglas, integraciones, gobernanza, reporting y utilidades.

Subcarpetas directas:

- `case_context/`: Construye y normaliza el contexto canonico del caso. Es la capa que transforma evidencia y contexto operativo en una estructura comun que despues pueden usar las reglas y la gestion del caso.
- `case_management/`: Gestiona el ciclo de vida del caso: estado, tareas, hitos, bloqueos y preparacion para decision. Sirve para evitar que una alerta se trate siempre como lista para ejecutar.
- `comparison/`: Contiene utilidades para comparar resultados o caminos de decision. Ayuda a analizar diferencias entre ejecuciones o condiciones.
- `config/`: Agrupa configuraciones del proyecto. Sirve para centralizar parametros y evitar valores dispersos en el codigo.
- `decision_rules/`: Contiene la logica de decision tipo DMN. Evalua prioridad, modo de ejecucion, factibilidad de intervencion y necesidad de revision humana.
- `deterministic_anchor/`: Contiene anclas deterministas. Sirve como referencia estable para comparar comportamientos frente a caminos mas flexibles o generativos.
- `digital_factory/`: Contiene elementos relacionados con la fabrica digital o entorno sintetico de validacion. Su papel es apoyar escenarios y datos de demostracion.
- `domain/`: Define objetos y conceptos de dominio. Normalmente incluye modelos o estructuras que representan entidades del mundo industrial.
- `external_sources/`: Representa fuentes externas o datos equivalentes a sistemas empresariales. En la demo, estas fuentes se simulan para mantener reproducibilidad.
- `governance/`: Agrupa logica de gobernanza, trazabilidad y control. Es clave para que la recomendacion final sea auditable y revisable.
- `grounded_model_path/`: Contiene componentes de un camino de modelo fundamentado en evidencia o contexto. Sirve para separar salidas apoyadas en informacion trazable.
- `integration/`: Integra las capas y conecta escenarios con la ejecucion real. Aqui estan piezas clave como el cliente de APIs respaldado por escenarios y los constructores de entradas ejecutables.
- `live_generative_path/`: Contiene componentes relacionados con ejecuciones generativas reales o simuladas. En la demo actual no es el foco principal.
- `model_backed_anchor/`: Contiene anclas apoyadas en modelo. Sirve para comparacion o apoyo a decisiones cuando se usa un componente de modelo.
- `reporting/`: Contiene utilidades de reporting. Ayuda a serializar resultados, manifiestos, resumenes y salidas legibles.
- `retrieval/`: Contiene componentes de recuperacion de informacion. Sirve para localizar o preparar informacion que luego alimenta decisiones.
- `upstream/`: Subcarpeta del proyecto.
- `utils/`: Utilidades compartidas por varias partes del proyecto.

Ficheros directos principales:

- `__init__.py`

### `src/oversee/case_context/`

Construye y normaliza el contexto canonico del caso. Es la capa que transforma evidencia y contexto operativo en una estructura comun que despues pueden usar las reglas y la gestion del caso.

Ficheros directos principales:

- `__init__.py`
- `canonical_case_context.py`
- `canonical_context_builder.py`
- `contextualization_rules.py`

### `src/oversee/case_management/`

Gestiona el ciclo de vida del caso: estado, tareas, hitos, bloqueos y preparacion para decision. Sirve para evitar que una alerta se trate siempre como lista para ejecutar.

Ficheros directos principales:

- `__init__.py`
- `case_lifecycle.py`
- `case_lifecycle_builder.py`

### `src/oversee/comparison/`

Contiene utilidades para comparar resultados o caminos de decision. Ayuda a analizar diferencias entre ejecuciones o condiciones.

Ficheros directos principales:

- `__init__.py`
- `deterministic_generative_comparison.py`

### `src/oversee/config/`

Agrupa configuraciones del proyecto. Sirve para centralizar parametros y evitar valores dispersos en el codigo.

Ficheros directos principales:

- `__init__.py`
- `settings.py`

### `src/oversee/decision_rules/`

Contiene la logica de decision tipo DMN. Evalua prioridad, modo de ejecucion, factibilidad de intervencion y necesidad de revision humana.

Ficheros directos principales:

- `__init__.py`
- `decision_rule_contracts.py`
- `dmn_like_rules.py`
- `live_generative_recommendation.py`
- `recommendation_path_runner.py`

### `src/oversee/deterministic_anchor/`

Contiene anclas deterministas. Sirve como referencia estable para comparar comportamientos frente a caminos mas flexibles o generativos.

Ficheros directos principales:

- `__init__.py`
- `contracts.py`
- `deterministic_anchor.py`

### `src/oversee/digital_factory/`

Contiene elementos relacionados con la fabrica digital o entorno sintetico de validacion. Su papel es apoyar escenarios y datos de demostracion.

Ficheros directos principales:

- `__init__.py`
- `compressor_scenario_generator.py`
- `deterministic_anchor_adapter.py`
- `generative_external_source_factory.py`
- `live_generative_path_adapter.py`
- `oversee_input_mapper.py`
- `scenario_bridge_adapter.py`
- `synthetic_case_schema.py`
- `synthetic_scenario_loader.py`

### `src/oversee/domain/`

Define objetos y conceptos de dominio. Normalmente incluye modelos o estructuras que representan entidades del mundo industrial.

Ficheros directos principales:

- `DATA_DICTIONARY.md`
- `README.md`
- `__init__.py`
- `asset.py`
- `decision_case.py`
- `enums.py`
- `intervention.py`
- `predictive_alert.py`
- `recommendation.py`
- `validators.py`

### `src/oversee/external_sources/`

Representa fuentes externas o datos equivalentes a sistemas empresariales. En la demo, estas fuentes se simulan para mantener reproducibilidad.

Ficheros directos principales:

- `__init__.py`
- `compressor_external_source_factory.py`
- `external_source_contracts.py`

### `src/oversee/governance/`

Agrupa logica de gobernanza, trazabilidad y control. Es clave para que la recomendacion final sea auditable y revisable.

Ficheros directos principales:

- `__init__.py`
- `contracts.py`

### `src/oversee/grounded_model_path/`

Contiene componentes de un camino de modelo fundamentado en evidencia o contexto. Sirve para separar salidas apoyadas en informacion trazable.

Ficheros directos principales:

- `__init__.py`
- `grounded_model_path.py`
- `grounded_model_payload.py`

### `src/oversee/integration/`

Integra las capas y conecta escenarios con la ejecucion real. Aqui estan piezas clave como el cliente de APIs respaldado por escenarios y los constructores de entradas ejecutables.

Ficheros directos principales:

- `__init__.py`
- `layer1_evidence_pipeline.py`
- `predictive_alert_api.py`
- `scenario_backed_enterprise_apis.py`
- `scenario_executable_inputs.py`
- `simulated_enterprise_apis.py`

### `src/oversee/live_generative_path/`

Contiene componentes relacionados con ejecuciones generativas reales o simuladas. En la demo actual no es el foco principal.

Ficheros directos principales:

- `__init__.py`
- `live_generative_path.py`
- `live_generative_payload.py`

### `src/oversee/model_backed_anchor/`

Contiene anclas apoyadas en modelo. Sirve para comparacion o apoyo a decisiones cuando se usa un componente de modelo.

Ficheros directos principales:

- `__init__.py`
- `model_backed_anchor.py`
- `model_backed_payload.py`

### `src/oversee/reporting/`

Contiene utilidades de reporting. Ayuda a serializar resultados, manifiestos, resumenes y salidas legibles.

Ficheros directos principales:

- `__init__.py`
- `generative_comparison.py`
- `governed_recommendation_package.py`
- `reviewer_package.py`

### `src/oversee/retrieval/`

Contiene componentes de recuperacion de informacion. Sirve para localizar o preparar informacion que luego alimenta decisiones.

Ficheros directos principales:

- `__init__.py`
- `evidence_bundle.py`
- `maintenance_guidance_retriever.py`

### `src/oversee/utils/`

Utilidades compartidas por varias partes del proyecto.

Ficheros directos principales:

- `__init__.py`
- `model_client.py`

### `demo/`

Contiene elementos de demostracion. No debe ser dependencia del core. La direccion correcta es demo -> src/oversee.

Subcarpetas directas:

- `interactive_walkthrough/`: Demo interactiva que explica OVERSEE capa por capa. Usa los escenarios ejecutables y presenta la salida de forma guiada.

Ficheros directos principales:

- `__init__.py`

### `demo/interactive_walkthrough/`

Demo interactiva que explica OVERSEE capa por capa. Usa los escenarios ejecutables y presenta la salida de forma guiada.

Subcarpetas directas:

- `adapters/`: Adaptadores que conectan la demo con los runners reales sin contaminar el core.
- `presenters/`: Presentadores de consola. Transforman resultados y artefactos en una explicacion paso a paso.
- `scenarios/`: Catalogo de escenarios JSON. Cada escenario contiene narrativa de demo y entradas ejecutables para el runner real.

Ficheros directos principales:

- `DEMO_MANUAL.md`
- `README.md`
- `__init__.py`
- `demo_state.py`
- `display.py`
- `output_manager.py`
- `pause.py`
- `scenario_catalog.py`
- `walkthrough.py`

### `demo/interactive_walkthrough/scenarios/`

Catalogo de escenarios JSON. Cada escenario contiene narrativa de demo y entradas ejecutables para el runner real.

Ficheros directos principales:

- `agv_001_battery_degradation.json`
- `boiler_001_pressure_instability.json`
- `chiller_001_energy_efficiency_degradation.json`
- `cip_001_cleaning_reliability_issue.json`
- `comp_001_default.json`
- `comp_002_lower_urgency.json`
- `comp_003_rapid_degradation_missing_specialist.json`
- `conv_001_production_conflict.json`
- `data_001_evidence_quality_stop.json`
- `fan_001_low_criticality_monitoring.json`
- `gear_001_repeated_wear.json`
- `hvac_001_air_handling_degradation.json`
- `mixer_001_product_quality_instability.json`
- `motor_001_moderate_overheating.json`
- `pack_001_bottleneck_stoppages.json`
- `pump_001_resource_constrained.json`
- `pump_002_technician_unavailable.json`
- `robot_001_safety_sensitive_axis_abnormality.json`
- `sensor_001_sensor_drift_suspected.json`
- `valve_001_intermittent_actuation_fault.json`

### `demo/interactive_walkthrough/adapters/`

Adaptadores que conectan la demo con los runners reales sin contaminar el core.

Ficheros directos principales:

- `__init__.py`
- `placeholder_adapter.py`
- `real_layer1_adapter.py`
- `real_layer2_adapter.py`
- `real_layer3_adapter.py`
- `real_layer4_adapter.py`
- `real_layer5_adapter.py`
- `scenario_all_layers_adapter.py`

### `demo/interactive_walkthrough/presenters/`

Presentadores de consola. Transforman resultados y artefactos en una explicacion paso a paso.

Ficheros directos principales:

- `__init__.py`
- `common.py`
- `intro_presenter.py`
- `layer_presenter.py`

### `scripts/`

Scripts ejecutables desde consola. Incluye runners para ejecutar escenarios, demos y flujos completos.

Ficheros directos principales:

- `run_deterministic_anchor_smoke.py`
- `run_deterministic_generative_comparison.py`
- `run_digital_factory_deterministic_anchor_smoke.py`
- `run_digital_factory_live_generative_path_offline_smoke.py`
- `run_generative_digital_factory_workbench_smoke.py`
- `run_interactive_oversee_demo.py`
- `run_layer1_layer2_compressor_smoke.py`
- `run_layer1_paper_aligned_demo.py`
- `run_layer2_paper_aligned_demo.py`
- `run_layer3_case_lifecycle_smoke.py`
- `run_layer3_paper_aligned_demo.py`
- `run_layer4_decision_rules_smoke.py`
- `run_layer4_paper_aligned_demo.py`
- `run_layer5_governed_package_smoke.py`
- `run_layer5_paper_aligned_demo.py`
- `run_live_generative_oversee_smoke.py`
- `run_live_generative_path_offline_smoke.py`
- `run_oversee_reviewer_demo.py`
- `run_paper_aligned_all_layers_demo.py`
- `run_scenario_all_layers_demo.py`

### `tests/`

Suite de tests automatizados.

Subcarpetas directas:

- `oversee/`: Tests del paquete OVERSEE.

### `tests/oversee/`

Tests del paquete OVERSEE.

Subcarpetas directas:

- `case_context/`: Subcarpeta del proyecto.
- `case_management/`: Subcarpeta del proyecto.
- `comparison/`: Subcarpeta del proyecto.
- `decision_rules/`: Subcarpeta del proyecto.
- `deterministic_anchor/`: Subcarpeta del proyecto.
- `integration/`: Tests de integracion. Verifican que escenarios, runners y capas funcionen juntos.
- `layers/`: Subcarpeta del proyecto.
- `live_generative_path/`: Subcarpeta del proyecto.
- `reporting/`: Subcarpeta del proyecto.

### `tests/oversee/integration/`

Tests de integracion. Verifican que escenarios, runners y capas funcionen juntos.

Ficheros directos principales:

- `test_data_quality_scenario_behavior.py`
- `test_full_executable_scenario_library.py`
- `test_interactive_walkthrough_scenario_runner_adapter.py`
- `test_layer1_paper_aligned_demo.py`
- `test_layer1_scenario_injection.py`
- `test_master_scenario_execution.py`
- `test_scenario_all_layers_execution.py`
- `test_scenario_backed_enterprise_apis.py`
- `test_scenario_executable_inputs.py`

### `docs/`

Documentacion del proyecto, manuales, guias de demo, resumenes de release e informes.

Subcarpetas directas:

- `reports/`: Reportes generados para la demo. Incluye resumenes de resultados en Markdown, CSV y JSON.

Ficheros directos principales:

- `advanced_workbench_demo_guide.md`
- `implementation_status.md`
- `master_cases_demo_guide.md`
- `master_cases_results_comparison.md`
- `oversee_architecture_comp001_deep_dive_manual.md`
- `oversee_architecture_comp001_deep_dive_manual.pdf`
- `paper_aligned_all_layers_demo_guide.md`
- `release_v0_6_1_summary.md`
- `reviewer_demo_walkthrough.md`
- `scenario_coverage_matrix.md`

### `docs/reports/`

Reportes generados para la demo. Incluye resumenes de resultados en Markdown, CSV y JSON.

Ficheros directos principales:

- `v0_6_2_scenario_results_summary.csv`
- `v0_6_2_scenario_results_summary.json`
- `v0_6_2_scenario_results_summary.md`

## 6. Escenarios ejecutables incluidos en la demo

Los escenarios estan en:

```text
demo/interactive_walkthrough/scenarios/
```

Cada escenario JSON contiene dos niveles de informacion:

1. Informacion narrativa para explicar la demo capa por capa.
2. Entradas ejecutables para alimentar el runner real Layer 1 a Layer 5.

Tabla de escenarios versionados:

| Scenario | Master | Asset type | Failure mode | Title |
|---|---:|---|---|---|
| `AGV-001` | False | `automated_guided_vehicle` | `battery_degradation` | Redundant AGV battery degradation case |
| `BOILER-001` | False | `boiler_system` | `pressure_instability` | Boiler pressure instability case |
| `CHILLER-001` | False | `industrial_chiller` | `energy_efficiency_degradation` | Chiller energy efficiency degradation case |
| `CIP-001` | False | `cip_system` | `cleaning_cycle_reliability_issue` | CIP cleaning reliability case |
| `COMP-001` | True | `industrial_air_compressor` | `bearing_degradation` | Paper compressor case |
| `COMP-002` | True | `industrial_air_compressor` | `early_vibration_anomaly` | Lower urgency compressor case |
| `COMP-003` | False | `industrial_air_compressor` | `rapid_degradation_missing_specialist` | Rapid compressor degradation with missing specialist case |
| `CONV-001` | True | `conveyor_system` | `belt_drive_degradation` | Production-constrained conveyor case |
| `DATA-001` | True | `electric_motor` | `contradictory_thermal_vibration_evidence` | Evidence-quality stop case |
| `FAN-001` | False | `industrial_fan` | `mild_vibration_drift` | Low-criticality fan monitoring case |
| `GEAR-001` | False | `gearbox` | `repeated_gear_wear` | Repeated gearbox wear case |
| `HVAC-001` | False | `industrial_hvac` | `air_handling_degradation` | Industrial HVAC air handling case |
| `MIXER-001` | False | `industrial_mixer` | `mixing_instability` | Mixer product quality instability case |
| `MOTOR-001` | False | `electric_motor` | `moderate_overheating` | Moderate motor overheating case |
| `PACK-001` | False | `packaging_line_asset` | `intermittent_stoppages` | Packaging bottleneck stoppage case |
| `PUMP-001` | True | `industrial_pump` | `seal_degradation` | Resource-constrained pump case |
| `PUMP-002` | False | `industrial_pump` | `bearing_wear` | Pump spare available but technician unavailable case |
| `ROBOT-001` | False | `industrial_robot` | `axis_abnormality` | Safety-sensitive robot axis case |
| `SENSOR-001` | False | `critical_sensor` | `sensor_drift_suspected` | Critical sensor drift suspected case |
| `VALVE-001` | False | `critical_valve` | `intermittent_actuation_fault` | Intermittent critical valve fault case |

## 7. Como se ejecuta la demo

Para listar escenarios:

```powershell
$env:PYTHONPATH = "."
python scripts\run_scenario_all_layers_demo.py --list-scenarios
```

Para ejecutar un caso completo por las cinco capas:

```powershell
$env:PYTHONPATH = "."
python scripts\run_scenario_all_layers_demo.py --scenario COMP-001
```

Para ejecutar la demo interactiva:

```powershell
$env:PYTHONPATH = "."
python scripts\run_interactive_oversee_demo.py --scenario COMP-001
```

## 8. Como se valida el repositorio

Validacion completa:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee -q
```

Validacion especifica de los 20 escenarios:

```powershell
$env:PYTHONPATH = "."
python -m pytest tests\oversee\integration\test_full_executable_scenario_library.py -q
```

En el hito actual, el resultado esperado es:

```text
88 passed
21 passed en el test formal de escenarios
```

## 9. Salidas generadas durante una ejecucion

Cuando se ejecuta un escenario, se generan carpetas temporales bajo `outputs/`.

Estas carpetas contienen artefactos como:

- `00_scenario.json`
- `00_predictive_alert_request.json`
- `01_aggregated_evidence_package.json`
- `01_validation_report.json`
- `02_canonical_case_context.json`
- `03_case_management_state.json`
- `04_dmn_decision_evaluation.json`
- `05_governed_recommendation_package.json`
- `05_traceability_index.json`
- `05_scenario_execution_summary.md`

La idea es que OVERSEE no produzca solo una recomendacion final, sino una cadena de evidencia completa que permita explicar que entro, como se interpreto, que reglas se aplicaron y que salida final se genero.

## 10. Resumen para explicar el proyecto

La forma mas sencilla de explicar el repositorio es:

```text
src/oversee/ contiene el motor.
demo/ contiene la explicacion interactiva.
scripts/ contiene los lanzadores.
demo/interactive_walkthrough/scenarios/ contiene los 20 casos.
tests/ demuestra que todo sigue funcionando.
docs/ contiene el material para explicar la demo.
```

OVERSEE no es solo un modelo predictivo. Es un artefacto de orquestacion decision-to-action gobernado, donde una alerta predictiva se transforma en una recomendacion trazable mediante evidencia, contexto, ciclo de vida del caso, reglas explicitas y empaquetado final.
