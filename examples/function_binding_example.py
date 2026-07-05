from urivision import CapabilityRegistry, register_uri_function, uri_function


@uri_function(
    "math://local/add/command/run",
    title="Add two integers",
    description="Przykład migracji zwykłej funkcji Python do wywołania przez URI.",
    kind="command",
)
def add(a: int, b: int) -> dict:
    return {"ok": True, "value": a + b}


if __name__ == "__main__":
    registry = CapabilityRegistry()
    register_uri_function(registry, add)
    print(registry.catalog_markdown())
    print(registry.call("math://local/add/command/run", {"a": 2, "b": 3}))
