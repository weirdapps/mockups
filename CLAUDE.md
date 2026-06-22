# mockups

Pixel-perfect iPhone mockup generator. Places screenshots inside Apple device frames using a flood-fill masking algorithm to respect curved screen corners.

## Tech Stack

- Python 3.9+ with Hatchling build backend
- Pillow (image processing), NumPy (flood-fill masking)
- Ruff (lint/format), mypy (type-checking), pytest (tests)
- SonarCloud for code quality; CI via GitHub Actions

## Install

```bash
# For use
pipx install git+https://github.com/weirdapps/mockups.git

# For development
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Run

```bash
mockup screenshot.png                         # default frame: iPhone 16 Pro Max Black Titanium
mockup screenshot.png out.png --frame 16_pro_black
mockup --list-frames
```

## Test

```bash
pytest
```

CI runs lint (`ruff check`, `ruff format --check`, `mypy`) then `pytest` on every push/PR.

## Code Organization

```text
src/mockups/
  __init__.py   — public API: create_mockup(), FRAMES, DEFAULT_FRAME
  core.py       — flood-fill masking, frame registry, image composition
  cli.py        — argparse CLI entry point
tests/
  test_mockup.py
```

## Key Conventions

- All public surface lives in `src/mockups/__init__.py`; import from there, not from submodules.
- Frame PNGs ship inside the package (no runtime download). Add new frames by extending `FRAMES` dict in `core.py` and placing the PNG alongside.
- Flood-fill starts from screen center — don't change the seed point without verifying all frame variants.
- Type annotations required on all public functions; mypy runs in CI.
- Output is always PNG with transparent background regardless of input format.
