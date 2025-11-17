# Repository Guidelines

## Project Structure & Module Organization
The `hpfspecmatch/` package contains the fitting engine (`hpfspecmatch.py`), likelihood and prior math, plotting helpers, and the shared configuration module. Command-line entry points live at the repo root: use `run_hpfspecmatch.py` for single targets and `run_crossval.py` for survey sweeps. Spectral libraries sit in `lib/`, raw HPF extractions or staging data belong in `input/`, notebooks under `notebooks/` document worked examples, and MkDocs sources in `docs/` plus `custom_theme/` power the published documentation referenced by `mkdocs.yml`.

## Build, Test, and Development Commands
Install dependencies in editable mode via `python -m pip install -e .`. Use `python run_hpfspecmatch.py --config hpfspecmatch/config.py --target <OBJECT>` to fit a single star and write outputs next to the chosen library. Run validation sweeps with `python run_crossval.py --library lib/SPECMATCH_MASTER_with_ids.csv --nwalkers 256`. Preview the docs locally with `mkdocs serve` and publish-ready builds with `mkdocs build`.

## Coding Style & Naming Conventions
Follow PEP 8: four-space indentation, 88-character soft limit, and module-level logging via `logging.getLogger(__name__)`. Functions and modules use `snake_case`, classes (rare) use `PascalCase`, configuration constants remain uppercase, and new parameters should ship with docstrings plus type hints so notebooks and CLI scripts stay consistent.

## Testing Guidelines
There is no standalone `tests/` package yet, so authors should add targeted `pytest` files alongside the modules they touch (for example `tests/test_likelihood.py`). Favor deterministic fixtures by loading trimmed spectra from `input/` or synthetic arrays from `hpfspecmatch/utils.py`. When touching sampling logic, run `python run_crossval.py ...` and summarize metrics (log-likelihood deltas, recovered RVs) in the pull request.

## Commit & Pull Request Guidelines
Recent history shows short, imperative commit titles (e.g., “Enhance spectral matching functions with RV order support”). Mirror that style, mention the affected module when possible, and keep bodies focused on motivation plus data or notebook dependencies. Pull requests should describe scientific intent, list new CLI flags, attach validation plots or notebook cells, and link GitHub issues or observing programs. Ensure local install and docs build complete before requesting review.

## Configuration & Data Handling
Edit `hpfspecmatch/config.py` for default priors, MCMC settings, and path templates, but avoid hard-coding site-specific paths—prefer environment variables documented in README updates. Large FITS files and proprietary libraries belong outside the repo; reference their expected folder (usually `input/` or `lib/`) and add `.gitignore` entries if needed. Scrub headers for observer names or coordinates before sharing sample data.
