# VURI — Visual URI Process Language (`urivision`)

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `urivision`
- **version**: `0.1.0`
- **python_requires**: `>=3.10`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, testql(2), app.doql.less, project/(5 analysis files)

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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 16f 455L | python:8,txt:5,shell:2,toml:1 | 2026-07-05
# generated in 0.00s
# CC̅=4.4 | critical:1/15 | dups:0 | cycles:0

HEALTH[1]:
  🟡 CC    parse CC=19 (limit:15)

REFACTOR[1]:
  1. split 1 high-CC methods  (CC>15)

PIPELINES[3]:
  [1] Src [main]: main → run_file → run_source → validate → ...(1 more)
      PURITY: 100% pure
  [2] Src [run]: run → model_id
      PURITY: 100% pure
  [3] Src [run]: run → run_source → validate → _scheme
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=4.4    ←in:1  →out:2
  │ !! dsl                         93L  3C    2m  CC=19     ←1
  │ runner_litellm              54L  0C    2m  CC=4      ←0
  │ schemas                     41L  0C    1m  CC=2      ←1
  │ validators                  38L  1C    2m  CC=14     ←1
  │ __init__                    33L  0C    3m  CC=1      ←1
  │ cli                         28L  0C    1m  CC=5      ←0
  │ compiler                    28L  0C    1m  CC=4      ←1
  │ resolver                    27L  0C    3m  CC=6      ←2
  │ SOURCES.txt                 17L  0C    0m  CC=0.0    ←0
  │ requires.txt                 3L  0C    0m  CC=0.0    ←0
  │ entry_points.txt             2L  0C    0m  CC=0.0    ←0
  │ dependency_links.txt         1L  0C    0m  CC=0.0    ←0
  │ top_level.txt                1L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ project.sh                  66L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              19L  0C    0m  CC=0.0    ←0
  │ tree.sh                      4L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                           src  src.urivision
            src             ──              2
  src.urivision              1             ──
  CYCLES: none

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 8f 342L | 2026-07-05

SUMMARY:
  files_scanned: 8
  total_lines:   342
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       45
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 15 func | 8f | 2026-07-05
# generated in 0.00s

NEXT[1] (ranked by impact):
  [1] !  SPLIT-FUNC      parse  CC=19  fan=16
      WHY: CC=19 exceeds 15
      EFFORT: ~1h  IMPACT: 304


RISKS[0]: none

METRICS-TARGET:
  CC̄:          4.4 → ≤3.1
  max-CC:      19 → ≤9
  god-modules: 0 → 0
  high-CC(≥15): 1 → ≤0
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
  (first run — no previous data)
```

## Intent

VURI — Visual URI Process Language: point at an image + model + aspects + decision question + result schema; get a DecisionCard (decision with evidence), not a description.
