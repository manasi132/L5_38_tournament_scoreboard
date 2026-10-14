# Static Code Analysis Issue Log

**File:** `tournament_scoreboard.py`  
**Tools:** Pylint, Bandit, Flake8

The line numbers below refer to the original starter file and its initial reports. Grouped naming/docstring entries represent repeated warnings for multiple functions or parameters. The reports produced on your computer are the authority for exact line numbers and tool-version-specific findings.

| Issue / finding | Tool and severity | Original line(s) | Why it is a problem | Fix applied |
|---|---|---:|---|---|
| Shell command built with string concatenation | Bandit B605 — High | 69–71 | `os.system()` invokes a shell with a value derived from `server`, creating a command-injection risk. | Use `subprocess.run()` with an argument list, `shell=False`, `check=True`, and server-input validation. |
| Unsafe temporary-file name | Bandit B306 — Medium | 64–66 | `tempfile.mktemp()` returns a path without safely creating the file, allowing a race condition. | Use `NamedTemporaryFile(delete=False)` to create the file safely. |
| Mutable default list | Pylint W0102 | 11 | `players=[]` reuses the same list object across calls that omit the argument. | Default to `None` and make a new list per team. |
| Hard-coded password-like constant | Bandit B105 — Low | 6 | The constant `REFEREE_PASSWORD` is unused and resembles a credential embedded in source code. | Remove the unused constant; do not store real credentials in source. |
| Pseudo-random choice flagged for security use | Bandit B311 — Low | 60–61 | The `random` module is not designed for security-sensitive randomness. | Use `secrets.choice()` for the coin toss, removing the Bandit warning. |
| CamelCase function names | Pylint C0103 | 11, 16, 25, 47, 51, 56, 60, 64, 69 | Function names do not follow Python's `snake_case` convention. | Rename functions to `add_team`, `match_result`, `record_match`, `goal_difference`, `league_table`, `is_top_two`, `toss_coin`, `table_file_path`, and `publish_table`. |
| CamelCase parameter names | Pylint C0103 | 11, 16, 25, 42, 47, 56 | Names such as `teamName`, `homeGoals`, and `awayGoals` are inconsistent with Python style. | Rename parameters to `team_name`, `home_goals`, and `away_goals`. |
| Missing module docstring | Pylint C0114 | 1 | The module purpose is not documented. | Add a module docstring. |
| Missing function docstrings | Pylint C0116 | Multiple functions | Function behavior and expectations are unclear to readers. | Add docstrings to public and helper functions. |
| Unnecessary `elif` after `return` | Pylint R1705 | 17 | The `elif` is redundant because the preceding branch already returns. | Use a separate `if` and a final `return`. |
| Repeated comparisons for top-two check | Pylint R1714 | 58 | Comparing separately against two positions is less concise. | Use membership in `league_table()[:2]`. |
| Whitespace before dictionary colon | Flake8 E203 | 5 | Inconsistent whitespace violates PEP 8 formatting. | Format as `"win": 3`. |
| Incorrect blank lines before function | Flake8 E302 | 60 | Top-level function definitions require two blank lines. | Apply consistent top-level spacing. |
| Missing whitespace after comma | Flake8 E231 | 79 | A comma is not followed by a space. | Apply standard spacing and f-string formatting. |
| Insufficient spacing before inline comment | Flake8 E261 | 87 | Inline comment spacing violates the style guide. | Remove the unnecessary inline comment and format the statement. |
| No validation of match inputs | Correctness issue found by code review | 12–37 | Negative/non-integer goals, unknown teams, duplicate team names, or self-matches could cause invalid data or confusing failures. | Validate team names, duplicate registrations, goals, and both teams before updating statistics. |
| Demo executes when imported | Maintainability issue found by code review | Final line | Importing the module immediately prints output and mutates global state. | Put the demo call inside `if __name__ == "__main__":`. |
| Unformatted print output | Readability issue found by code review | 67–75 | Comma-separated print arguments make formatting less consistent. | Use f-strings and readable multiline output. |

## Verification

After replacing the starter code, run:

```powershell
python -m pylint tournament_scoreboard.py > pylint_report.txt
python -m bandit -r tournament_scoreboard.py > bandit_report.txt
python -m flake8 tournament_scoreboard.py > flake8_report.txt
```

Then inspect the reports. A clean Flake8 run produces no findings. Bandit should report no issues in this file. Pylint's score and remaining messages depend on the installed version; do not claim a perfect score unless your report confirms it. Also run the program and test invalid inputs before submission.
