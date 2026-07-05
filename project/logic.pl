% ── Project Metadata ─────────────────────────────────────
project_metadata('urivision', '0.1.0', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 27, 'less').
project_file('project.sh', 66, 'shell').
project_file('src/urivision/__init__.py', 34, 'python').
project_file('src/urivision/cli.py', 29, 'python').
project_file('src/urivision/compiler.py', 29, 'python').
project_file('src/urivision/dsl.py', 94, 'python').
project_file('src/urivision/resolver.py', 28, 'python').
project_file('src/urivision/runner_litellm.py', 55, 'python').
project_file('src/urivision/schemas.py', 42, 'python').
project_file('src/urivision/validators.py', 39, 'python').
project_file('tests/test_dsl.py', 55, 'python').
project_file('tree.sh', 5, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('src/urivision/__init__.py', 'run_source', 1, 1, 3).
python_function('src/urivision/__init__.py', 'run_file', 1, 1, 3).
python_function('src/urivision/__init__.py', 'run', 1, 1, 1).
python_function('src/urivision/cli.py', 'main', 1, 5, 11).
python_function('src/urivision/compiler.py', 'compile_prompt', 1, 4, 3).
python_function('src/urivision/dsl.py', '_parse_options', 1, 3, 2).
python_function('src/urivision/dsl.py', 'parse', 1, 19, 10).
python_function('src/urivision/resolver.py', 'model_id', 1, 1, 0).
python_function('src/urivision/resolver.py', 'artifact_path', 2, 6, 6).
python_function('src/urivision/resolver.py', 'label', 1, 2, 1).
python_function('src/urivision/runner_litellm.py', '_image_data_url', 2, 1, 4).
python_function('src/urivision/runner_litellm.py', 'run', 1, 4, 14).
python_function('src/urivision/schemas.py', 'resolve_schema', 1, 2, 1).
python_function('src/urivision/validators.py', '_scheme', 1, 2, 1).
python_function('src/urivision/validators.py', 'validate', 1, 14, 5).
python_function('tests/test_dsl.py', 'test_parse_reads_all_parts', 0, 7, 5).
python_function('tests/test_dsl.py', 'test_missing_emit_rejected', 0, 3, 6).
python_function('tests/test_dsl.py', 'test_bad_scheme_rejected', 0, 1, 4).
python_function('tests/test_dsl.py', 'test_non_image_rejected', 0, 1, 4).
python_function('tests/test_dsl.py', 'test_unknown_statement_rejected', 0, 1, 2).
python_function('tests/test_dsl.py', 'test_dry_run_compiles_call_without_model', 0, 5, 1).

% ── Python Classes ───────────────────────────────────────
python_class('src/urivision/dsl.py', 'Model').
python_class('src/urivision/dsl.py', 'Process').
python_class('src/urivision/dsl.py', 'VuriSyntaxError').
python_class('src/urivision/validators.py', 'VuriValidationError').

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────

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

