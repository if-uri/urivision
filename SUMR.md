# urivision 0.3 — VURI + URI Runtime + Native Test Lab

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `urivision`
- **version**: `0.3.0`
- **python_requires**: `>=3.10`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(2), app.doql.less, docker-compose.yml, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: urivision;
  version: 0.3.0;
}

dependencies {
  litellm: litellm>=1.40;
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="urivision"] {
  entry: urivision.cli:main;
}

integration[name="github"] {
  type: scm;
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=PYTHONPATH=src:. python3 -m unittest discover -s tests -v;
}

workflow[name="matrix"] {
  trigger: manual;
  step-1: run cmd=PYTHONPATH=src:. python3 tools/run_backend_matrix.py --out artifacts/backend-matrix.json --markdown artifacts/backend-matrix.md;
}

workflow[name="native-matrix"] {
  trigger: manual;
  step-1: run cmd=PYTHONPATH=src:. python3 tools/run_native_lab_matrix.py --out artifacts/native-lab-matrix.json --markdown artifacts/native-lab-matrix.md --confidence artifacts/native-confidence-gate.md;
}

workflow[name="native-probe"] {
  trigger: manual;
  step-1: run cmd=PYTHONPATH=src:. python3 tools/probe_native_host.py --out artifacts/native-host-probe.json;
}

workflow[name="confidence"] {
  trigger: manual;
  step-1: run cmd=PYTHONPATH=src:. python3 tools/check_confidence_gate.py artifacts/native-lab-matrix.json;
}

workflow[name="docker-matrix"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml run --rm uri-runtime-matrix;
}

workflow[name="docker-linux-x11"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml --profile linux-x11 up --build --abort-on-container-exit;
}

workflow[name="docker-wayland"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml --profile linux-wayland up --build --abort-on-container-exit;
}

workflow[name="docker-contract"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml --profile contract up --build --abort-on-container-exit;
}

workflow[name="zip"] {
  trigger: manual;
  step-1: run cmd=cd .. && zip -qr urivision_native_test_lab.zip urivision -x 'urivision/venv/*' -x 'urivision/.git/*';
}

tests {
  import: testql-scenarios/**/*.testql.toon.yaml;
}

env_vars {
  keys: XDG_SESSION_TYPE, DISPLAY, WAYLAND_DISPLAY, CI, GITHUB_ACTIONS, URIVISION_BACKEND_PROFILE, URIVISION_PROFILE;
}

deploy {
  target: docker-compose;
  compose_file: docker/docker-compose.yml;
}

