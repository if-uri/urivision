# System Architecture Analysis
<!-- generated in 0.00s -->

## Overview

- **Project**: /home/tom/github/if-uri/urivision
- **Primary Language**: python
- **Languages**: python: 24, shell: 10, json: 6, yaml: 4, toml: 1
- **Analysis Mode**: static
- **Total Functions**: 90
- **Total Classes**: 16
- **Modules**: 49
- **Entry Points**: 35

## Architecture by Module

### src.urivision.registry
- **Functions**: 14
- **Classes**: 3
- **File**: `registry.py`

### src.urivision.runtime
- **Functions**: 13
- **Classes**: 1
- **File**: `runtime.py`

### src.urivision.orchestrator
- **Functions**: 7
- **Classes**: 2
- **File**: `orchestrator.py`

### src.urivision.native_profiles
- **Functions**: 6
- **Classes**: 1
- **File**: `native_profiles.py`

### tools.run_native_lab_matrix
- **Functions**: 4
- **File**: `run_native_lab_matrix.py`

### tools.probe_native_host
- **Functions**: 4
- **File**: `probe_native_host.py`

### src.urivision.uri
- **Functions**: 4
- **Classes**: 1
- **File**: `uri.py`

### src.urivision.resolver
- **Functions**: 3
- **File**: `resolver.py`

### src.urivision
- **Functions**: 3
- **File**: `__init__.py`

### tools.probe_runtime
- **Functions**: 3
- **File**: `probe_runtime.py`

### src.urivision.bindings
- **Functions**: 3
- **File**: `bindings.py`

### src.urivision.method_router
- **Functions**: 3
- **Classes**: 1
- **File**: `method_router.py`

### src.urivision.platforms
- **Functions**: 3
- **Classes**: 1
- **File**: `platforms.py`

### src.urivision.capability
- **Functions**: 3
- **Classes**: 2
- **File**: `capability.py`

### src.urivision.runner_litellm
- **Functions**: 2
- **File**: `runner_litellm.py`

### src.urivision.dsl
- **Functions**: 2
- **Classes**: 3
- **File**: `dsl.py`

### tools.run_backend_matrix
- **Functions**: 2
- **File**: `run_backend_matrix.py`

### src.urivision.validators
- **Functions**: 2
- **Classes**: 1
- **File**: `validators.py`

### src.urivision.llm_catalog
- **Functions**: 2
- **File**: `llm_catalog.py`

### src.urivision.cli
- **Functions**: 2
- **File**: `cli.py`

## Key Entry Points

Main execution flows into the system:

### src.urivision.cli.main
- **Calls**: argparse.ArgumentParser, ap.add_subparsers, sub.add_parser, r.add_argument, r.add_argument, r.add_argument, sub.add_parser, c.add_argument

### tools.run_native_lab_matrix.main
- **Calls**: argparse.ArgumentParser, ap.add_argument, ap.add_argument, ap.add_argument, ap.parse_args, tools.run_native_lab_matrix.build_matrix, None.parent.mkdir, None.write_text

### tools.run_backend_matrix.main
- **Calls**: argparse.ArgumentParser, ap.add_argument, ap.add_argument, ap.add_argument, ap.parse_args, Path, out.parent.mkdir, out.write_text

