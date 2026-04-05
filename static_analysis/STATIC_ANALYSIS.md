# Static Analysis Report — Test-Users-Backend

Tools used: **Bandit** (security) and **Radon** (complexity).

Run the analysis with:
```powershell
# Windows
.\static_analysis\run_static_analysis.ps1

# Mac/Linux
bash static_analysis/run_static_analysis.sh
```

---

## Bandit — Security Analysis

### HIGH severity

| File | Line | Finding |
|------|------|---------|
| `app.py` | 123 | Flask running with `debug=True`. Exposes the Werkzeug interactive debugger which allows arbitrary code execution on the server. **CWE-94**. |

### MEDIUM severity

| File | Line | Finding |
|------|------|---------|
| `app.py` | 123 | `host='0.0.0.0'` binds to all network interfaces, making the app reachable from any machine on the same network. **CWE-605**. |
| `src/town.py` | 40 | SQL injection risk. The `LIMIT` clause is built using an f-string directly injecting the variable `random_town` into raw SQL instead of using a parameterised query. The value is internally generated so not immediately exploitable, but the pattern is unsafe. **CWE-89**. |

### LOW severity

| File | Finding |
|------|---------|
| `src/fake_info.py`, `src/town.py` | Use of `random.randint()` and `random.choice()` (21 instances). Bandit flags these because `random` is not cryptographically secure. For fake data generation this is acceptable — `random` is not being used for passwords or tokens — but noted for completeness. |
| `src/info.py` | Line 12 — empty hardcoded password string `PASSWORD = ''`. |

---

## Radon — Cyclomatic Complexity Analysis

| Function | File | Grade | Complexity | Notes |
|----------|------|-------|------------|-------|
| `api_handler` | `app.py` | C | 18 | Routes all 9 API endpoints in a single function with many conditional branches. Should ideally be split into separate route handlers. |
| `FakeInfo._set_address` | `src/fake_info.py` | B | 8 | Many branches for floor, door, and house number format generation. |
| `FakeInfo._set_cpr` | `src/fake_info.py` | B | 7 | CPR generation with gender parity logic. This is the function where the gender/CPR parity bug was found. |
| All other functions | — | A | 1–5 | Clean and straightforward. |

**Average complexity: A (2.53)** — overall the codebase is clean and maintainable.

---

## Key Insight

The two functions Radon flagged as most complex — `_set_cpr` (complexity 7) and `_set_address` (complexity 8) — are exactly the two functions where real bugs were found by E2E testing. Higher complexity correlates with higher bug risk.

This validates using static complexity analysis as a signal for where to focus testing effort.