environment[name="local"] {
  runtime: docker-compose;
  python_version: >=3.10;
}
```

## Workflows

## Call Graph

*60 nodes · 52 edges · 21 modules · CC̄=4.2*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `build_default_registry` *(in src.urivision.runtime)* | 1 | 1 | 187 | **188** |
| `run_probe` *(in tools.probe_runtime)* | 9 | 2 | 39 | **41** |
| `parse` *(in src.urivision.dsl)* | 19 ⚠ | 1 | 35 | **36** |
| `probe` *(in tools.probe_native_host)* | 17 ⚠ | 1 | 31 | **32** |
| `_find_element` *(in src.urivision.runtime)* | 14 ⚠ | 3 | 24 | **27** |
| `_ensure_state` *(in src.urivision.runtime)* | 1 | 13 | 8 | **21** |
| `print` *(in native.linux.probe_linux_display)* | 0 | 21 | 0 | **21** |
| `route_intent` *(in src.urivision.method_router)* | 12 ⚠ | 3 | 18 | **21** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/if-uri/urivision
# generated in 0.03s
# nodes: 60 | edges: 52 | modules: 21
# CC̄=4.2

HUBS[20]:
  src.urivision.runtime.build_default_registry
    CC=1  in:1  out:187  total:188
  tools.probe_runtime.run_probe
    CC=9  in:2  out:39  total:41
  src.urivision.dsl.parse
    CC=19  in:1  out:35  total:36
  tools.probe_native_host.probe
    CC=17  in:1  out:31  total:32
  src.urivision.runtime._find_element
    CC=14  in:3  out:24  total:27
  src.urivision.runtime._ensure_state
    CC=1  in:13  out:8  total:21
  native.linux.probe_linux_display.print
    CC=0  in:21  out:0  total:21
  src.urivision.method_router.route_intent
    CC=12  in:3  out:18  total:21
  src.urivision.registry.CapabilityRegistry.register
    CC=2  in:18  out:2  total:20
  tools.run_native_lab_matrix.main
    CC=1  in:0  out:20  total:20
  src.urivision.registry.validate_payload
    CC=12  in:1  out:18  total:19
  src.urivision.orchestrator.PlanRunner.run
    CC=10  in:0  out:17  total:17
  src.urivision.runner_litellm.run
    CC=4  in:0  out:17  total:17
  src.urivision.orchestrator._resolve_templates
    CC=9  in:3  out:11  total:14
  tools.probe_native_host.run_short
    CC=2  in:10  out:3  total:13
  src.urivision.orchestrator._check_expectation
    CC=8  in:1  out:12  total:13
  tools.run_native_lab_matrix.build_matrix
    CC=8  in:1  out:12  total:13
  src.urivision.native_profiles.native_matrix_markdown
    CC=4  in:2  out:11  total:13
  tools.probe_runtime.main
    CC=3  in:0  out:12  total:12
  src.urivision.uri.parse_uri
    CC=7  in:3  out:9  total:12

MODULES:
  examples.function_binding_example  [1 funcs]
    add  CC=1  out:1
  native.linux.probe_linux_display  [1 funcs]
    print  CC=0  out:0
  src.urivision  [3 funcs]
    run  CC=1  out:1
    run_file  CC=1  out:3
    run_source  CC=1  out:3
  src.urivision.bindings  [3 funcs]
    register_module_uri_functions  CC=4  out:6
    register_uri_function  CC=2  out:9
    uri_function  CC=1  out:5
  src.urivision.compiler  [1 funcs]
    compile_prompt  CC=4  out:6
  src.urivision.dsl  [1 funcs]
    parse  CC=19  out:35
  src.urivision.llm_catalog  [2 funcs]
    compile_runtime_prompt  CC=2  out:2
    compile_runtime_tools  CC=2  out:2
  src.urivision.method_router  [2 funcs]
    route_intent  CC=12  out:18
    route_matrix  CC=3  out:5
  src.urivision.native_profiles  [4 funcs]
    coverage_summary  CC=9  out:6
    get_native_target  CC=2  out:3
    list_native_targets  CC=2  out:1
    native_matrix_markdown  CC=4  out:11
  src.urivision.orchestrator  [7 funcs]
    __init__  CC=2  out:1
    run  CC=10  out:17
    _check_expectation  CC=8  out:12
    _get_path  CC=5  out:5
    _resolve_templates  CC=9  out:11
    run_plan  CC=1  out:2
    run_plan_file  CC=1  out:4
  src.urivision.registry  [7 funcs]
    all  CC=1  out:1
    call  CC=6  out:9
    capability  CC=1  out:3
    find  CC=3  out:2
    register  CC=2  out:2
    schema_from_signature  CC=10  out:3
    validate_payload  CC=12  out:18
  src.urivision.resolver  [3 funcs]
    artifact_path  CC=6  out:8
    label  CC=2  out:1
    model_id  CC=1  out:0
  src.urivision.runner_litellm  [1 funcs]
    run  CC=4  out:17
  src.urivision.runtime  [7 funcs]
    __init__  CC=3  out:2
    _default_tree  CC=1  out:0
    _ensure_state  CC=1  out:8
    _find_element  CC=14  out:24
    _walk  CC=3  out:3
    build_default_registry  CC=1  out:187
    default_runtime  CC=2  out:2
  src.urivision.schemas  [1 funcs]
    resolve_schema  CC=2  out:1
  src.urivision.uri  [4 funcs]
    _match_segment  CC=7  out:4
    match_uri  CC=6  out:7
    normalize_uri  CC=2  out:2
    parse_uri  CC=7  out:9
  src.urivision.validators  [2 funcs]
    _scheme  CC=2  out:1
    validate  CC=14  out:10
  tools.check_confidence_gate  [1 funcs]
    main  CC=9  out:10
  tools.probe_native_host  [4 funcs]
    main  CC=2  out:10
    probe  CC=17  out:31
    read_os_release  CC=4  out:7
    run_short  CC=2  out:3
  tools.probe_runtime  [2 funcs]
    main  CC=3  out:12
    run_probe  CC=9  out:39
  tools.run_native_lab_matrix  [3 funcs]
    build_matrix  CC=8  out:12
    contract_check  CC=4  out:10
    main  CC=1  out:20

EDGES:
  src.urivision.runner_litellm.run → src.urivision.resolver.model_id
  src.urivision.runner_litellm.run → src.urivision.schemas.resolve_schema
  src.urivision.runner_litellm.run → src.urivision.compiler.compile_prompt
  src.urivision.runner_litellm.run → src.urivision.resolver.artifact_path
  src.urivision.compiler.compile_prompt → src.urivision.resolver.label
  src.urivision.registry.CapabilityRegistry.capability → src.urivision.registry.schema_from_signature
  src.urivision.registry.CapabilityRegistry.find → src.urivision.uri.match_uri
  src.urivision.registry.CapabilityRegistry.call → src.urivision.registry.validate_payload
  tools.check_confidence_gate.main → native.linux.probe_linux_display.print
  tools.check_confidence_gate.main → src.urivision.registry.CapabilityRegistry.all
  tools.run_native_lab_matrix.contract_check → src.urivision.runtime.default_runtime
  tools.run_native_lab_matrix.contract_check → src.urivision.registry.CapabilityRegistry.all
  tools.run_native_lab_matrix.build_matrix → tools.run_native_lab_matrix.contract_check
  tools.run_native_lab_matrix.build_matrix → src.urivision.native_profiles.list_native_targets
  tools.run_native_lab_matrix.build_matrix → src.urivision.native_profiles.coverage_summary
  tools.run_native_lab_matrix.build_matrix → src.urivision.method_router.route_intent
  tools.run_native_lab_matrix.main → tools.run_native_lab_matrix.build_matrix
  tools.probe_native_host.probe → tools.probe_native_host.run_short
  tools.probe_native_host.probe → tools.probe_native_host.read_os_release
  tools.probe_native_host.main → tools.probe_native_host.probe
  tools.probe_native_host.main → native.linux.probe_linux_display.print
  src.urivision.run_source → src.urivision.validators.validate
  src.urivision.run_source → src.urivision.dsl.parse
  src.urivision.run_file → src.urivision.run_source
  src.urivision.run → src.urivision.run_source
  src.urivision.validators.validate → src.urivision.validators._scheme
  tools.probe_runtime.run_probe → src.urivision.runtime.default_runtime
  tools.probe_runtime.main → tools.probe_runtime.run_probe
  tools.probe_runtime.main → native.linux.probe_linux_display.print
  src.urivision.llm_catalog.compile_runtime_prompt → src.urivision.runtime.default_runtime
  src.urivision.llm_catalog.compile_runtime_tools → src.urivision.runtime.default_runtime
  src.urivision.bindings.uri_function → src.urivision.registry.schema_from_signature
  src.urivision.bindings.register_module_uri_functions → src.urivision.bindings.register_uri_function
  src.urivision.orchestrator._resolve_templates → src.urivision.orchestrator._get_path
  src.urivision.orchestrator.PlanRunner.__init__ → src.urivision.runtime.default_runtime
  src.urivision.orchestrator.PlanRunner.run → src.urivision.orchestrator._resolve_templates
  src.urivision.orchestrator.PlanRunner.run → src.urivision.orchestrator._check_expectation
  src.urivision.orchestrator.run_plan_file → src.urivision.orchestrator.run_plan
  examples.function_binding_example.add → src.urivision.bindings.uri_function
  src.urivision.native_profiles.coverage_summary → src.urivision.native_profiles.list_native_targets
  src.urivision.native_profiles.native_matrix_markdown → src.urivision.native_profiles.coverage_summary
  src.urivision.native_profiles.native_matrix_markdown → src.urivision.native_profiles.list_native_targets
  src.urivision.uri.normalize_uri → src.urivision.uri.parse_uri
  src.urivision.uri.match_uri → src.urivision.uri.parse_uri
  src.urivision.uri.match_uri → src.urivision.uri._match_segment
  src.urivision.runtime._ensure_state → src.urivision.runtime._default_tree
  src.urivision.runtime._find_element → src.urivision.runtime._walk
  src.urivision.runtime.build_default_registry → src.urivision.registry.CapabilityRegistry.register
  src.urivision.runtime.UriRuntime.__init__ → src.urivision.runtime.build_default_registry
  src.urivision.method_router.route_intent → src.urivision.native_profiles.get_native_target
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/if-uri/urivision
# generated in 0.03s
# nodes: 60 | edges: 52 | modules: 21
# CC̄=4.2

HUBS[20]:
  src.urivision.runtime.build_default_registry
    CC=1  in:1  out:187  total:188
  tools.probe_runtime.run_probe
    CC=9  in:2  out:39  total:41
  src.urivision.dsl.parse
    CC=19  in:1  out:35  total:36
  tools.probe_native_host.probe
    CC=17  in:1  out:31  total:32
  src.urivision.runtime._find_element
    CC=14  in:3  out:24  total:27
  src.urivision.runtime._ensure_state
    CC=1  in:13  out:8  total:21
  native.linux.probe_linux_display.print
    CC=0  in:21  out:0  total:21
  src.urivision.method_router.route_intent
    CC=12  in:3  out:18  total:21
  src.urivision.registry.CapabilityRegistry.register
    CC=2  in:18  out:2  total:20
  tools.run_native_lab_matrix.main
    CC=1  in:0  out:20  total:20
  src.urivision.registry.validate_payload
    CC=12  in:1  out:18  total:19
  src.urivision.orchestrator.PlanRunner.run
    CC=10  in:0  out:17  total:17
  src.urivision.runner_litellm.run
    CC=4  in:0  out:17  total:17
  src.urivision.orchestrator._resolve_templates
    CC=9  in:3  out:11  total:14
  tools.probe_native_host.run_short
    CC=2  in:10  out:3  total:13
  src.urivision.orchestrator._check_expectation
    CC=8  in:1  out:12  total:13
  tools.run_native_lab_matrix.build_matrix
    CC=8  in:1  out:12  total:13
  src.urivision.native_profiles.native_matrix_markdown
    CC=4  in:2  out:11  total:13
  tools.probe_runtime.main
    CC=3  in:0  out:12  total:12
  src.urivision.uri.parse_uri
    CC=7  in:3  out:9  total:12

MODULES:
  examples.function_binding_example  [1 funcs]
    add  CC=1  out:1
  native.linux.probe_linux_display  [1 funcs]
    print  CC=0  out:0
  src.urivision  [3 funcs]
    run  CC=1  out:1
    run_file  CC=1  out:3
    run_source  CC=1  out:3
  src.urivision.bindings  [3 funcs]
    register_module_uri_functions  CC=4  out:6
    register_uri_function  CC=2  out:9
    uri_function  CC=1  out:5
  src.urivision.compiler  [1 funcs]
    compile_prompt  CC=4  out:6
  src.urivision.dsl  [1 funcs]
    parse  CC=19  out:35
  src.urivision.llm_catalog  [2 funcs]
    compile_runtime_prompt  CC=2  out:2
    compile_runtime_tools  CC=2  out:2
  src.urivision.method_router  [2 funcs]
    route_intent  CC=12  out:18
    route_matrix  CC=3  out:5
  src.urivision.native_profiles  [4 funcs]
    coverage_summary  CC=9  out:6
    get_native_target  CC=2  out:3
    list_native_targets  CC=2  out:1
    native_matrix_markdown  CC=4  out:11
  src.urivision.orchestrator  [7 funcs]
    __init__  CC=2  out:1
    run  CC=10  out:17
    _check_expectation  CC=8  out:12
    _get_path  CC=5  out:5
    _resolve_templates  CC=9  out:11
    run_plan  CC=1  out:2
    run_plan_file  CC=1  out:4
  src.urivision.registry  [7 funcs]
    all  CC=1  out:1
    call  CC=6  out:9
    capability  CC=1  out:3
    find  CC=3  out:2
    register  CC=2  out:2
    schema_from_signature  CC=10  out:3
    validate_payload  CC=12  out:18
  src.urivision.resolver  [3 funcs]
    artifact_path  CC=6  out:8
    label  CC=2  out:1
    model_id  CC=1  out:0
  src.urivision.runner_litellm  [1 funcs]
    run  CC=4  out:17
  src.urivision.runtime  [7 funcs]
    __init__  CC=3  out:2
    _default_tree  CC=1  out:0
    _ensure_state  CC=1  out:8
    _find_element  CC=14  out:24
    _walk  CC=3  out:3
    build_default_registry  CC=1  out:187
    default_runtime  CC=2  out:2
  src.urivision.schemas  [1 funcs]
    resolve_schema  CC=2  out:1
  src.urivision.uri  [4 funcs]
    _match_segment  CC=7  out:4
    match_uri  CC=6  out:7
    normalize_uri  CC=2  out:2
    parse_uri  CC=7  out:9
  src.urivision.validators  [2 funcs]
    _scheme  CC=2  out:1
    validate  CC=14  out:10
  tools.check_confidence_gate  [1 funcs]
    main  CC=9  out:10
  tools.probe_native_host  [4 funcs]
    main  CC=2  out:10
    probe  CC=17  out:31
    read_os_release  CC=4  out:7
    run_short  CC=2  out:3
  tools.probe_runtime  [2 funcs]
    main  CC=3  out:12
    run_probe  CC=9  out:39
  tools.run_native_lab_matrix  [3 funcs]
    build_matrix  CC=8  out:12
    contract_check  CC=4  out:10
    main  CC=1  out:20

EDGES:
  src.urivision.runner_litellm.run → src.urivision.resolver.model_id
  src.urivision.runner_litellm.run → src.urivision.schemas.resolve_schema
  src.urivision.runner_litellm.run → src.urivision.compiler.compile_prompt
  src.urivision.runner_litellm.run → src.urivision.resolver.artifact_path
  src.urivision.compiler.compile_prompt → src.urivision.resolver.label
  src.urivision.registry.CapabilityRegistry.capability → src.urivision.registry.schema_from_signature
  src.urivision.registry.CapabilityRegistry.find → src.urivision.uri.match_uri
  src.urivision.registry.CapabilityRegistry.call → src.urivision.registry.validate_payload
  tools.check_confidence_gate.main → native.linux.probe_linux_display.print
  tools.check_confidence_gate.main → src.urivision.registry.CapabilityRegistry.all
  tools.run_native_lab_matrix.contract_check → src.urivision.runtime.default_runtime
  tools.run_native_lab_matrix.contract_check → src.urivision.registry.CapabilityRegistry.all
  tools.run_native_lab_matrix.build_matrix → tools.run_native_lab_matrix.contract_check
  tools.run_native_lab_matrix.build_matrix → src.urivision.native_profiles.list_native_targets
  tools.run_native_lab_matrix.build_matrix → src.urivision.native_profiles.coverage_summary
  tools.run_native_lab_matrix.build_matrix → src.urivision.method_router.route_intent
  tools.run_native_lab_matrix.main → tools.run_native_lab_matrix.build_matrix
  tools.probe_native_host.probe → tools.probe_native_host.run_short
  tools.probe_native_host.probe → tools.probe_native_host.read_os_release
  tools.probe_native_host.main → tools.probe_native_host.probe
  tools.probe_native_host.main → native.linux.probe_linux_display.print
  src.urivision.run_source → src.urivision.validators.validate
  src.urivision.run_source → src.urivision.dsl.parse
  src.urivision.run_file → src.urivision.run_source
  src.urivision.run → src.urivision.run_source
  src.urivision.validators.validate → src.urivision.validators._scheme
  tools.probe_runtime.run_probe → src.urivision.runtime.default_runtime
  tools.probe_runtime.main → tools.probe_runtime.run_probe
  tools.probe_runtime.main → native.linux.probe_linux_display.print
  src.urivision.llm_catalog.compile_runtime_prompt → src.urivision.runtime.default_runtime
  src.urivision.llm_catalog.compile_runtime_tools → src.urivision.runtime.default_runtime
  src.urivision.bindings.uri_function → src.urivision.registry.schema_from_signature
  src.urivision.bindings.register_module_uri_functions → src.urivision.bindings.register_uri_function
  src.urivision.orchestrator._resolve_templates → src.urivision.orchestrator._get_path
  src.urivision.orchestrator.PlanRunner.__init__ → src.urivision.runtime.default_runtime
  src.urivision.orchestrator.PlanRunner.run → src.urivision.orchestrator._resolve_templates
  src.urivision.orchestrator.PlanRunner.run → src.urivision.orchestrator._check_expectation
  src.urivision.orchestrator.run_plan_file → src.urivision.orchestrator.run_plan
  examples.function_binding_example.add → src.urivision.bindings.uri_function
  src.urivision.native_profiles.coverage_summary → src.urivision.native_profiles.list_native_targets
  src.urivision.native_profiles.native_matrix_markdown → src.urivision.native_profiles.coverage_summary
  src.urivision.native_profiles.native_matrix_markdown → src.urivision.native_profiles.list_native_targets
  src.urivision.uri.normalize_uri → src.urivision.uri.parse_uri
  src.urivision.uri.match_uri → src.urivision.uri.parse_uri
  src.urivision.uri.match_uri → src.urivision.uri._match_segment
  src.urivision.runtime._ensure_state → src.urivision.runtime._default_tree
  src.urivision.runtime._find_element → src.urivision.runtime._walk
  src.urivision.runtime.build_default_registry → src.urivision.registry.CapabilityRegistry.register
  src.urivision.runtime.UriRuntime.__init__ → src.urivision.runtime.build_default_registry
  src.urivision.method_router.route_intent → src.urivision.native_profiles.get_native_target
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 49f 19129L | python:24,shell:10,json:6,yaml:4,toml:1,txt:1,x11-novnc:1,yml:1 | 2026-07-05
# generated in 0.02s
# CC̅=4.2 | critical:3/90 | dups:0 | cycles:2

HEALTH[3]:
  🟡 CC    parse CC=19 (limit:15)
  🟡 CC    probe CC=17 (limit:15)
  🟡 CC    main CC=22 (limit:15)

REFACTOR[2]:
  1. split 3 high-CC methods  (CC>15)
  2. break 2 circular dependencies

PIPELINES[32]:
  [1] Src [run]: run → model_id
      PURITY: 100% pure
  [2] Src [capability]: capability → schema_from_signature
      PURITY: 100% pure
  [3] Src [find]: find → match_uri → parse_uri
      PURITY: 100% pure
  [4] Src [call]: call → validate_payload → _json_type_ok
      PURITY: 100% pure
  [5] Src [catalog_json]: catalog_json
      PURITY: 100% pure
  [6] Src [catalog_markdown]: catalog_markdown
      PURITY: 100% pure
  [7] Src [catalog_prompt]: catalog_prompt
      PURITY: 100% pure
  [8] Src [pretty_json]: pretty_json
      PURITY: 100% pure
  [9] Src [main]: main → print
      PURITY: 100% pure
  [10] Src [main]: main → build_matrix → contract_check → default_runtime
      PURITY: 100% pure
  [11] Src [main]: main → print
      PURITY: 100% pure
  [12] Src [main]: main → probe → run_short
      PURITY: 100% pure
  [13] Src [run]: run → run_source → validate → _scheme
      PURITY: 100% pure
  [14] Src [main]: main → run_probe → default_runtime
      PURITY: 100% pure
  [15] Src [compile_runtime_prompt]: compile_runtime_prompt → default_runtime
      PURITY: 100% pure
  [16] Src [compile_runtime_tools]: compile_runtime_tools → default_runtime
      PURITY: 100% pure
  [17] Src [register_module_uri_functions]: register_module_uri_functions → register_uri_function
      PURITY: 100% pure
  [18] Src [__init__]: __init__ → default_runtime
      PURITY: 100% pure
  [19] Src [run]: run → _resolve_templates → _get_path
      PURITY: 100% pure
  [20] Src [add]: add → uri_function → schema_from_signature
      PURITY: 100% pure
  [21] Src [to_dict]: to_dict
      PURITY: 100% pure
  [22] Src [normalize_uri]: normalize_uri → parse_uri
      PURITY: 100% pure
  [23] Src [main]: main → default_runtime
      PURITY: 100% pure
  [24] Src [__init__]: __init__ → build_default_registry → register
      PURITY: 100% pure
  [25] Src [call]: call
      PURITY: 100% pure
  [26] Src [catalog]: catalog
      PURITY: 100% pure
  [27] Src [explain]: explain
      PURITY: 100% pure
  [28] Src [trace]: trace
      PURITY: 100% pure
  [29] Src [to_dict]: to_dict
      PURITY: 100% pure
  [30] Src [emit]: emit
      PURITY: 100% pure
  [31] Src [to_dict]: to_dict
      PURITY: 100% pure
  [32] Src [to_llm_card]: to_llm_card
      PURITY: 100% pure

LAYERS:
  tools/                          CC̄=5.3    ←in:0  →out:16  !! split
  │ run_native_lab_matrix      117L  0C    4m  CC=8      ←0
  │ !! probe_native_host          112L  0C    4m  CC=17     ←0
  │ probe_runtime               92L  0C    3m  CC=9      ←1
  │ run_backend_matrix          49L  0C    2m  CC=4      ←0
  │ check_confidence_gate       29L  0C    1m  CC=9      ←0
  │
  src/                            CC̄=4.1    ←in:1  →out:2
  │ !! runtime                    513L  1C   13m  CC=14     ←5
  │ native_profiles            427L  1C    6m  CC=9      ←3
  │ registry                   209L  3C   14m  CC=12     ←6
  │ method_router              144L  1C    3m  CC=12     ←2
  │ !! cli                        140L  0C    2m  CC=22     ←0
  │ platforms                  138L  1C    3m  CC=5      ←1
  │ uri                        100L  1C    4m  CC=7      ←1
  │ schemas                     99L  0C    1m  CC=2      ←1
  │ orchestrator                95L  2C    7m  CC=10     ←1
  │ !! dsl                         93L  3C    2m  CC=19     ←1
  │ capability                  89L  2C    3m  CC=6      ←0
  │ bindings                    68L  0C    3m  CC=4      ←1
  │ runner_litellm              54L  0C    2m  CC=4      ←0
  │ __init__                    47L  0C    3m  CC=1      ←1
  │ validators                  38L  1C    2m  CC=14     ←1
  │ compiler                    28L  0C    1m  CC=4      ←1
  │ resolver                    27L  0C    3m  CC=6      ←2
  │ llm_catalog                 15L  0C    2m  CC=2      ←0
  │
  examples/                       CC̄=1.0    ←in:0  →out:1
  │ desktop-control.plan.json    42L  0C    0m  CC=0.0    ←0
  │ guarded-batch.plan.json     21L  0C    0m  CC=0.0    ←0
  │ function_binding_example    18L  0C    1m  CC=1      ←0
  │
  native/                         CC̄=0.0    ←in:0  →out:0
  │ probe_linux_display.sh      31L  0C    1m  CC=0.0    ←6
  │ probe_ios.sh                22L  0C    0m  CC=0.0    ←0
  │ probe_macos_ax.sh           20L  0C    0m  CC=0.0    ←0
  │ runner-manifest.json        19L  0C    0m  CC=0.0    ←0
  │ probe_android.sh            18L  0C    0m  CC=0.0    ←0
  │ run_smoke.sh                 8L  0C    0m  CC=0.0    ←0
  │ run_smoke.sh                 7L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ planfile.yaml              279L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                94L  0C    0m  CC=0.0    ←0
  │ project.sh                  66L  0C    0m  CC=0.0    ←0
  │ Makefile                    31L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              19L  0C    0m  CC=0.0    ←0
  │ tree.sh                      4L  0C    0m  CC=0.0    ←0
  │
  artifacts/                      CC̄=0.0    ←in:0  →out:0
  │ !! native-lab-matrix.json    9534L  0C    0m  CC=0.0    ←0
  │ !! backend-matrix.json       5965L  0C    0m  CC=0.0    ←0
  │ native-host-probe.json      73L  0C    0m  CC=0.0    ←0
  │ docker-availability.txt      7L  0C    0m  CC=0.0    ←0
  │
  docker/                         CC̄=0.0    ←in:0  →out:0
  │ docker-compose.yml          54L  0C    0m  CC=0.0    ←0
  │ Dockerfile.x11-novnc        25L  0C    0m  CC=0.0    ←0
  │ entrypoint-wayland.sh       10L  0C    0m  CC=0.0    ←0
  │ entrypoint-x11-novnc.sh      9L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    10L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                 src.urivision   native.linux          tools            src       examples
  src.urivision             ──             16            ←11              1             ←1  hub
   native.linux            ←16             ──             ←5                                hub
          tools             11              5             ──                                !! fan-out
            src              2                                           ──               
       examples              1                                                          ──
  CYCLES: 2
  HUB: src.urivision/ (fan-in=14)
  HUB: native.linux/ (fan-in=21)
  SMELL: tools/ fan-out=16 → split needed
  SMELL: src.urivision/ fan-out=17 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 2 groups | 24f 2741L | 2026-07-05

SUMMARY:
  files_scanned: 24
  total_lines:   2741
  dup_groups:    2
  dup_fragments: 5
  saved_lines:   9
  scan_ms:       847

HOTSPOTS[2] (files with most duplication):
  src/urivision/uri.py  dup=9L  groups=1  frags=3  (0.3%)
  src/urivision/llm_catalog.py  dup=6L  groups=1  frags=2  (0.2%)

DUPLICATES[2] (ranked by impact):
  [F0002]   FUZZ  kind  L=3 N=3 saved=6 sim=0.87
      src/urivision/uri.py:24-26  (kind)
      src/urivision/uri.py:29-31  (name)
      src/urivision/uri.py:34-36  (area)
  [F0001]   FUZZ  compile_runtime_prompt  L=3 N=2 saved=3 sim=0.91
      src/urivision/llm_catalog.py:8-10  (compile_runtime_prompt)
      src/urivision/llm_catalog.py:13-15  (compile_runtime_tools)

REFACTOR[2] (ranked by priority):
  [1] ○ extract_class      → src/urivision/utils/kind.py
      WHY: 3 occurrences of 3-line block across 1 files — saves 6 lines
      FILES: src/urivision/uri.py
  [2] ○ extract_function   → src/urivision/utils/compile_runtime_prompt.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: src/urivision/llm_catalog.py

QUICK_WINS[1] (low risk, high savings — do first):
  [1] extract_class      saved=6L  → src/urivision/utils/kind.py
      FILES: uri.py

EFFORT_ESTIMATE (total ≈ 0.3h):
  easy   kind                                saved=6L  ~12min
  easy   compile_runtime_prompt              saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  2 → 0
  saved_lines: 9 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 89 func | 24f | 2026-07-05
# generated in 0.00s

NEXT[6] (ranked by impact):
  [1] !! SPLIT           src/urivision/runtime.py
      WHY: 513L, 1 classes, max CC=14
      EFFORT: ~4h  IMPACT: 7182

  [2] !  SPLIT-FUNC      main  CC=22  fan=37
      WHY: CC=22 exceeds 15
      EFFORT: ~1h  IMPACT: 814

  [3] !  SPLIT-FUNC      parse  CC=19  fan=16
      WHY: CC=19 exceeds 15
      EFFORT: ~1h  IMPACT: 304

  [4] !  SPLIT-FUNC      probe  CC=17  fan=9
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 153

  [5] !! SPLIT           artifacts/native-lab-matrix.json
      WHY: 9534L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [6] !! SPLIT           artifacts/backend-matrix.json
      WHY: 5965L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[3]:
  ⚠ Splitting artifacts/native-lab-matrix.json may break 0 import paths
  ⚠ Splitting artifacts/backend-matrix.json may break 0 import paths
  ⚠ Splitting src/urivision/runtime.py may break 13 import paths

METRICS-TARGET:
  CC̄:          4.3 → ≤3.0
  max-CC:      22 → ≤11
  god-modules: 3 → 0
  high-CC(≥15): 3 → ≤1
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=4.4 → now CC̄=4.3
```

## Intent

VURI — Visual URI Process Language plus URI-addressable runtime, Docker contracts and native OS test lab.
