"""
Insert topic classifications for 2000 AMC 10A questions into the problems table.
Topics were derived by analyzing each problem's content against the existing taxonomy.
"""

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "amc_problems.db"
TABLE = "problems"

# (year, version, question_num, level_1, level_2, level_3)
# Questions with multiple topics get multiple rows (consistent with existing data pattern)
TOPICS = [
    # Q1: I*M*O = 2001, maximize I+M+O — prime factorization + factor optimization
    (2000, "A", 1,  "Number Theory",         "Primes and Composites",              "Prime Factorization"),
    (2000, "A", 1,  "Number Theory",         "Multiples and Divisors",             "Factors and Multiples"),

    # Q2: 2000 * 2000^2000 = 2000^2001 — exponent rules
    (2000, "A", 2,  "Algebra",               "Exponents and Radicals",             "Exponent Rules"),

    # Q3: Jenny eats 20% of jellybeans each day, 32 remain — percentages / working backwards
    (2000, "A", 3,  "Algebra",               "Basic Algebra",                      "Percentages"),

    # Q4: Fixed fee + hourly charge, two bills — system of equations / money problem
    (2000, "A", 4,  "Algebra",               "Algebraic Application",              "Money Problems"),
    (2000, "A", 4,  "Algebra",               "Basic Algebra",                      "System of Equations"),

    # Q5: Midpoints B, D; B moves parallel to AE — which of 4 quantities change?
    (2000, "A", 5,  "Geometry",              "Triangle Geometry",                  "Triangle Area"),
    (2000, "A", 5,  "Algebra",               "Logic",                              "Making Inferences"),

    # Q6: Which digit last appears in units position of Fibonacci numbers?
    (2000, "A", 6,  "Algebra",               "Sequences and Series",               "Fibonacci Sequences"),
    (2000, "A", 6,  "Number Theory",         "Modular Arithmetic and Congruences", "Last Digits"),

    # Q7: Rectangle, segments trisect a right angle — 30/60/90 triangles in a rectangle
    (2000, "A", 7,  "Geometry",              "Quadrilateral Geometry",             "Rectangles"),
    (2000, "A", 7,  "Geometry",              "Triangle Geometry",                  "30/60/90"),

    # Q8: 4/5 freshmen and 2/3 sophomores took AMC, equal contestants — ratio and proportion
    (2000, "A", 8,  "Algebra",               "Basic Algebra",                      "Ratio and Proportion"),

    # Q9: ab = sqrt(ab), a >= b — radical/exponent manipulation
    (2000, "A", 9,  "Algebra",               "Exponents and Radicals",             "Radicals"),

    # Q10: Two triangles with related side lengths — triangle inequality
    (2000, "A", 10, "Geometry",              "Triangle Geometry",                  "Triangle Inequality"),

    # Q11: Two primes between 4 and 18, product minus sum — primes + setting up equations
    (2000, "A", 11, "Number Theory",         "Primes and Composites",              "Primes"),
    (2000, "A", 11, "Algebra",               "Equations and Expressions",          "Setting up Equations"),

    # Q12: Figures with 1, 5, 13, 25... unit squares; figure 100 — quadratic pattern
    (2000, "A", 12, "Algebra",               "Sequences and Series",               "Patterns"),

    # Q13: 15 colored pegs on triangular board, no row/col repeats — constructive counting
    (2000, "A", 13, "Counting & Probability","Counting",                           "Constructive Counting"),

    # Q14: 5 scores entered randomly, running average always integer — divisibility + casework
    (2000, "A", 14, "Number Theory",         "Divisibility",                       "Divisibility"),
    (2000, "A", 14, "Counting & Probability","Counting",                           "Casework"),

    # Q15: ab = a - b, find possible value of a/b — algebraic manipulations
    (2000, "A", 15, "Algebra",               "Equations and Expressions",          "Algebraic Manipulations"),

    # Q16: Lattice points, segment meets segment at T — lattice points + distance formula
    (2000, "A", 16, "Geometry",              "Coordinate Geometry",                "Lattice Points"),
    (2000, "A", 16, "Geometry",              "Coordinate Geometry",                "Distance Formula"),

    # Q17: Coin machine invariant (penny→5 quarters etc.) — modular arithmetic invariant
    (2000, "A", 17, "Number Theory",         "Modular Arithmetic and Congruences", "Mods"),

    # Q18: Walk around 1km square, can see 1km in all directions — area with circular arcs
    (2000, "A", 18, "Geometry",              "Circle Geometry",                    "Circle Area"),

    # Q19: Hypotenuse split into square and two small right triangles — similar triangles
    (2000, "A", 19, "Geometry",              "Triangle Geometry",                  "Similar Triangles"),

    # Q20: Nonneg integers with constraint, maximize product — optimization / AM-GM
    (2000, "A", 20, "Algebra",               "Equations and Expressions",          "Optimization"),
    (2000, "A", 20, "Algebra",               "Inequalities",                       "AM/GM"),

    # Q21: All alligators are ferocious, some creepy crawlers are alligators — logic
    (2000, "A", 21, "Algebra",               "Logic",                              "Making Inferences"),

    # Q22: Angela drank 1/4 of total milk and 1/6 of total coffee — mixture / equations
    (2000, "A", 22, "Algebra",               "Algebraic Application",              "Mixture Problems"),

    # Q23: Mean, median, mode form arithmetic progression — statistics (3 tags)
    (2000, "A", 23, "Algebra",               "Statistics",                         "Mean"),
    (2000, "A", 23, "Algebra",               "Statistics",                         "Median"),
    (2000, "A", 23, "Algebra",               "Statistics",                         "Mode"),

    # Q24: f(3/4 + x) = 1/2 + sqrt(f(x) - f(x)^2), find sum of x where f(x) = 1/3
    (2000, "A", 24, "Algebra",               "Equations and Expressions",          "Functional Equations"),

    # Q25: Year n day 300 is Tuesday, year n+1 day 200 is Tuesday — calendar/modular
    (2000, "A", 25, "Number Theory",         "Modular Arithmetic and Congruences", "Calendar Problems"),
]


if __name__ == "__main__":
    with sqlite3.connect(DB_FILE) as conn:
        deleted = conn.execute(
            f"DELETE FROM {TABLE} WHERE year = 2000 AND version = 'A'"
        ).rowcount
        if deleted:
            print(f"Removed {deleted} existing rows for 2000-A.")

        conn.executemany(
            f"INSERT INTO {TABLE} (year, version, question_num, level_1, level_2, level_3) VALUES (?,?,?,?,?,?)",
            TOPICS,
        )
        print(f"Inserted {len(TOPICS)} topic rows for 2000-A.")

        print("\n--- 2000-A topics ---")
        for row in conn.execute(
            f"SELECT question_num, level_1, level_2, level_3 FROM {TABLE} "
            f"WHERE year=2000 AND version='A' ORDER BY question_num"
        ):
            print(f"  Q{row[0]:>2}  {row[1]:<25} {row[2]:<40} {row[3]}")
