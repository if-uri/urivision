# Dokumentacja refaktoryzacji: URI Runtime Control Plane

## Diagnoza

Dotychczasowa ścieżka `urivision` jest dobra dla jednego typu procesu: obraz → prompt vision → DecisionCard. W repo widać już właściwy kierunek: proces `.vuri` używa adresów `view://`, `llm://`, `artifact://`, `aspect://`, `schema://`, `policy://`, a nie bezpośrednich importów. Ten sam wzorzec trzeba przenieść na funkcje wykonawcze: screenshot, OCR, element lookup, focus, type, click, DOM fill, KVM batch, HID.

Największy dług architektoniczny przy kontroli desktopu to nie brak jednej biblioteki do myszy. To brak jawnego, maszynowo opisanego katalogu zdolności. Bez tego LLM widzi „kod” albo „prompt”, ale nie widzi stabilnych funkcji systemu.

## Docelowy model

Każda funkcja wykonawcza ma być capability:

```json
{
  "uri_pattern": "input://{target}/keyboard/command/type",
  "kind": "command",
  "title": "Type text through keyboard backend",
  "description": "Wysyła tekst przez backend klawiatury. Używać po focus/locator i zawsze z postcondition verify.",
  "input_schema": {
    "type": "object",
    "required": ["text"],
    "properties": {
      "text": {"type": "string"}
    }
  },
  "side_effects": [
    "sends keyboard input",
    "may type into wrong focused element if focus is stale"
  ],
  "postconditions": [
    "expected text visible or value changed"
  ],
  "safety": "needs-verification"
}
```

LLM nie musi znać importu Pythona. Ma znać URI, opis, argumenty, ryzyko i postcondition.

## Zasada semantyczna

Nie robimy jednego wielkiego `control_computer()`.

Robimy małe, jawne, adresowalne funkcje:

```txt
runtime://local/capabilities/query/list
ui://local/tree/query/snapshot
ui://local/element/query/find
ui://local/element/command/focus
ui://local/element/command/press
browser://chrome/element/command/fill
view://local/screen/query/text
vision://local/screen/command/parse
input://local/keyboard/command/type
input://local/pointer/command/click
kvm://local/input/command/task_run
guard://local/batch/command/run
```

## Kolejność refaktoryzacji

### Etap 1 — opakować istniejące funkcje

Nie przepisywać wszystkiego naraz. Najpierw dodać `@uri_function` do istniejących funkcji.

```python
@uri_function(
    "kvm://{target}/input/command/task_run",
    title="Run batched KVM input steps",
    description="Batch input actions over KVM/VNC/HID-like channel.",
    kind="command",
)
def task_run(steps: list) -> dict:
    ...
```

Potem zarejestrować moduł:

```python
registry = CapabilityRegistry()
register_module_uri_functions(registry, kvm_module)
```

Efekt: runtime i LLM zaczynają widzieć funkcje jako URI, nawet jeśli implementacja nadal jest stara.

### Etap 2 — oddzielić kontrakt od adaptera

Docelowy podział:

```txt
capability contract      stable
adapter implementation   replaceable
transport                replaceable
trace                    common
```

Przykład:

```txt
input://local/keyboard/command/type
  ├─ WindowsAdapter.SendInput
  ├─ MacAdapter.CGEvent
  ├─ X11Adapter.xdotool
  ├─ WaylandAdapter.libei/ydotool/portal
  ├─ KvmAdapter.RFB
  └─ HidAdapter.RP2040
```

URI zostaje ten sam, backend się zmienia.

### Etap 3 — dodać capability discovery

Każdy host/target musi umieć odpowiedzieć:

```txt
runtime://target/capabilities/query/list
```

Wynik ma mówić nie tylko „co istnieje”, ale też „czego brakuje”:

```json
{
  "target": "fedora-wayland",
  "capabilities": [...],
  "limitations": [
    "global pointer coordinates unavailable",
    "requires portal permission",
    "keyboard injection limited"
  ]
}
```

### Etap 4 — wymusić verify-before-act

