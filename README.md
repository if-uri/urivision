# VURI — Visual URI Process Language (`urivision`)

Lekki, szybki model **analizy i kontroli obrazu**. Zamiast długiego promptu wskazujesz
**obraz + model + aspekty + pytanie decyzyjne + schemat wyniku** — a proces kompiluje się do
wywołania modelu vision i zwraca **DecisionCard: decyzję z dowodami, nie opis**.

Powstało z lekcji [[verify-before-act]]: percepcja ma być tanim, powtarzalnym procesem URI
(warstwa 3: „wizja LLM"), a nie ręcznym oglądaniem zrzutów.

## Proces `.vuri`

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

## Użycie

```bash
pip install -e '.[litellm]'
urivision run examples/screen-review.vuri --dry-run          # kompiluje wywołanie (bez modelu)
urivision run examples/screen-review.vuri --root screenshots=/data/shots
```

```python
from urivision import run_file
res = run_file("examples/screen-review.vuri")                # DecisionCard → artifact://reports/...
```

## Kontrakt wyniku — DecisionCard v1

`decision` (ok|fix|block|unknown) · `confidence` · `summary` · `findings[]` (aspect, severity,
`region.anchor` — kotwica opisowa, nie piksele, evidence, impact, recommendation) · `next_actions[]`.
Wymuszany przez `response_format=json_schema` (structured output).

## Architektura

```
.vuri → dsl.parse → AST(Process) → validators.validate (blokuje złe procesy TANIO)
      → compiler.compile_prompt (wymusza decyzję+dowody, nie opis)
      → resolver (llm://gemini/x → 'gemini/x' LiteLLM; artifact:// → ścieżka)
      → runner_litellm (multimodal text+image, json_schema) → DecisionCard → artifact://reports
```

Rdzeń (parser/walidacja/kompilacja) nie ma zależności i jest w pełni testowalny bez modelu
(`pytest`, `--dry-run`). Model dokłada się jako `[litellm]`.

## Roadmap

- lokalny etap `artifact://image/crop/...` (Pillow/OpenCV) przed drugim wywołaniem na wycinku
  (mały tekst, kadr) — jako **jawny proces URI**, nie ukryta akcja modelu;
- `event://` trace store; więcej `aspect://` (car/part, document/missing-data, diagram/wiring-risk);
- pak obok `uricore`/`uri_router` — połączenie z pętlą kontroli [[verify-before-act]]
  (`vguard`): tania kotwica → gdy niejednoznaczne, VURI-DecisionCard jako warstwa 3.
