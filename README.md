# urivision 0.3 — VURI + URI Runtime + Native Test Lab

Ten pakiet zachowuje dotychczasowy rdzeń `urivision` dla procesów `.vuri`, ale dodaje drugą warstwę: **URI Runtime Control Plane**. Celem jest przejście z reużycia przez import Pythona na reużycie przez **kontrakty URI**, które LLM może łatwo zrozumieć, katalogować i orkiestracyjnie wywoływać.

## Rdzeń VURI — procesy `.vuri`

Lekki, szybki model **analizy i kontroli obrazu**. Zamiast długiego promptu wskazujesz
**obraz + model + aspekty + pytanie decyzyjne + schemat wyniku** — a proces kompiluje się do
wywołania modelu vision i zwraca **DecisionCard: decyzję z dowodami, nie opis**.

```txt
proc   view://local/screenshot/query/decision-card
use    llm://gemini/gemini-3.5-flash as vision(reasoning=low,json=strict)
read   artifact://screenshots/prototyp3d/home.png as image/png
inspect image for aspect://ui/layout, aspect://ui/cta, aspect://ui/risk
decide "Czy ekran można pokazać klientowi bez poprawek?"
emit   artifact://reports/prototyp3d/home.decision.json as schema://vision/decision-card.v1
policy policy://vision/no-guessing, policy://vision/evidence-required
```

Każda część to **adres URI** — reużycie zdolności przez URI, nie import Pythona.
`view:// proc/query` · `artifact:// obraz/raport` · `llm:// model` · `aspect:// co ocenić` ·
`schema:// kontrakt wyniku` · `policy:// zasady jakości` · `event:// ślad wykonania`.

```bash
urivision run examples/screen-review.vuri --dry-run          # kompiluje wywołanie (bez modelu)
urivision run examples/screen-review.vuri --root screenshots=/data/shots
```

```python
from urivision import run_file
res = run_file("examples/screen-review.vuri")                # DecisionCard → artifact://reports/...
```

**Kontrakt wyniku — DecisionCard v1:** `decision` (ok|fix|block|unknown) · `confidence` ·
`summary` · `findings[]` (aspect, severity, `region.anchor` — kotwica opisowa, nie piksele,
evidence, impact, recommendation) · `next_actions[]`. Wymuszany przez
`response_format=json_schema` (structured output).

**Potok:**

```
.vuri → dsl.parse → AST(Process) → validators.validate (blokuje złe procesy TANIO)
      → compiler.compile_prompt (wymusza decyzję+dowody, nie opis)
      → resolver (llm://gemini/x → 'gemini/x' LiteLLM; artifact:// → ścieżka)
      → runner_litellm (multimodal text+image, json_schema) → DecisionCard → artifact://reports
```

Rdzeń (parser/walidacja/kompilacja) nie ma zależności i jest w pełni testowalny bez modelu
(`make test`, `--dry-run`). Model dokłada się jako `[litellm]`.

## Nowość w 0.3 — Native Test Lab

Ta warstwa dodaje to, czego brakowało po Dockerze: **macierz natywnych runnerów OS** i narzędzia do oceny, czy można realnie deklarować wsparcie dla popularnych systemów z ostatnich lat. Docker nadal służy do kontraktu i Linuksa, ale Windows UIA, macOS AX, Wayland, Android, iOS, RDP/Citrix i HID/KVM wymagają realnych hostów lub urządzeń.

Nowe komendy:

```bash
urivision native-matrix --format markdown
urivision native-probe --format json
urivision route type_text --profile windows-11-uia
urivision route-matrix

make native-matrix
make native-probe
make confidence
```

Nowe dokumenty:

```txt
docs/NATIVE_TEST_LAB.md
docs/OS_COVERAGE_MATRIX.md
docs/METHOD_ROUTER_DESIGN.md
docs/ADAPTER_CONTRACT.md
docs/EVENT_TRACE_SCHEMA.md
docs/BENCHMARK_PLAN.md
docs/SECURITY_POLICY.md
```

Nowe profile natywne obejmują Windows 10/11/Server, macOS 14/15/26, Ubuntu X11/Wayland, Fedora GNOME Wayland, KDE Wayland, Debian/RHEL/Rocky, ChromeOS, Android, iOS, VNC/noVNC, RDP/Citrix/Horizon oraz HID/KVM/RP2040.

## Po co ta zmiana

Dotychczasowy `urivision` dobrze rozwiązuje warstwę percepcji: `.vuri` opisuje obraz, model, aspekty, pytanie decyzyjne i schemat wyniku, a runtime kompiluje to do DecisionCard. To zostaje bez zmian.

