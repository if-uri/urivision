# urivision 0.3 — VURI + URI Runtime + Native Test Lab

VURI — Visual URI Process Language plus URI-addressable runtime, Docker contracts and native OS test lab.

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `urivision`
- **version**: `0.3.0`
- **python_requires**: `>=3.10`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(2), app.doql.less, docker-compose.yml, project/(3 analysis files)

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

## Interfaces

### CLI Entry Points

- `urivision`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m urivision
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m urivision --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m urivision --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m urivision --help" 10000
ASSERT_EXIT_CODE 0
```

#### `testql-scenarios/generated-from-pytests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-from-pytests.testql.toon.yaml
# SCENARIO: Auto-generated from Python Tests
# TYPE: integration
# GENERATED: true

CONFIG[2]{key, value}:
  base_url, ${api_url:-http://localhost:8101}
  timeout_ms, 10000

# NOTE: Python pytest files were detected but no convertible HTTP calls or assertions were found.
# To run pytest tests directly, use: pytest <test_file>
```

## Workflows

## Configuration

```yaml
project:
  name: urivision
  version: 0.3.0
  env: local
```

## Deployment

```bash markpact:run
pip install urivision

# development install
pip install -e .[dev]
```

### Docker Compose (`docker-compose.yml`)

- **uri-runtime-matrix** image=`{'context': '..', 'dockerfile': 'docker/Dockerfile.runtime'}`
- **linux-x11-novnc** image=`{'context': '..', 'dockerfile': 'docker/Dockerfile.x11-novnc'}`
- **linux-wayland-headless** image=`{'context': '..', 'dockerfile': 'docker/Dockerfile.wayland'}`
- **windows-uia-contract** image=`{'context': '..', 'dockerfile': 'docker/Dockerfile.runtime'}`
- **macos-ax-contract** image=`{'context': '..', 'dockerfile': 'docker/Dockerfile.runtime'}`

## Makefile Targets

- `test`
- `matrix`
- `native-matrix`
- `native-probe`
- `confidence`
- `docker-matrix`
- `docker-linux-x11`
- `docker-wayland`
- `docker-contract`
- `zip`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# urivision | 39f 3267L | python:28,shell:10,less:1 | 2026-07-05
# stats: 72 func | 19 cls | 39 mod | CC̄=4.8 | critical:9 | cycles:0
# alerts[5]: CC main=22; CC parse=19; CC probe=17; CC _find_element=14; CC validate=14
# hotspots[5]: main fan=28; build_default_registry fan=27; route_intent fan=14; run fan=14; main fan=12
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[39]:
  app.doql.less,90
  docker/entrypoint-wayland.sh,11
  docker/entrypoint-x11-novnc.sh,10
  examples/function_binding_example.py,19
  native/android/probe_android.sh,19
  native/ios/probe_ios.sh,23
  native/linux/probe_linux_display.sh,32
  native/linux/run_smoke.sh,9
  native/macos/probe_macos_ax.sh,21
  native/macos/run_smoke.sh,8
  project.sh,66
  src/urivision/__init__.py,48
  src/urivision/bindings.py,69
  src/urivision/capability.py,90
  src/urivision/cli.py,141
  src/urivision/compiler.py,29
  src/urivision/dsl.py,94
  src/urivision/llm_catalog.py,16
  src/urivision/method_router.py,145
  src/urivision/native_profiles.py,428
  src/urivision/orchestrator.py,96
  src/urivision/platforms.py,139
  src/urivision/registry.py,210
  src/urivision/resolver.py,28
  src/urivision/runner_litellm.py,55
  src/urivision/runtime.py,514
  src/urivision/schemas.py,100
  src/urivision/uri.py,101
  src/urivision/validators.py,39
  tests/test_backend_profiles.py,38
  tests/test_dsl.py,55
  tests/test_native_lab.py,57
  tests/test_uri_runtime.py,58
  tools/check_confidence_gate.py,30
  tools/probe_native_host.py,113
  tools/probe_runtime.py,93
  tools/run_backend_matrix.py,50
  tools/run_native_lab_matrix.py,118
  tree.sh,5
D:
  examples/function_binding_example.py:
    e: add
    add(a;b)
  src/urivision/__init__.py:
    e: run_source,run_file,run
    run_source(text)
    run_file(path)
    run(text)
  src/urivision/bindings.py:
    e: uri_function,register_uri_function,register_module_uri_functions
    uri_function(uri_pattern)
    register_uri_function(registry;fn)
    register_module_uri_functions(registry;module)
  src/urivision/capability.py:
    e: RuntimeContext,Capability
    RuntimeContext: emit(1)  # Execution context passed to every capability handler.
    Capability: to_dict(0),to_llm_card(0)
  src/urivision/cli.py:
    e: _json_arg,main
    _json_arg(blob)
    main(argv)
  src/urivision/compiler.py:
    e: compile_prompt
    compile_prompt(p)
  src/urivision/dsl.py:
    e: _parse_options,parse,Model,Process,VuriSyntaxError
    Model:
    Process:
    VuriSyntaxError:
    _parse_options(blob)
    parse(text)
  src/urivision/llm_catalog.py:
    e: compile_runtime_prompt,compile_runtime_tools
    compile_runtime_prompt(runtime)
    compile_runtime_tools(runtime)
  src/urivision/method_router.py:
    e: route_intent,route_matrix,RouteDecision
    RouteDecision: to_dict(0)
    route_intent(intent;profile)
    route_matrix()
  src/urivision/native_profiles.py:
    e: list_native_targets,get_native_target,coverage_summary,detect_local_host,native_matrix_markdown,NativeTargetProfile
    NativeTargetProfile: to_dict(0)
    list_native_targets()
    get_native_target(target_id)
    coverage_summary()
    detect_local_host()
    native_matrix_markdown(targets)
  src/urivision/orchestrator.py:
    e: _get_path,_resolve_templates,_check_expectation,run_plan,run_plan_file,PlanError,PlanRunner
    PlanError:
    PlanRunner: __init__(1),run(1)
    _get_path(data;path)
    _resolve_templates(value;outputs)
    _check_expectation(result;expectation)
    run_plan(plan)
    run_plan_file(path)
  src/urivision/platforms.py:
    e: list_backend_profiles,get_backend_profile,BackendProfile
    BackendProfile: to_dict(0)
    list_backend_profiles()
    get_backend_profile(name)
  src/urivision/registry.py:
    e: _json_type_ok,validate_payload,schema_from_signature,pretty_json,UriDispatchError,PayloadValidationError,CapabilityRegistry
    UriDispatchError:
    PayloadValidationError:
    CapabilityRegistry: __init__(0),register(2),capability(1),find(1),call(2),all(0),catalog_json(0),catalog_markdown(0),catalog_prompt(0),tools_json(0)
    _json_type_ok(value;expected)
    validate_payload(schema;payload)
    schema_from_signature(fn)
    pretty_json(data)
  src/urivision/resolver.py:
    e: model_id,artifact_path,label
    model_id(model)
    artifact_path(uri;roots)
    label(uri)
  src/urivision/runner_litellm.py:
    e: _image_data_url,run
    _image_data_url(path;mime)
    run(p)
  src/urivision/runtime.py:
    e: _schema,_ok,_default_tree,_ensure_state,_walk,_find_element,build_default_registry,default_runtime,UriRuntime
    UriRuntime: __init__(1),call(2),catalog(1),explain(1),trace(0)
    _schema(props;required)
    _ok()
    _default_tree()
    _ensure_state(ctx)
    _walk(node)
    _find_element(tree;payload)
    build_default_registry()
    default_runtime()
  src/urivision/schemas.py:
    e: resolve_schema
    resolve_schema(uri)
  src/urivision/uri.py:
    e: parse_uri,normalize_uri,_match_segment,match_uri,UriParts
    UriParts: kind(0),name(0),area(0)
    parse_uri(uri)
    normalize_uri(uri)
    _match_segment(pattern;value;captures)
    match_uri(pattern;uri)
  src/urivision/validators.py:
    e: _scheme,validate,VuriValidationError
    VuriValidationError:
    _scheme(uri)
    validate(p)
  tests/test_backend_profiles.py:
    e: BackendProfileTests
    BackendProfileTests: test_default_matrix_has_four_profiles(0),test_platform_profile_capability(0),test_health_check_for_all_matrix_profiles(0),test_list_backend_profiles(0)
  tests/test_dsl.py:
    e: test_parse_reads_all_parts,test_missing_emit_rejected,test_bad_scheme_rejected,test_non_image_rejected,test_unknown_statement_rejected,test_dry_run_compiles_call_without_model
    test_parse_reads_all_parts()
    test_missing_emit_rejected()
    test_bad_scheme_rejected()
    test_non_image_rejected()
    test_unknown_statement_rejected()
    test_dry_run_compiles_call_without_model()
  tests/test_native_lab.py:
    e: NativeLabTests
    NativeLabTests: test_required_families_are_covered(0),test_each_profile_has_evidence_and_probes(0),test_method_router_selects_route_for_key_intents(0),test_route_matrix_has_all_profiles_and_intents(0),test_known_profile_lookup(0)
  tests/test_uri_runtime.py:
    e: UriRuntimeTests
    UriRuntimeTests: test_parse_and_match_uri(0),test_catalog_has_runtime_capabilities(0),test_call_find_and_type_and_verify(0),test_plan_runner_template_reference(0),test_function_binding(0)
  tools/check_confidence_gate.py:
    e: main
    main()
  tools/probe_native_host.py:
    e: run_short,read_os_release,probe,main
    run_short(cmd)
    read_os_release()
    probe()
    main()
  tools/probe_runtime.py:
    e: call_step,run_probe,main
    call_step(rt;step_id;uri;payload)
    run_probe(profile)
    main()
  tools/run_backend_matrix.py:
    e: to_markdown,main
    to_markdown(matrix)
    main()
  tools/run_native_lab_matrix.py:
    e: contract_check,build_matrix,confidence_gate,main
    contract_check()
    build_matrix()
    confidence_gate(matrix)
    main()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('urivision', '0.3.0', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 90, 'less').
project_file('docker/entrypoint-wayland.sh', 11, 'shell').
project_file('docker/entrypoint-x11-novnc.sh', 10, 'shell').
project_file('examples/function_binding_example.py', 19, 'python').
project_file('native/android/probe_android.sh', 19, 'shell').
project_file('native/ios/probe_ios.sh', 23, 'shell').
project_file('native/linux/probe_linux_display.sh', 32, 'shell').
project_file('native/linux/run_smoke.sh', 9, 'shell').
project_file('native/macos/probe_macos_ax.sh', 21, 'shell').
project_file('native/macos/run_smoke.sh', 8, 'shell').
project_file('project.sh', 66, 'shell').
project_file('src/urivision/__init__.py', 48, 'python').
project_file('src/urivision/bindings.py', 69, 'python').
project_file('src/urivision/capability.py', 90, 'python').
project_file('src/urivision/cli.py', 141, 'python').
project_file('src/urivision/compiler.py', 29, 'python').
project_file('src/urivision/dsl.py', 94, 'python').
project_file('src/urivision/llm_catalog.py', 16, 'python').
project_file('src/urivision/method_router.py', 145, 'python').
project_file('src/urivision/native_profiles.py', 428, 'python').
project_file('src/urivision/orchestrator.py', 96, 'python').
project_file('src/urivision/platforms.py', 139, 'python').
project_file('src/urivision/registry.py', 210, 'python').
project_file('src/urivision/resolver.py', 28, 'python').
project_file('src/urivision/runner_litellm.py', 55, 'python').
project_file('src/urivision/runtime.py', 514, 'python').
project_file('src/urivision/schemas.py', 100, 'python').
project_file('src/urivision/uri.py', 101, 'python').
project_file('src/urivision/validators.py', 39, 'python').
project_file('tests/test_backend_profiles.py', 38, 'python').
project_file('tests/test_dsl.py', 55, 'python').
project_file('tests/test_native_lab.py', 57, 'python').
project_file('tests/test_uri_runtime.py', 58, 'python').
project_file('tools/check_confidence_gate.py', 30, 'python').
project_file('tools/probe_native_host.py', 113, 'python').
project_file('tools/probe_runtime.py', 93, 'python').
project_file('tools/run_backend_matrix.py', 50, 'python').
project_file('tools/run_native_lab_matrix.py', 118, 'python').
project_file('tree.sh', 5, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/function_binding_example.py', 'add', 2, 1, 1).
python_function('src/urivision/__init__.py', 'run_source', 1, 1, 3).
python_function('src/urivision/__init__.py', 'run_file', 1, 1, 3).
python_function('src/urivision/__init__.py', 'run', 1, 1, 1).
python_function('src/urivision/bindings.py', 'uri_function', 1, 1, 5).
python_function('src/urivision/bindings.py', 'register_uri_function', 2, 2, 8).
python_function('src/urivision/bindings.py', 'register_module_uri_functions', 2, 4, 6).
python_function('src/urivision/cli.py', '_json_arg', 1, 4, 3).
python_function('src/urivision/cli.py', 'main', 1, 22, 28).
python_function('src/urivision/compiler.py', 'compile_prompt', 1, 4, 3).
python_function('src/urivision/dsl.py', '_parse_options', 1, 3, 2).
python_function('src/urivision/dsl.py', 'parse', 1, 19, 10).
python_function('src/urivision/llm_catalog.py', 'compile_runtime_prompt', 1, 2, 2).
python_function('src/urivision/llm_catalog.py', 'compile_runtime_tools', 1, 2, 2).
python_function('src/urivision/method_router.py', 'route_intent', 2, 12, 14).
python_function('src/urivision/method_router.py', 'route_matrix', 0, 3, 4).
python_function('src/urivision/native_profiles.py', 'list_native_targets', 0, 2, 1).
python_function('src/urivision/native_profiles.py', 'get_native_target', 1, 2, 3).
python_function('src/urivision/native_profiles.py', 'coverage_summary', 0, 9, 6).
python_function('src/urivision/native_profiles.py', 'detect_local_host', 0, 9, 5).
python_function('src/urivision/native_profiles.py', 'native_matrix_markdown', 1, 4, 6).
python_function('src/urivision/orchestrator.py', '_get_path', 2, 5, 4).
python_function('src/urivision/orchestrator.py', '_resolve_templates', 2, 9, 8).
python_function('src/urivision/orchestrator.py', '_check_expectation', 2, 8, 5).
python_function('src/urivision/orchestrator.py', 'run_plan', 1, 1, 2).
python_function('src/urivision/orchestrator.py', 'run_plan_file', 1, 1, 4).
python_function('src/urivision/platforms.py', 'list_backend_profiles', 0, 2, 1).
python_function('src/urivision/platforms.py', 'get_backend_profile', 1, 5, 4).
python_function('src/urivision/registry.py', '_json_type_ok', 2, 10, 1).
python_function('src/urivision/registry.py', 'validate_payload', 2, 12, 8).
python_function('src/urivision/registry.py', 'schema_from_signature', 1, 10, 3).
python_function('src/urivision/registry.py', 'pretty_json', 1, 1, 1).
python_function('src/urivision/resolver.py', 'model_id', 1, 1, 0).
python_function('src/urivision/resolver.py', 'artifact_path', 2, 6, 6).
python_function('src/urivision/resolver.py', 'label', 1, 2, 1).
python_function('src/urivision/runner_litellm.py', '_image_data_url', 2, 1, 4).
python_function('src/urivision/runner_litellm.py', 'run', 1, 4, 14).
python_function('src/urivision/runtime.py', '_schema', 2, 2, 0).
python_function('src/urivision/runtime.py', '_ok', 0, 1, 0).
python_function('src/urivision/runtime.py', '_default_tree', 0, 1, 0).
python_function('src/urivision/runtime.py', '_ensure_state', 1, 1, 2).
python_function('src/urivision/runtime.py', '_walk', 1, 3, 3).
python_function('src/urivision/runtime.py', '_find_element', 2, 14, 6).
python_function('src/urivision/runtime.py', 'build_default_registry', 0, 1, 27).
python_function('src/urivision/runtime.py', 'default_runtime', 0, 2, 2).
python_function('src/urivision/schemas.py', 'resolve_schema', 1, 2, 1).
python_function('src/urivision/uri.py', 'parse_uri', 1, 7, 8).
python_function('src/urivision/uri.py', 'normalize_uri', 1, 2, 2).
python_function('src/urivision/uri.py', '_match_segment', 3, 7, 4).
python_function('src/urivision/uri.py', 'match_uri', 2, 6, 4).
python_function('src/urivision/validators.py', '_scheme', 1, 2, 1).
python_function('src/urivision/validators.py', 'validate', 1, 14, 5).
python_function('tests/test_dsl.py', 'test_parse_reads_all_parts', 0, 7, 5).
python_function('tests/test_dsl.py', 'test_missing_emit_rejected', 0, 3, 6).
python_function('tests/test_dsl.py', 'test_bad_scheme_rejected', 0, 1, 4).
python_function('tests/test_dsl.py', 'test_non_image_rejected', 0, 1, 4).
python_function('tests/test_dsl.py', 'test_unknown_statement_rejected', 0, 1, 2).
python_function('tests/test_dsl.py', 'test_dry_run_compiles_call_without_model', 0, 5, 1).
python_function('tools/check_confidence_gate.py', 'main', 0, 9, 9).
python_function('tools/probe_native_host.py', 'run_short', 1, 2, 3).
python_function('tools/probe_native_host.py', 'read_os_release', 0, 4, 6).
python_function('tools/probe_native_host.py', 'probe', 0, 17, 9).
python_function('tools/probe_native_host.py', 'main', 0, 2, 9).
python_function('tools/probe_runtime.py', 'call_step', 4, 2, 7).
python_function('tools/probe_runtime.py', 'run_probe', 1, 9, 8).
python_function('tools/probe_runtime.py', 'main', 0, 3, 10).
python_function('tools/run_backend_matrix.py', 'to_markdown', 1, 4, 3).
python_function('tools/run_backend_matrix.py', 'main', 0, 4, 12).
python_function('tools/run_native_lab_matrix.py', 'contract_check', 0, 4, 7).
python_function('tools/run_native_lab_matrix.py', 'build_matrix', 0, 8, 10).
python_function('tools/run_native_lab_matrix.py', 'confidence_gate', 1, 5, 2).
python_function('tools/run_native_lab_matrix.py', 'main', 0, 1, 12).

% ── Python Classes ───────────────────────────────────────
python_class('src/urivision/capability.py', 'RuntimeContext').
python_method('RuntimeContext', 'emit', 1, 1, 1).
python_class('src/urivision/capability.py', 'Capability').
python_method('Capability', 'to_dict', 0, 2, 2).
python_method('Capability', 'to_llm_card', 0, 6, 3).
python_class('src/urivision/dsl.py', 'Model').
python_class('src/urivision/dsl.py', 'Process').
python_class('src/urivision/dsl.py', 'VuriSyntaxError').
python_class('src/urivision/method_router.py', 'RouteDecision').
python_method('RouteDecision', 'to_dict', 0, 1, 0).
python_class('src/urivision/native_profiles.py', 'NativeTargetProfile').
python_method('NativeTargetProfile', 'to_dict', 0, 1, 1).
python_class('src/urivision/orchestrator.py', 'PlanError').
python_class('src/urivision/orchestrator.py', 'PlanRunner').
python_method('PlanRunner', '__init__', 1, 2, 1).
python_method('PlanRunner', 'run', 1, 10, 9).
python_class('src/urivision/platforms.py', 'BackendProfile').
python_method('BackendProfile', 'to_dict', 0, 1, 1).
python_class('src/urivision/registry.py', 'UriDispatchError').
python_class('src/urivision/registry.py', 'PayloadValidationError').
python_class('src/urivision/registry.py', 'CapabilityRegistry').
python_method('CapabilityRegistry', '__init__', 0, 1, 0).
python_method('CapabilityRegistry', 'register', 2, 2, 2).
python_method('CapabilityRegistry', 'capability', 1, 1, 3).
python_method('CapabilityRegistry', 'find', 1, 3, 2).
python_method('CapabilityRegistry', 'call', 2, 6, 8).
python_method('CapabilityRegistry', 'all', 0, 1, 1).
python_method('CapabilityRegistry', 'catalog_json', 0, 2, 1).
python_method('CapabilityRegistry', 'catalog_markdown', 0, 2, 3).
python_method('CapabilityRegistry', 'catalog_prompt', 0, 1, 1).
python_method('CapabilityRegistry', 'tools_json', 0, 1, 0).
python_class('src/urivision/runtime.py', 'UriRuntime').
python_method('UriRuntime', '__init__', 1, 3, 2).
python_method('UriRuntime', 'call', 2, 3, 1).
python_method('UriRuntime', 'catalog', 1, 4, 4).
python_method('UriRuntime', 'explain', 1, 1, 1).
python_method('UriRuntime', 'trace', 0, 1, 1).
python_class('src/urivision/uri.py', 'UriParts').
python_method('UriParts', 'kind', 0, 2, 1).
python_method('UriParts', 'name', 0, 2, 0).
python_method('UriParts', 'area', 0, 2, 0).
python_class('src/urivision/validators.py', 'VuriValidationError').
python_class('tests/test_backend_profiles.py', 'BackendProfileTests').
python_method('BackendProfileTests', 'test_default_matrix_has_four_profiles', 0, 1, 3).
python_method('BackendProfileTests', 'test_platform_profile_capability', 0, 1, 4).
python_method('BackendProfileTests', 'test_health_check_for_all_matrix_profiles', 0, 2, 4).
python_method('BackendProfileTests', 'test_list_backend_profiles', 0, 3, 4).
python_class('tests/test_native_lab.py', 'NativeLabTests').
python_method('NativeLabTests', 'test_required_families_are_covered', 0, 2, 4).
python_method('NativeLabTests', 'test_each_profile_has_evidence_and_probes', 0, 2, 4).
python_method('NativeLabTests', 'test_method_router_selects_route_for_key_intents', 0, 2, 7).
python_method('NativeLabTests', 'test_route_matrix_has_all_profiles_and_intents', 0, 3, 6).
python_method('NativeLabTests', 'test_known_profile_lookup', 0, 1, 2).
python_class('tests/test_uri_runtime.py', 'UriRuntimeTests').
python_method('UriRuntimeTests', 'test_parse_and_match_uri', 0, 1, 3).
python_method('UriRuntimeTests', 'test_catalog_has_runtime_capabilities', 0, 2, 3).
python_method('UriRuntimeTests', 'test_call_find_and_type_and_verify', 0, 1, 3).
python_method('UriRuntimeTests', 'test_plan_runner_template_reference', 0, 1, 4).
python_method('UriRuntimeTests', 'test_function_binding', 0, 1, 5).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('test', '').
makefile_target('matrix', '').
makefile_target('native-matrix', '').
makefile_target('native-probe', '').
makefile_target('confidence', '').
makefile_target('docker-matrix', '').
makefile_target('docker-linux-x11', '').
makefile_target('docker-wayland', '').
makefile_target('docker-contract', '').
makefile_target('zip', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').
testql_scenario('generated-from-pytests.testql.toon.yaml', 'integration').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('testql-scenarios/generated-from-pytests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'PYTHONPATH=src:. python3 -m unittest discover -s tests -v').
sumd_workflow('matrix', 'manual').
sumd_workflow_step('matrix', 1, 'PYTHONPATH=src:. python3 tools/run_backend_matrix.py --out artifacts/backend-matrix.json --markdown artifacts/backend-matrix.md').
sumd_workflow('native-matrix', 'manual').
sumd_workflow_step('native-matrix', 1, 'PYTHONPATH=src:. python3 tools/run_native_lab_matrix.py --out artifacts/native-lab-matrix.json --markdown artifacts/native-lab-matrix.md --confidence artifacts/native-confidence-gate.md').
sumd_workflow('native-probe', 'manual').
sumd_workflow_step('native-probe', 1, 'PYTHONPATH=src:. python3 tools/probe_native_host.py --out artifacts/native-host-probe.json').
sumd_workflow('confidence', 'manual').
sumd_workflow_step('confidence', 1, 'PYTHONPATH=src:. python3 tools/check_confidence_gate.py artifacts/native-lab-matrix.json').
sumd_workflow('docker-matrix', 'manual').
sumd_workflow_step('docker-matrix', 1, 'docker compose -f docker/docker-compose.yml run --rm uri-runtime-matrix').
sumd_workflow('docker-linux-x11', 'manual').
sumd_workflow_step('docker-linux-x11', 1, 'docker compose -f docker/docker-compose.yml --profile linux-x11 up --build --abort-on-container-exit').
sumd_workflow('docker-wayland', 'manual').
sumd_workflow_step('docker-wayland', 1, 'docker compose -f docker/docker-compose.yml --profile linux-wayland up --build --abort-on-container-exit').
sumd_workflow('docker-contract', 'manual').
sumd_workflow_step('docker-contract', 1, 'docker compose -f docker/docker-compose.yml --profile contract up --build --abort-on-container-exit').
sumd_workflow('zip', 'manual').
sumd_workflow_step('zip', 1, 'cd .. && zip -qr urivision_native_test_lab.zip urivision -x \'urivision/venv/*\' -x \'urivision/.git/*\'').
```

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

## Intent

VURI — Visual URI Process Language plus URI-addressable runtime, Docker contracts and native OS test lab.
