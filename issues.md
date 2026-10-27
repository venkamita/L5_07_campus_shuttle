# Issues Found & Fixed — shuttle_system.py

| # | Issue | Type | Tool / Code | Line(s) (original) | Description | Fix Approach |
|---|-------|------|-------------|--------------------|-------------|--------------|
| 1 | Bare `except: pass` | Bug / Security | Bandit B110, Pylint W0702, Flake8 E722 | 26–30 | Swallows every error, so the `TypeError` from the `"full"` trip on R3 was silently hidden. | Removed the try/except; skip routes with no trips explicitly, and validate input at entry. |
| 2 | Mutable default argument | Bug | Pylint W0102 | 11 | `logs=[]` is created once and shared across every call, so logs leak between calls. | Default to `None` and create a new list inside the function. |
| 3 | Invalid passenger counts accepted | Logic bug (no tool flagged it) | — (found by running) | 49–50 | `-6` and `"full"` were stored; R2 average became `-1.0`, R3 crashed `sum()`. | `add_trip_log` rejects non-int / negative counts with `ValueError`; `main` reports and skips them. |
| 4 | Crash on removed / unknown route | Logic bug (no tool flagged it) | — (found by running) | 17, 21, 57–58 | Program died with `KeyError: 'R3'` after `remove_route("R3")`; any typo at the prompt also crashed; empty route → `ZeroDivisionError`. | `average_load` returns `None` for missing/empty routes; lookup checks membership; `remove_route` uses `pop(..., None)`. |
| 5 | Insecure PRNG | Security (Low) | Bandit B311 | 35 | `random.choice` flagged as non-cryptographic. | Switched to `secrets.choice`. |
| 6 | `open()` without `with` / encoding | Resource leak | Pylint R1732, W1514 | 39, 42 | File handles left open on error (second one never closed); platform-dependent encoding. | `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| 7 | `global` rebinding | Design | Pylint W0603 | 38 | `sync_fleet_data` reassigned the module global. | Renamed to constant `ROUTES` and update it in place (`clear()` + `update()`). |
| 8 | Bad name & unused argument | Style | Pylint C0103, W0613 | 33 | `assignDriver` not snake_case; `route_id` unused. | Renamed to `assign_driver()`, dropped the unused parameter, moved drivers to `DRIVERS`. |
| 9 | Missing docstrings, %-formatting | Style | Pylint C0114, C0116, C0209 | 1, 11–45 | No module/function docstrings; old-style `%` formatting. | Added docstrings; used f-strings. |
| 10 | PEP 8 formatting | Style | Flake8 E302, E305, E501 | 11–60 | One blank line between functions, 82-char line, no blank lines before module code. | Two blank lines between top-level defs, wrapped long line, added `if __name__ == "__main__":` guard. |

**Results:** Pylint 6.25 → **10.00/10** · Bandit 2 Low → **0** · Flake8 10 → **0**
