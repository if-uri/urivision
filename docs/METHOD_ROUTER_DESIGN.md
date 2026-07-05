# MethodRouter Design

## Problem

The same user intent can be executed many ways. For example `type_text` can mean:

- DOM fill through CDP.
- Accessibility `set_value` through UIA/AX/AT-SPI.
- Focus + keyboard events.
- VNC/RDP keyboard injection.
- Physical HID keyboard.

The LLM should not choose between those directly. The runtime should.

## Route order

For semantic UI tasks:

```text
browser DOM/CDP
  -> native accessibility tree/action
  -> keyboard/focus fallback
  -> pointer coordinate fallback
  -> remote session fallback
  -> hardware HID fallback
```

For verification:

```text
DOM/accessibility state
  -> screen text/OCR
  -> vision parser
  -> human/unknown
```

## Implemented file

`src/urivision/method_router.py`

Example:

```bash
PYTHONPATH=src python -m urivision.cli route type_text --profile windows-11-uia
PYTHONPATH=src python -m urivision.cli route press_element --profile hid-kvm-rp2040
```

## Router output

The route decision includes:

- selected adapter;
- selected URI;
- fallback candidates;
- quality class;
- verification URI.

This makes the runtime explainable to LLM and debuggable by humans.
