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

