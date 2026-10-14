# Lab 5: Reflection — Static Code Analysis

## 1. What is static code analysis, and how is it useful?

Static code analysis examines source code without executing it. It helps find likely bugs, unsafe coding patterns, maintainability problems, and style violations early. Fixing these issues before deployment makes code easier to understand and reduces avoidable defects.

## 2. What did Pylint, Bandit, and Flake8 each help identify?

Pylint identified quality issues such as missing docstrings, non-standard naming, and a mutable default argument. Bandit identified security concerns, including shell execution built from a string, unsafe temporary-file creation, a hard-coded password-like value, and use of the `random` module for a random choice. Flake8 identified formatting violations such as whitespace and blank-line errors. Together, the tools cover different but complementary aspects of code quality.

## 3. Which issues were most important, and how were they fixed?

The highest-priority issue was the shell command constructed with `os.system()` because untrusted input could alter the command. It was replaced with `subprocess.run()` using a list of arguments and `shell=False`, with validation and error checking. The unsafe `tempfile.mktemp()` call was replaced by `NamedTemporaryFile`. The mutable default list was changed to `None`, and a fresh list is created for each team. The unused password-like constant was removed, and `secrets.choice()` replaced `random.choice()`. Other improvements included `snake_case` names, docstrings, input validation, consistent formatting, and a main guard so importing the module does not run the demonstration.

## 4. How does static analysis improve code quality, and what are its limitations?

Static analysis encourages consistent style, catches common mistakes, and highlights risky code patterns before runtime. It also gives developers repeatable feedback after changes. However, tools can produce false positives and cannot guarantee that a program is correct or secure. They may miss logical errors that depend on runtime data or requirements. Therefore, static analysis should be combined with tests, manual review, and running the program with valid and invalid inputs.

## Verification note

Run Pylint, Bandit, and Flake8 locally after applying the changes. Record the actual Pylint score and any remaining findings from your generated reports. Do not claim that every tool is clean until the reports confirm it.