### src.urivision.runner_litellm.run
> Wykonaj proces VURI: obraz+prompt → model → DecisionCard (zwalidowany schematem).
dry_run zwraca wkompilowane wywołanie bez uderzania w model (do test
- **Calls**: src.urivision.resolver.model_id, src.urivision.schemas.resolve_schema, src.urivision.compiler.compile_prompt, src.urivision.resolver.artifact_path, None.get, completion, json.loads, src.urivision.resolver.artifact_path

### src.urivision.orchestrator.PlanRunner.run
- **Calls**: enumerate, PlanError, src.urivision.orchestrator._resolve_templates, self.runtime.call, src.urivision.orchestrator._check_expectation, trace.append, self.runtime.trace, isinstance

### tools.probe_runtime.main
- **Calls**: argparse.ArgumentParser, ap.add_argument, ap.add_argument, ap.parse_args, tools.probe_runtime.run_probe, json.dumps, native.linux.probe_linux_display.print, Path

### tools.check_confidence_gate.main
- **Calls**: argparse.ArgumentParser, ap.add_argument, ap.add_argument, ap.parse_args, json.loads, native.linux.probe_linux_display.print, None.read_text, src.urivision.registry.CapabilityRegistry.all

### tools.probe_native_host.main
- **Calls**: argparse.ArgumentParser, ap.add_argument, ap.parse_args, tools.probe_native_host.probe, json.dumps, native.linux.probe_linux_display.print, None.parent.mkdir, None.write_text

### src.urivision.registry.CapabilityRegistry.call
- **Calls**: self.find, src.urivision.registry.validate_payload, ctx.emit, ctx.emit, RuntimeContext, cap.handler, cap.to_dict, UriDispatchError

### src.urivision.native_profiles.NativeTargetProfile.to_dict
- **Calls**: list, list, list, list, list, list, list, list

### src.urivision.capability.Capability.to_llm_card
- **Calls**: self.input_schema.get, self.input_schema.get, None.join, None.join, ex.get, ex.get, props.items, spec.get

### src.urivision.bindings.register_module_uri_functions
- **Calls**: None.values, vars, callable, registered.append, getattr, src.urivision.bindings.register_uri_function

### src.urivision.platforms.BackendProfile.to_dict
- **Calls**: list, list, list, list, list

### src.urivision.runtime.UriRuntime.catalog
- **Calls**: self.registry.catalog_json, self.registry.catalog_markdown, self.registry.catalog_prompt, self.registry.tools_json

### src.urivision.registry.CapabilityRegistry.capability
- **Calls**: self.register, Capability, src.urivision.registry.schema_from_signature

### src.urivision.registry.CapabilityRegistry.catalog_markdown
- **Calls**: lines.append, None.join, cap.to_llm_card

### src.urivision.registry.CapabilityRegistry.find
- **Calls**: UriDispatchError, src.urivision.uri.match_uri

### src.urivision.llm_catalog.compile_runtime_prompt
- **Calls**: runtime.catalog, src.urivision.runtime.default_runtime

### src.urivision.llm_catalog.compile_runtime_tools
- **Calls**: runtime.catalog, src.urivision.runtime.default_runtime

### src.urivision.uri.normalize_uri
- **Calls**: src.urivision.uri.parse_uri, None.join

### src.urivision.runtime.UriRuntime.__init__
- **Calls**: src.urivision.runtime.build_default_registry, RuntimeContext

### src.urivision.capability.Capability.to_dict
- **Calls**: getattr, str

### src.urivision.registry.CapabilityRegistry.catalog_json
- **Calls**: c.to_dict

### src.urivision.registry.CapabilityRegistry.catalog_prompt
- **Calls**: self.catalog_markdown

### src.urivision.registry.pretty_json
- **Calls**: json.dumps

### src.urivision.run
- **Calls**: src.urivision.run_source

### src.urivision.orchestrator.PlanRunner.__init__
- **Calls**: src.urivision.runtime.default_runtime

### examples.function_binding_example.add
- **Calls**: src.urivision.bindings.uri_function

### src.urivision.runtime.UriRuntime.call
- **Calls**: self.registry.call

### src.urivision.runtime.UriRuntime.explain
- **Calls**: self.call

## Process Flows

Key execution flows identified:

### Flow 1: main
```
main [src.urivision.cli]
```

### Flow 2: run
```
run [src.urivision.runner_litellm]
  └─ →> model_id
  └─ →> artifact_path
  └─ →> resolve_schema
```

### Flow 3: call
```
call [src.urivision.registry.CapabilityRegistry]
  └─ →> validate_payload
```

### Flow 4: to_dict
```
to_dict [src.urivision.native_profiles.NativeTargetProfile]
```

### Flow 5: to_llm_card
```
to_llm_card [src.urivision.capability.Capability]
```

### Flow 6: register_module_uri_functions
```
register_module_uri_functions [src.urivision.bindings]
```

### Flow 7: catalog
```
catalog [src.urivision.runtime.UriRuntime]
```

### Flow 8: capability
```
capability [src.urivision.registry.CapabilityRegistry]
  └─ →> schema_from_signature
```

### Flow 9: catalog_markdown
```
catalog_markdown [src.urivision.registry.CapabilityRegistry]
```

### Flow 10: find
```
find [src.urivision.registry.CapabilityRegistry]
  └─ →> match_uri
      └─> parse_uri
      └─> parse_uri
```

## Key Classes

### src.urivision.registry.CapabilityRegistry
- **Methods**: 10
- **Key Methods**: src.urivision.registry.CapabilityRegistry.__init__, src.urivision.registry.CapabilityRegistry.register, src.urivision.registry.CapabilityRegistry.capability, src.urivision.registry.CapabilityRegistry.find, src.urivision.registry.CapabilityRegistry.call, src.urivision.registry.CapabilityRegistry.all, src.urivision.registry.CapabilityRegistry.catalog_json, src.urivision.registry.CapabilityRegistry.catalog_markdown, src.urivision.registry.CapabilityRegistry.catalog_prompt, src.urivision.registry.CapabilityRegistry.tools_json

### src.urivision.runtime.UriRuntime
- **Methods**: 5
- **Key Methods**: src.urivision.runtime.UriRuntime.__init__, src.urivision.runtime.UriRuntime.call, src.urivision.runtime.UriRuntime.catalog, src.urivision.runtime.UriRuntime.explain, src.urivision.runtime.UriRuntime.trace

### src.urivision.uri.UriParts
- **Methods**: 3
- **Key Methods**: src.urivision.uri.UriParts.kind, src.urivision.uri.UriParts.name, src.urivision.uri.UriParts.area

### src.urivision.orchestrator.PlanRunner
- **Methods**: 2
- **Key Methods**: src.urivision.orchestrator.PlanRunner.__init__, src.urivision.orchestrator.PlanRunner.run

### src.urivision.capability.Capability
- **Methods**: 2
- **Key Methods**: src.urivision.capability.Capability.to_dict, src.urivision.capability.Capability.to_llm_card

### src.urivision.native_profiles.NativeTargetProfile
- **Methods**: 1
- **Key Methods**: src.urivision.native_profiles.NativeTargetProfile.to_dict

### src.urivision.method_router.RouteDecision
- **Methods**: 1
- **Key Methods**: src.urivision.method_router.RouteDecision.to_dict

### src.urivision.platforms.BackendProfile
- **Methods**: 1
- **Key Methods**: src.urivision.platforms.BackendProfile.to_dict

### src.urivision.capability.RuntimeContext
> Execution context passed to every capability handler.
- **Methods**: 1
- **Key Methods**: src.urivision.capability.RuntimeContext.emit

### src.urivision.dsl.Model
- **Methods**: 0

### src.urivision.dsl.Process
- **Methods**: 0

### src.urivision.dsl.VuriSyntaxError
- **Methods**: 0
- **Inherits**: ValueError

### src.urivision.registry.UriDispatchError
- **Methods**: 0
- **Inherits**: RuntimeError

### src.urivision.registry.PayloadValidationError
- **Methods**: 0
- **Inherits**: ValueError

### src.urivision.validators.VuriValidationError
- **Methods**: 0
- **Inherits**: ValueError

### src.urivision.orchestrator.PlanError
- **Methods**: 0
- **Inherits**: ValueError

## Data Transformation Functions

Key functions that process and transform data:

### src.urivision.dsl._parse_options
- **Output to**: v.strip, _OPT.findall

### src.urivision.dsl.parse
> Parsuj źródło .vuri → AST procesu. Rzuca VuriSyntaxError na niepoprawnej instrukcji.
- **Output to**: Process, text.splitlines, None.strip, line.partition, rest.strip

### src.urivision.registry.validate_payload
- **Output to**: schema.get, schema.get, payload.items, schema.get, isinstance

### src.urivision.validators.validate
- **Output to**: VuriValidationError, src.urivision.validators._scheme, p.input_mime.startswith, VuriValidationError, p.output_schema.startswith

### src.urivision.uri.parse_uri
- **Output to**: urlparse, tuple, UriParts, ValueError, ValueError

## Behavioral Patterns

### recursion__resolve_templates
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: src.urivision.orchestrator._resolve_templates

### recursion__walk
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: src.urivision.runtime._walk

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `src.urivision.runtime.build_default_registry` - 187 calls
- `src.urivision.cli.main` - 78 calls
- `tools.probe_runtime.run_probe` - 39 calls
- `src.urivision.dsl.parse` - 35 calls
- `tools.probe_native_host.probe` - 31 calls
- `tools.run_native_lab_matrix.main` - 20 calls
- `src.urivision.registry.validate_payload` - 18 calls
- `tools.run_backend_matrix.main` - 18 calls
- `src.urivision.method_router.route_intent` - 18 calls
- `src.urivision.runner_litellm.run` - 17 calls
- `src.urivision.orchestrator.PlanRunner.run` - 17 calls
- `tools.run_backend_matrix.to_markdown` - 13 calls
- `src.urivision.native_profiles.detect_local_host` - 13 calls
- `tools.run_native_lab_matrix.build_matrix` - 12 calls
- `tools.probe_runtime.main` - 12 calls
- `src.urivision.native_profiles.native_matrix_markdown` - 11 calls
- `tools.check_confidence_gate.main` - 10 calls
- `tools.run_native_lab_matrix.contract_check` - 10 calls
- `tools.probe_native_host.main` - 10 calls
- `src.urivision.validators.validate` - 10 calls
- `src.urivision.registry.CapabilityRegistry.call` - 9 calls
- `src.urivision.bindings.register_uri_function` - 9 calls
- `src.urivision.native_profiles.NativeTargetProfile.to_dict` - 9 calls
- `src.urivision.uri.parse_uri` - 9 calls
- `src.urivision.resolver.artifact_path` - 8 calls
- `tools.probe_runtime.call_step` - 8 calls
- `src.urivision.capability.Capability.to_llm_card` - 8 calls
- `tools.probe_native_host.read_os_release` - 7 calls
- `src.urivision.uri.match_uri` - 7 calls
- `src.urivision.compiler.compile_prompt` - 6 calls
- `src.urivision.bindings.register_module_uri_functions` - 6 calls
- `src.urivision.native_profiles.coverage_summary` - 6 calls
- `src.urivision.bindings.uri_function` - 5 calls
- `src.urivision.method_router.route_matrix` - 5 calls
- `src.urivision.platforms.BackendProfile.to_dict` - 5 calls
- `src.urivision.platforms.get_backend_profile` - 5 calls
- `tools.run_native_lab_matrix.confidence_gate` - 4 calls
- `src.urivision.orchestrator.run_plan_file` - 4 calls
- `src.urivision.runtime.UriRuntime.catalog` - 4 calls
- `src.urivision.registry.CapabilityRegistry.capability` - 3 calls

## System Interactions

How components interact:

```mermaid
graph TD
    main --> ArgumentParser
    main --> add_subparsers
    main --> add_parser
    main --> add_argument
    main --> parse_args
    run --> model_id
    run --> resolve_schema
    run --> compile_prompt
    run --> artifact_path
    run --> get
    run --> enumerate
    run --> PlanError
    run --> _resolve_templates
    run --> call
    run --> _check_expectation
    main --> run_probe
    main --> loads
    main --> probe
    main --> dumps
    call --> find
    call --> validate_payload
    call --> emit
    call --> RuntimeContext
    to_dict --> list
    to_llm_card --> get
    to_llm_card --> join
    register_module_uri_ --> values
    register_module_uri_ --> vars
    register_module_uri_ --> callable
    register_module_uri_ --> append
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.