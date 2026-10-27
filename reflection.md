# Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
Easiest were the style findings: Flake8 blank-line/line-length warnings and Pylint docstring/naming messages are mechanical and have one obvious fix. Hardest were the logic bugs no tool reported — the negative and `"full"` passenger counts and the `KeyError` after `remove_route("R3")`. They needed running the program, reading the output, and deciding what correct behaviour should be (reject bad input, report missing routes) rather than just silencing a warning. The bare `except` was also tricky: removing it exposed the hidden `TypeError`, so it had to be fixed together with input validation.

**2. Did the static analysis tools report any false positives? If so, describe one example.**
Bandit B311 (`random.choice`) is effectively a false positive here: picking a shuttle driver is not a security decision, so a standard PRNG is fine. I switched to `secrets.choice` because it costs nothing, but `# nosec B311` with a justification would also have been reasonable. Pylint's missing-docstring warnings on tiny functions are arguably noise too.

**3. How would you integrate static analysis tools into your actual software development workflow?**
Run Flake8 and Pylint in a pre-commit hook so problems are caught before they reach the repo, and run all three (plus Bandit) in CI on every pull request, failing the build on Bandit medium/high findings or a Pylint score below a threshold. Keep a shared `.pylintrc`/`setup.cfg` so the whole team uses the same rules, and use editor integration for instant feedback.

**4. What tangible improvements did you observe in the code quality, readability, and potential robustness after applying the fixes?**
Pylint went from 6.25 to 10.00, Bandit and Flake8 from 2 and 10 findings to zero. More importantly the program no longer crashes: invalid trips are rejected with a clear message, averages are correct (R2 is 4.0 instead of -1.0), unknown routes are handled, files are closed reliably, and the module can be imported without running `main()`. Docstrings and consistent naming make it easier to read and maintain.