Problem kontroli systemów operacyjnych jest jednak szerszy: funkcje typu `screenshot`, `OCR`, `find element`, `focus`, `type`, `click`, `browser fill`, `KVM batch`, `verify_texts` nie powinny być znane agentowi jako importy Pythona. Powinny być znane jako **adresowalne zdolności**:

```txt
ui://local/tree/query/snapshot
ui://local/element/query/find
ui://local/element/command/focus
input://local/keyboard/command/type
browser://chrome/element/command/fill
kvm://local/input/command/task_run
guard://local/batch/command/run
vision://local/screen/command/parse
runtime://local/capabilities/query/list
```

Dzięki temu LLM dostaje katalog funkcji z opisami, schematami argumentów, efektami ubocznymi i przykładami. Orkiestruje przez URI, a implementacja pod spodem może być inna dla Windows, macOS, Linux X11, Wayland, noVNC, RDP, HID albo przeglądarki.

## Instalacja lokalna

```bash
pip install -e .
```

Opcjonalnie dla ścieżki vision/LiteLLM:

```bash
pip install -e '.[litellm]'
```

## Szybki test

```bash
urivision catalog --format markdown
urivision explain input://local/keyboard/command/type
urivision call input://local/keyboard/command/type --json '{"text":"hello"}'
urivision plan examples/desktop-control.plan.json
```

## Katalog dla LLM

```bash
urivision catalog --format prompt
```

Zwraca instrukcję i pełny katalog capability. To jest blok, który można wstrzyknąć do promptu orkiestratora.

Przykład fragmentu:

```txt
- input://{target}/keyboard/command/type
    kind: command; title: Type text through keyboard backend
    when: Wysyła tekst przez backend klawiatury. Używać po focus/locator i zawsze z postcondition verify.
    args: text:string*
    side_effects: sends keyboard input; may type into wrong focused element if focus is stale
    safety: needs-verification
```

## Jedno wywołanie przez URI

```bash
urivision call ui://local/element/query/find --json '{"role":"button","name":"Save"}'
```

Wynik:

```json
{
  "ok": true,
  "found": true,
  "element": {
    "id": "button:save",
    "role": "button",
    "name": "Save"
  }
}
```

## Plan orkiestracji

Plany są zwykłym JSON. Każdy krok ma `call` jako URI i `with` jako payload.

```json
{
  "schema": "schema://runtime/uri-plan.v1",
  "goal": "Znajdź pole Search, ustaw fokus, wpisz tekst i potwierdź, że tekst jest widoczny.",
  "steps": [
    {
      "id": "find_search",
      "call": "ui://local/element/query/find",
      "with": {"role": "textbox", "name": "Search"},
      "expect_result": {"ok": true, "found": true}
    },
    {
      "id": "focus_search",
      "call": "ui://local/element/command/focus",
      "with": {"element_id": "${find_search.element.id}"}
    },
    {
      "id": "type_text",
      "call": "input://local/keyboard/command/type",
      "with": {"text": "URI runtime works"}
    },
    {
      "id": "verify_text",
      "call": "view://local/screen/query/text",
      "with": {"contains": "URI runtime works"},
      "expect_result": {"ok": true, "found": true}
    }
  ]
}
```

Uruchomienie:

```bash
urivision plan examples/desktop-control.plan.json
```

## Guarded batch

Dla niestabilnego inputu, np. KVM/VNC/HID, nie należy akceptować samego faktu wysłania klawiszy. Trzeba sprawdzić skutek.

```json
{
  "call": "guard://local/batch/command/run",
  "with": {
    "steps": [{"op": "type", "text": "guarded input"}],
    "expect": {
      "uri": "view://local/screen/query/text",
      "with": {"contains": "guarded input"}
    },
    "tries": 2
  }
}
```

To formalizuje wzorzec:

```txt
act → verify postcondition → retry/fail
```

## Reużycie istniejących funkcji przez URI

Migracja istniejącej funkcji:

```python
from urivision import CapabilityRegistry, register_uri_function, uri_function

@uri_function(
    "math://local/add/command/run",
    title="Add two integers",
    description="Przykład migracji zwykłej funkcji Python do wywołania przez URI.",
    kind="command",
)
def add(a: int, b: int) -> dict:
    return {"ok": True, "value": a + b}

registry = CapabilityRegistry()
register_uri_function(registry, add)
print(registry.call("math://local/add/command/run", {"a": 2, "b": 3}))
```

W refaktoryzacji oznacza to: najpierw opakowujesz istniejące funkcje kontraktem URI, dopiero później porządkujesz implementację.

## Warstwy architektury

