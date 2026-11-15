# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**CURP Suite** (`CURPSuite` on PyPI, import name `curp`) parses and validates
the Mexican CURP (Clave Única de Registro de Población). Pure Python, single
runtime dependency: `unidecode`. Licensed GPL v2.

Code, docstrings, error messages, docs and user-facing text are in **Spanish**;
keep new public API names and messages in Spanish to match
(e.g. `fecha_nacimiento`, `nombre_valido`, `CURPNameError`).

## Layout

- `curp/curp.py` — the `CURP` class (core). The constructor validates length,
  check digit, birth date, sex, region and name characters, then optionally
  validates `nombre` / `primer_apellido` / `segundo_apellido` or
  `nombre_completo`. Also the `Sexo` enum (ISO/IEC 5218).
- `curp/features.py` — `WordFeatures`: extracts first char / vowel / consonant
  from names, used for name matching.
- `curp/estados.py` — state codes → name + ISO 3166-2.
- `curp/altisonantes.py` — offensive-word substitutions per the official spec.
- `curp/chars.py` — character sets.
- `curp/exceptions.py` — exception hierarchy; all value errors subclass
  `CURPValueError`.
- `curp/cli.py` — `curp` console script (`curp <CURP> [-n|-p|-s|-c ...]`),
  prints JSON.
- `curp/__about__.py` — `__version__` (single source of truth; read by
  setuptools and checked against the git tag in CI).
- `tests/` — `unittest` suites with `hypothesis` property tests;
  `tests/strategies.py` and `tests/utils.py` generate valid CURPs and names.
- `docs/` — Sphinx docs (Read the Docs), incl. `CHANGELOG.rst` and the official
  spec `InstructivoCURP.pdf`.

## Environment setup

Dependencies are managed with Pipenv (`Pipfile` / `Pipfile.lock`); CI installs
them into the system interpreter rather than a virtualenv:

```bash
pip install pipenv
pipenv requirements --dev > /tmp/requirements.txt
pip install -r /tmp/requirements.txt
pip install -e .
```

## Commands

```bash
python -m unittest            # full test suite (what CI runs; ~20s, hypothesis)
python -m unittest tests.test_curp.TestCURP   # a single class (example)
flake8 curp tests             # lint (not enforced in CI)
mypy curp                     # type check (not enforced in CI)
python -m build               # build sdist/wheel
cd docs && make html          # build docs
```

`docs/dev/contributing.rst` mentions `tox`, but there is no tox config; use
`python -m unittest`.

## CI

`.github/workflows/integration.yml` runs `python -m unittest` on Python
3.10–3.14 across Ubuntu, macOS and Windows for pushes/PRs to `master`. On a tag,
it checks `v{__version__}` matches the tag and publishes to PyPI.

## Known state (as of this file's creation)

- Tests pass. `flake8` reports existing style warnings (mostly E501) and
  `mypy` reports implicit-`Optional` defaults in `CURP.__init__` plus missing
  `unidecode` stubs. Don't mass-reformat unrelated code in feature PRs.
- `pyproject.toml`/README claim Python 3.8+, while CI tests 3.10+.

## Conventions

- Branch names: `claude/{type}/short-description`, where type is `feat`, `fix`,
  `docs`, `refactor`, `test`, `chore`, `ci`, etc.
  (e.g. `claude/fix/verify-digit-overflow`).
- Default branch is `master`.
- Add or update tests for behaviour changes; prefer hypothesis strategies in
  `tests/strategies.py` for generated data.
- Note user-visible changes in `docs/CHANGELOG.rst`; update docs when the
  public API changes.
- When bumping the version, edit only `curp/__about__.py`.
