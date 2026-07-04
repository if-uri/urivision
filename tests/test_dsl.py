# Author: Tom Sapletta · Part of the ifURI solution.
"""Walidacja lokalna VURI — parser + kontrola procesu, bez uderzania w model."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from urivision import parse, validate, run_source          # noqa: E402
from urivision.validators import VuriValidationError        # noqa: E402
from urivision.dsl import VuriSyntaxError                   # noqa: E402

GOOD = (Path(__file__).resolve().parents[1] / "examples" / "screen-review.vuri").read_text()


def test_parse_reads_all_parts():
    p = validate(parse(GOOD))
    assert p.model.provider == "gemini"
    assert p.model.model == "gemini-3.5-flash"
    assert p.model.options.get("reasoning") == "low"
    assert len(p.aspects) == 4
    assert p.output_schema == "schema://vision/decision-card.v1"
    assert p.question.startswith("Czy ekran")


def test_missing_emit_rejected():
    src = "\n".join(l for l in GOOD.splitlines() if not l.startswith("emit"))
    with pytest.raises(VuriValidationError, match="output_"):
        validate(parse(src))


def test_bad_scheme_rejected():
    src = GOOD.replace("read artifact://", "read http://")
    with pytest.raises(VuriValidationError, match="scheme"):
        validate(parse(src))


def test_non_image_rejected():
    src = GOOD.replace("as image/png", "as application/pdf")
    with pytest.raises(VuriValidationError, match="image"):
        validate(parse(src))


def test_unknown_statement_rejected():
    with pytest.raises(VuriSyntaxError):
        parse(GOOD + "\nfoobar something")


def test_dry_run_compiles_call_without_model():
    r = run_source(GOOD, dry_run=True)
    assert r["ok"] and r["dryRun"]
    assert r["call"]["model"] == "gemini/gemini-3.5-flash"     # forma LiteLLM
    assert "DECYZJĘ" in r["call"]["prompt"]                    # prompt wymusza decyzję, nie opis
    assert r["call"]["reasoning"] == "low"