```txt
LLM / user intent
  ↓
runtime://local/capabilities/query/list       # LLM poznaje funkcje
  ↓
URI plan: ui://..., input://..., browser://... # LLM orkiestruje przez adresy
  ↓
CapabilityRegistry                            # dopasowanie URI do handlera
  ↓
Adapter OS/browser/KVM/HID/vision             # konkretne wykonanie
  ↓
Trace + postconditions                         # verify-before-act
```

## Zasada wyboru backendu

1. `browser://` / CDP / Playwright — gdy to przeglądarka albo Electron.
2. `ui://` / accessibility tree — gdy aplikacja wystawia semantykę UI.
3. `vision://` — gdy trzeba zsyntetyzować elementy ze screena.
4. `input://` — klawiatura/mysz jako fallback.
5. `kvm://` / `hid://` — gdy system jest zewnętrzny, zablokowany albo przed logowaniem.
6. `guard://` — każde kruche wejście z postcondition.

## Co jest mockiem, a co kontraktem

Domyślne handlery runtime są mockami bez zależności systemowych. To celowe. Stabilny ma być **kontrakt URI**, nie bieżący backend.

Do podmiany w realnym wdrożeniu:

| URI | Realny adapter |
| --- | --- |
| `ui://...` | Windows UIA, macOS AX, Linux AT-SPI, AccessKit/xa11y |
| `browser://...` | Playwright, CDP, extension/plugin |
| `view://...` | screenshot API, VNC/RDP capture, OCR worker, EasyOCR |
| `vision://...` | OmniParser, ScreenParser, lokalny VLM, LiteLLM vision |
| `input://...` | SendInput, CGEvent, xdotool, ydotool, libei |
| `kvm://...` | noVNC/RFB, RDP, KVM connector |
| `hid://...` | RP2040/USB HID, IP-KVM |

## Struktura plików runtime

```txt
src/urivision/uri.py              # parser i matcher URI
src/urivision/capability.py       # kontrakt capability + RuntimeContext
src/urivision/registry.py         # rejestr, dispatch, walidacja payloadów, katalog LLM
src/urivision/runtime.py          # domyślne capabilities i mock runtime
src/urivision/orchestrator.py     # JSON plan runner
src/urivision/bindings.py         # @uri_function dla migracji istniejących funkcji
src/urivision/llm_catalog.py      # prompt/tools dla LLM
src/urivision/method_router.py    # wybór backendu wg profilu OS
src/urivision/native_profiles.py  # profile natywne (Windows/macOS/Linux/Android/…)
examples/*.plan.json              # przykładowe procesy URI
examples/function_binding_example.py
```

## Dlaczego to będzie szybsze i stabilniejsze

Obecny problem nie wynika wyłącznie z OCR. Problemem jest to, że agent za każdym razem musi od nowa domyślać się: co jest funkcją, jaki ma payload, czy kliknięcie jest bezpieczne, czy po typowaniu trzeba zweryfikować wynik. Katalog URI przenosi tę wiedzę do jawnych kontraktów.

To nie usuwa kosztu screenshot/OCR, ale zmniejsza liczbę ślepych prób i pozwala routerowi wybierać lepszą ścieżkę: DOM/accessibility przed myszą, batch z postcondition zamiast serii niezweryfikowanych kliknięć.

## Docker / backend matrix

Warstwa Docker znajduje się w `docker/` i służy do testowania URI Runtime na czterech profilach backendów:

- `linux-x11-novnc` — Linux X11/noVNC harness, przygotowany pod Xvfb/x11vnc/VNC.
- `linux-wayland-headless` — Linux Wayland/headless harness, przygotowany pod AT-SPI/portal/libei.
- `windows-uia-contract` — kontrakt Windows UI Automation; realne UIA wymaga hosta Windows.
- `macos-ax-contract` — kontrakt macOS AXUIElement; realne AX wymaga hosta macOS i uprawnień TCC.

Lokalnie bez Dockera:

```bash
make matrix
```

W Dockerze:

```bash
make docker-matrix
make docker-linux-x11
make docker-wayland
make docker-contract
```

Raporty zapisują się do `artifacts/*.json` oraz `artifacts/backend-matrix.md`.

## Roadmap

- lokalny etap `artifact://image/crop/...` (Pillow/OpenCV) przed drugim wywołaniem na wycinku
  (mały tekst, kadr) — jako **jawny proces URI**, nie ukryta akcja modelu;
- `event://` trace store; więcej `aspect://` (car/part, document/missing-data, diagram/wiring-risk);
- realne adaptery za kontraktami `ui://`/`input://`/`view://` (UIA/AX/AT-SPI, SendInput/ydotool,
  screenshot+OCR) wg `docs/ADAPTER_CONTRACT.md`;
- integracja z pętlą kontroli verify-before-act (`vguard`): tania kotwica → gdy niejednoznaczne,
  VURI-DecisionCard jako warstwa 3.
