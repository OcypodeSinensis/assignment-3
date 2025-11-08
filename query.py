import sqlite3

with sqlite3.connect('concrete.db') as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. SHOW ALL TESTS
    print("ALL TESTS")
    for r in cursor.execute("""
        SELECT project_name, test_date, required_strength, actual_strength, passed
        FROM concrete_tests
        ORDER BY test_id
    """):
        status = "PASS" if r["passed"] == 1 else "FAIL"
        print(f"{r['project_name']}: {r['actual_strength']} PSI - {status}")
    print()

    # 2. Show ONLY failed tests
    print("FAILED TESTS")
    for r in cursor.execute("""
        SELECT project_name, test_date, required_strength, actual_strength
        FROM concrete_tests
        WHERE passed = 0
        ORDER BY test_id
    """):
        print(f"{r['project_name']} on {r['test_date']}")
        print(f"  Required: {r['required_strength']} PSI")
        print(f"  Actual: {r['actual_strength']} PSI")
    print()

    # 3. Count tests by project
    print("TESTS PER PROJECT")
    totals = {row["project_name"]: row["cnt"] for row in cursor.execute("""
        SELECT project_name, COUNT(*) AS cnt
        FROM concrete_tests
        GROUP BY project_name
    """)}
    passed = {row["project_name"]: row["cnt"] for row in cursor.execute("""
        SELECT project_name, COUNT(*) AS cnt
        FROM concrete_tests
        WHERE passed = 1
        GROUP BY project_name
    """)}

    for project in sorted(totals.keys()):
        t = totals[project]
        p = passed.get(project, 0)
        print(f"{project}: {p}/{t} passed")
    print()