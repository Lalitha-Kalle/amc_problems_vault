"""
Classifies the 25 AMC 10B 2024 problems and inserts their topic tags
into the `problems` table, matching the existing level_1/level_2/level_3 taxonomy.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'amc_problems.db')

# (question_num, level_1, level_2, level_3)
TAGS_2024_B = [
    # Q1 – 1013th from left is 1010th from right; total people in line
    (1,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q2 – Evaluate an arithmetic/algebraic expression
    (2,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),

    # Q3 – Count integer values satisfying an inequality/equation
    (3,  'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (3,  'Number Theory',         'Multiples and Divisors',            'Divisibility'),

    # Q4 – Balls deposited in 5 bins by pattern; find which bin ball N lands in
    (4,  'Algebra',               'Sequences and Series',              'Patterns'),
    (4,  'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),

    # Q5 – Change + to – in sum; least changes to make expression negative
    (5,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (5,  'Counting & Probability','Counting',                          'Casework'),

    # Q6 – Rectangle with integer sides, area 2024; least perimeter
    (6,  'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (6,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q7 – Remainder when expression is divided by n (modular arithmetic)
    (7,  'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),

    # Q8 – Product of all positive divisors of n; find units digit
    (8,  'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),

    # Q9 – Arithmetic mean of variables; find mean of another combination
    (9,  'Algebra',               'Statistics',                        'Mean'),
    (9,  'Algebra',               'Basic Algebra',                     'System of Equations'),

    # Q10 – Parallelogram ABCD, midpoint, intersection; ratio of areas
    (10, 'Geometry',              'Quadrilateral Geometry',            'Parallelograms'),
    (10, 'Geometry',              'Triangle Geometry',                 'Triangle Area'),

    # Q11 – Rectangle with right-angle point; equal triangle areas; find area
    (11, 'Geometry',              'Quadrilateral Geometry',            'Rectangle Area'),
    (11, 'Geometry',              'Triangle Geometry',                 'Triangle Area'),

    # Q12 – Students speak languages; every pair shares a language; combinatorics
    (12, 'Counting & Probability','Counting',                          'Casework'),

    # Q13 – Positive integers satisfying equation; minimum value
    (13, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (13, 'Algebra',               'Equations and Expressions',         'Solving Equations'),

    # Q14 – Dartboard regions; geometric probability
    (14, 'Counting & Probability','Probability',                       'Geometric Probability'),
    (14, 'Geometry',              'Coordinate Geometry',               'Distance Formula'),

    # Q15 – List of reals; range, mean, median all constrained; count ordered triples
    (15, 'Algebra',               'Statistics',                        'Mean'),
    (15, 'Counting & Probability','Counting',                          'Casework'),

    # Q16 – Integers on whiteboard; replace 4 numbers by sum or product; parity invariant
    (16, 'Number Theory',         'Parity',                            'Parity'),
    (16, 'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),

    # Q17 – Race with ties; count possible finishing orders for n snails
    (17, 'Counting & Probability','Counting',                          'Casework'),

    # Q18 – Count distinct remainders when n-th power divided by m
    (18, 'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),
    (18, 'Counting & Probability','Counting',                          'Casework'),

    # Q19 – Table: which slopes allow given number of lattice points on a line
    (19, 'Geometry',              'Coordinate Geometry',               'Lattice Points'),
    (19, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),

    # Q20 – Three pairs of shoes in a row; no left shoe next to right of different pair
    (20, 'Counting & Probability','Counting',                          'Arrangements'),
    (20, 'Counting & Probability','Counting',                          'Casework'),

    # Q21 – Two cylinders on flat floor; find possible radii of third tangent cylinder
    (21, 'Geometry',              'Circle Geometry',                   'Tangent Circles'),
    (21, 'Geometry',              'Solid Geometry',                    'Cylinder'),

    # Q22 – Group partitioned into k-person committees; chair + secretary assignments
    (22, 'Counting & Probability','Counting',                          'Committee Selection'),

    # Q23 – Fibonacci numbers; find a closed-form sum
    (23, 'Algebra',               'Sequences and Series',              'Fibonacci Sequences'),
    (23, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),

    # Q24 – Function values; how many are integers (floor/divisibility check)
    (24, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (24, 'Algebra',               'Equations and Expressions',         'Solving Equations'),

    # Q25 – Bricks with pairwise-coprime dimensions forming a block; count bricks
    (25, 'Number Theory',         'Primes and Composites',             'Prime Factorization'),
    (25, 'Number Theory',         'Multiples and Divisors',            'GCD'),
    (25, 'Geometry',              'Solid Geometry',                    'Volume'),
]


def insert_tags():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    deleted = cur.execute(
        "DELETE FROM problems WHERE year = 2024 AND version = 'B'"
    ).rowcount
    if deleted:
        print(f"Removed {deleted} existing 2024-B rows before re-inserting.")

    rows = [(2024, 'B', q, l1, l2, l3) for q, l1, l2, l3 in TAGS_2024_B]
    cur.executemany(
        "INSERT INTO problems (year, version, question_num, level_1, level_2, level_3) VALUES (?,?,?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"Inserted {len(rows)} topic tag rows for 2024 AMC 10B.")

    result = conn.execute("""
        SELECT question_num, level_1, level_2, level_3
        FROM problems WHERE year = 2024 AND version = 'B'
        ORDER BY question_num, level_1
    """).fetchall()
    for r in result:
        print(f"  Q{r[0]:2d}  {r[1]:<25} {r[2]:<40} {r[3]}")

    print(f"\nTotal rows for 2024-B: {len(result)}")
    conn.close()


if __name__ == '__main__':
    insert_tags()
