# mockups

Pixel-perfect iPhone mockup generator. Places screenshots inside Apple device frames using a flood-fill masking algorithm to respect curved screen corners.

## Tech Stack

- Python 3.9+ with Hatchling build backend
- Pillow (image processing), NumPy (flood-fill masking)
- Ruff (lint/format), pytest (tests); mypy runs via pre-commit only, not CI
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

CI runs `ruff check` and `ruff format --check`, then `pytest`, on every push/PR to `master` (see `.github/workflows/ci.yml`). Python 3.12 is used in CI. mypy, gitleaks, yamllint, and markdownlint run only via `pre-commit` locally.

Ruff is pinned to an exact version in CI and in `.pre-commit-config.yaml`; bump both together or local and CI results diverge. `ruff format` also formats Python code blocks inside Markdown, so `README.md` snippets are checked by `ruff format --check .`.

## Code Organization

```text
src/mockups/
  __init__.py   public API: create_mockup(), FRAMES, DEFAULT_FRAME
  core.py       flood-fill masking, frame registry, image composition
  cli.py        argparse CLI entry point (mockup)
  frames/       six bundled iPhone 16 Pro / Pro Max PNGs
tests/
  test_mockup.py
```

Bundled frame keys (see `FRAMES` in `core.py`): `16_pro_max_black` (default), `16_pro_max_natural`, `16_pro_max_white`, `16_pro_max_desert`, `16_pro_black`, `16_pro_natural`.

## Key Conventions

- All public surface lives in `src/mockups/__init__.py`; import from there, not from submodules.
- Frame PNGs ship inside the package (no runtime download). Add new frames by extending `FRAMES` dict in `core.py` and placing the PNG alongside in `src/mockups/frames/`.
- Flood-fill starts from screen center (`fw // 2, fh // 2`); do not change the seed point without verifying all frame variants.
- Type annotations are encouraged on public functions; mypy checks them via the pre-commit hook (not CI).
- Output is always PNG with a transparent RGBA background regardless of input format.
- Every `github/codeql-action/*` step in `.github/workflows/codeql.yml` must be pinned to the SAME version. A split across `init` and `analyze` fails the run with "Loaded a configuration file for version X, but running version Y". Dependabot groups them under `codeql-action` in `.github/dependabot.yml` so they always bump in one PR; never merge a partial bump.