Każdy command z ryzykiem musi mieć postcondition:

```txt
input://.../type      → verify text/value
pointer://.../click   → verify UI state changed
kvm://.../task_run    → verify screen/text/tree
browser://.../fill    → verify DOM value
```

Kruche akcje powinny iść przez:

```txt
guard://target/batch/command/run
```

### Etap 5 — dodać method router

Router powinien wybierać metodę według priorytetu:

```txt
browser:// > ui:// native action > ui:// focus+keyboard > vision:// locate > input:// pointer > kvm:// > hid://
```

Nie odwrotnie.

## Dlaczego wcześniejsze próby trwały długo

1. Zrzut/OCR to kosztowna pętla, zwłaszcza gdy każde sprawdzenie robi osobny capture.
2. Mysz/klawiatura są stanowe: fokus, aktywne okno, modal, animacja i timing zmieniają wynik.
3. Bez DOM/accessibility nie wiadomo, czy tekst trafił do właściwego pola.
4. Bez postcondition agent może uznać sukces, mimo że akcja nie zmieniła UI.
5. noVNC/X11 jest prostsze niż Windows/macOS/Wayland, więc test na noVNC daje fałszywe poczucie prostoty.

## Co jeszcze poprawić w następnym sprincie

### 1. Adapter browser/CDP

Największy zysk dla portali webowych i Electron.

URI:

```txt
browser://target/dom/query/snapshot
browser://target/element/query/find
browser://target/element/command/click
browser://target/element/command/fill
browser://target/network/query/state
```

### 2. Adapter accessibility

Windows UIA, macOS AX, Linux AT-SPI.

URI:

```txt
ui://target/tree/query/snapshot
ui://target/element/query/find
ui://target/element/command/press
ui://target/element/command/set-value
```

### 3. OCR worker i crop

Nie OCR całego ekranu za każdym razem.

URI:

```txt
view://target/screenshot/query/capture
view://target/screen/query/text
artifact://image/crop/command/run
```

### 4. Warm screencast

Zamiast zimnego screena na każde żądanie: ciepły strumień klatek z cache.

URI:

```txt
view://target/screencast/command/start
view://target/screencast/query/latest-frame
view://target/screencast/command/stop
```

### 5. Trace store

Każda akcja powinna zostawiać ślad:

```txt
event://target/trace/command/append
event://target/trace/query/list
```

Trace musi zawierać: URI, payload, wynik, czas, screenshot hash, postcondition.

## Kryteria gotowości

Refaktoryzacja jest gotowa, gdy:

- LLM potrafi pobrać katalog przez `runtime://.../capabilities/query/list`.
- Każda funkcja ma URI, opis, input_schema, output_schema i safety.
- Plany używają URI, nie importów Pythona.
- Akcje kruche mają postcondition.
- Backend można wymienić bez zmiany planu.
- Jest trace z każdego kroku.
- Da się uruchomić plan w `--dry-run` bez realnego OS.

## Minimalny plan wdrożenia na repo

1. Wrzucić moduły `uri.py`, `capability.py`, `registry.py`, `runtime.py`, `orchestrator.py`, `bindings.py`.
2. Dodać CLI: `catalog`, `explain`, `call`, `plan`.
3. Oznaczyć istniejące funkcje connectora przez `@uri_function`.
4. Dodać `runtime://.../capabilities/query/list` jako pierwszą funkcję każdego connectora.
5. Dodać `guard://.../batch/command/run` jako obowiązkowy wrapper dla batch input.
6. Dopiero potem optymalizować OCR/crop/screencast.

## Najważniejsza decyzja projektowa

Kontrakt URI jest stabilniejszy niż backend.

To znaczy, że nie projektujemy pod `pyautogui`, `xdotool`, `UIA`, `noVNC` ani `LiteLLM`. Projektujemy pod semantyczne polecenia:

```txt
znajdź element → ustaw fokus → wykonaj akcję → zweryfikuj skutek
```

a dopiero runtime wybiera backend.
