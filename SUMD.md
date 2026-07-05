# VURI — Visual URI Process Language (`urivision`)

VURI — Visual URI Process Language: point at an image + model + aspects + decision question + result schema; get a DecisionCard (decision with evidence), not a description.

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `urivision`
- **version**: `0.1.0`
- **python_requires**: `>=3.10`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(2), app.doql.less, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: urivision;
  version: 0.1.0;
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

deploy {
  target: pip;
}

environment[name="local"] {
  runtime: python;
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

## Configuration

```yaml
project:
  name: urivision
  version: 0.1.0
  env: local
```

## Deployment

```bash markpact:run
pip install urivision

# development install
pip install -e .[dev]
```

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# urivision | 12f 503L | python:9,shell:2,less:1 | 2026-07-05
# stats: 21 func | 4 cls | 12 mod | CC̄=4.0 | critical:2 | cycles:0
# alerts[5]: CC parse=19; CC validate=14; CC test_parse_reads_all_parts=7; CC artifact_path=6; CC main=5
# hotspots[5]: run fan=14; main fan=11; parse fan=10; artifact_path fan=6; test_missing_emit_rejected fan=6
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[12]:
  app.doql.less,27
  project.sh,66
  src/urivision/__init__.py,34
  src/urivision/cli.py,29
  src/urivision/compiler.py,29
  src/urivision/dsl.py,94
  src/urivision/resolver.py,28
  src/urivision/runner_litellm.py,55
  src/urivision/schemas.py,42
  src/urivision/validators.py,39
  tests/test_dsl.py,55
  tree.sh,5
D:
  src/urivision/__init__.py:
    e: run_source,run_file,run
    run_source(text)
    run_file(path)
    run(text)
  src/urivision/cli.py:
    e: main
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
  src/urivision/resolver.py:
    e: model_id,artifact_path,label
    model_id(model)
    artifact_path(uri;roots)
    label(uri)
  src/urivision/runner_litellm.py:
    e: _image_data_url,run
    _image_data_url(path;mime)
    run(p)
  src/urivision/schemas.py:
    e: resolve_schema
    resolve_schema(uri)
  src/urivision/validators.py:
    e: _scheme,validate,VuriValidationError
    VuriValidationError:
    _scheme(uri)
    validate(p)
  tests/test_dsl.py:
    e: test_parse_reads_all_parts,test_missing_emit_rejected,test_bad_scheme_rejected,test_non_image_rejected,test_unknown_statement_rejected,test_dry_run_compiles_call_without_model
    test_parse_reads_all_parts()
    test_missing_emit_rejected()
    test_bad_scheme_rejected()
    test_non_image_rejected()
    test_unknown_statement_rejected()
    test_dry_run_compiles_call_without_model()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
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
```

## Call Graph

*13 nodes · 11 edges · 8 modules · CC̄=4.4*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `parse` *(in src.urivision.dsl)* | 19 ⚠ | 1 | 35 | **36** |
| `run` *(in src.urivision.runner_litellm)* | 4 | 0 | 17 | **17** |
| `main` *(in src.urivision.cli)* | 5 | 0 | 13 | **13** |
| `validate` *(in src.urivision.validators)* | 14 ⚠ | 1 | 10 | **11** |
| `artifact_path` *(in src.urivision.resolver)* | 6 | 2 | 8 | **10** |
| `compile_prompt` *(in src.urivision.compiler)* | 4 | 1 | 6 | **7** |
| `run_source` *(in src.urivision)* | 1 | 2 | 3 | **5** |
| `label` *(in src.urivision.resolver)* | 2 | 3 | 1 | **4** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/if-uri/urivision
# generated in 0.02s
# nodes: 13 | edges: 11 | modules: 8
# CC̄=4.4

HUBS[20]:
  src.urivision.dsl.parse
    CC=19  in:1  out:35  total:36
  src.urivision.runner_litellm.run
    CC=4  in:0  out:17  total:17
  src.urivision.cli.main
    CC=5  in:0  out:13  total:13
  src.urivision.validators.validate
    CC=14  in:1  out:10  total:11
  src.urivision.resolver.artifact_path
    CC=6  in:2  out:8  total:10
  src.urivision.compiler.compile_prompt
    CC=4  in:1  out:6  total:7
  src.urivision.run_source
    CC=1  in:2  out:3  total:5
  src.urivision.resolver.label
    CC=2  in:3  out:1  total:4
  src.urivision.run_file
    CC=1  in:1  out:3  total:4
  src.urivision.validators._scheme
    CC=2  in:1  out:1  total:2
  src.urivision.schemas.resolve_schema
    CC=2  in:1  out:1  total:2
  src.urivision.resolver.model_id
    CC=1  in:1  out:0  total:1
  src.urivision.run
    CC=1  in:0  out:1  total:1

MODULES:
  src.urivision  [3 funcs]
    run  CC=1  out:1
    run_file  CC=1  out:3
    run_source  CC=1  out:3
  src.urivision.cli  [1 funcs]
    main  CC=5  out:13
  src.urivision.compiler  [1 funcs]
    compile_prompt  CC=4  out:6
  src.urivision.dsl  [1 funcs]
    parse  CC=19  out:35
  src.urivision.resolver  [3 funcs]
    artifact_path  CC=6  out:8
    label  CC=2  out:1
    model_id  CC=1  out:0
  src.urivision.runner_litellm  [1 funcs]
    run  CC=4  out:17
  src.urivision.schemas  [1 funcs]
    resolve_schema  CC=2  out:1
  src.urivision.validators  [2 funcs]
    _scheme  CC=2  out:1
    validate  CC=14  out:10

EDGES:
  src.urivision.cli.main → src.urivision.run_file
  src.urivision.runner_litellm.run → src.urivision.resolver.model_id
  src.urivision.runner_litellm.run → src.urivision.schemas.resolve_schema
  src.urivision.runner_litellm.run → src.urivision.compiler.compile_prompt
  src.urivision.runner_litellm.run → src.urivision.resolver.artifact_path
  src.urivision.run_source → src.urivision.validators.validate
  src.urivision.run_source → src.urivision.dsl.parse
  src.urivision.run_file → src.urivision.run_source
  src.urivision.run → src.urivision.run_source
  src.urivision.validators.validate → src.urivision.validators._scheme
  src.urivision.compiler.compile_prompt → src.urivision.resolver.label
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Intent

VURI — Visual URI Process Language: point at an image + model + aspects + decision question + result schema; get a DecisionCard (decision with evidence), not a description.
