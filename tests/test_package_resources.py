"""Package-resource smoke coverage."""

from __future__ import annotations

import hashlib
from importlib.resources import files

from change_audit.review.core.prompt import (
    PRODUCT_REVIEWER_PROMPT_VERSION,
    get_default_reviewer_template,
)
from change_audit.validation import load_audit_schema


def test_runtime_resources_are_readable_via_importlib() -> None:
    schema = load_audit_schema()
    template = files("change_audit.renderers").joinpath(
        "templates/audit.html.j2"
    ).read_text(encoding="utf-8")
    css = files("change_audit.renderers").joinpath("static/audit.css").read_text(
        encoding="utf-8"
    )
    javascript = files("change_audit.renderers").joinpath(
        "static/audit.js"
    ).read_text(encoding="utf-8")
    prompt = get_default_reviewer_template()

    assert schema["$schema"].endswith("2020-12/schema")
    assert "<!doctype html>" in template
    assert "prefers-reduced-motion" in css
    assert "changeAuditReady" in javascript
    assert PRODUCT_REVIEWER_PROMPT_VERSION == "v0.3"
    assert prompt.startswith("# change-audit Reviewer Prompt Template (product/v0.3)\n")
    assert hashlib.sha256(prompt.encode("utf-8")).hexdigest() == (
        "ea9f6d367e4d6791f188a1669753c2c77fcbc6eb8ae594400216b742c40663a7"
    )
    # Only the identity/version heading changed from product/v0.2.
    protocol_body = prompt.partition("\n")[2]
    assert hashlib.sha256(protocol_body.encode("utf-8")).hexdigest() == (
        "d20d5af60cf26c99b4f34a96de61f6013785928c7d435ee8e849dbc220c8ebc6"
    )
    assert "Simplified Chinese" in prompt
