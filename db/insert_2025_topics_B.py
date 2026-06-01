"""
Classifies the 25 AMC 10B 2025 problems and inserts their topic tags
into the `problems` table, matching the existing level_1/level_2/level_3 taxonomy.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'amc_problems.db')

# (question_num, level_1, level_2, level_3)
TAGS_2025_B = [
    # Q1 – Coffee-bean bag; greatest number of properly brewed mugs (division / floor)
    (1,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q2 – Ones digit of first n positive squares; find their sum (digit patterns)
    (2,  'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),
    (2,  'Number Theory',         'Parity',                            'Parity'),

    # Q3 – Pascal-like triangle; find an entry (binomial / recursive sums)
    (3,  'Counting & Probability','Binomial Coefficients',             'Binomial Theorem'),
    (3,  'Algebra',               'Sequences and Series',              'Patterns'),

    # Q4 – Two-digit number in base 7 equals two-digit number in base 9; find value
    (4,  'Number Theory',         'Modular Arithmetic and Congruences','Number Bases'),

    # Q5 – Triangle with circumcircle; find degree measure of angle at centre
    (5,  'Geometry',              'Circle Geometry',                   'Central and Inscribed Angles'),
    (5,  'Geometry',              'Triangle Geometry',                 'Triangle Geometry'),

    # Q6 – Line divides square region; lower half split into equal areas; find slope
    (6,  'Geometry',              'Coordinate Geometry',               'Area of Regions'),
    (6,  'Algebra',               'Equations and Expressions',         'Solving Equations'),

    # Q7 – Minimum-distance path from Frances to chocolate box via two gates (optimisation)
    (7,  'Geometry',              'Coordinate Geometry',               'Distance Formula'),
    (7,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q8 – 36 shirts, total cost is a 4-digit number with given digit constraint; find price
    (8,  'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (8,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q9 – Count ordered integer triples satisfying a system of inequalities
    (9,  'Counting & Probability','Counting',                          'Casework'),
    (9,  'Algebra',               'Equations and Expressions',         'Solving Equations'),

    # Q10 – Sum of integers n so that a rational expression is an integer
    (10, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (10, 'Algebra',               'Equations and Expressions',         'Solving Equations'),

    # Q11 – Students randomly assigned to tutors; P(no student gets same tutor twice)
    (11, 'Counting & Probability','Probability',                       'Basic Probability'),
    (11, 'Counting & Probability','Counting',                          'Arrangements'),

    # Q12 – Equilateral triangle, rhombus, hexagon with mutually tangent disks; ratio of radii
    (12, 'Geometry',              'Circle Geometry',                   'Tangent Circles'),
    (12, 'Geometry',              'Triangle Geometry',                 'Equilateral Triangles'),

    # Q13 – Altitude to hypotenuse divided by median; find ratio of segments
    (13, 'Geometry',              'Triangle Geometry',                 'Altitudes'),
    (13, 'Geometry',              'Triangle Geometry',                 'Medians'),

    # Q14 – Nine athletes draw wristbands; probability of satisfying height/colour condition
    (14, 'Counting & Probability','Probability',                       'Basic Probability'),
    (14, 'Counting & Probability','Counting',                          'Casework'),

    # Q15 – Telescoping or partial-fraction sum; express as a/b, find a + b
    (15, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (15, 'Number Theory',         'Multiples and Divisors',            'GCD'),

    # Q16 – Circle divided into 6 sectors; colour 2 each in 3 colours, no adjacent same colour
    (16, 'Counting & Probability','Counting',                          'Circular Arrangements'),
    (16, 'Counting & Probability','Counting',                          'Casework'),

    # Q17 – Decreasing sequence; average of first k terms satisfies conditions; find n
    (17, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (17, 'Algebra',               'Statistics',                        'Mean'),

    # Q18 – Ones digit of sum involving floor function
    (18, 'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),
    (18, 'Number Theory',         'Parity',                            'Parity'),

    # Q19 – Trapezoidal-sided container filled at constant rate; find height at given time
    (19, 'Geometry',              'Solid Geometry',                    'Volume'),
    (19, 'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q20 – Four congruent semicircles inscribed in unit square; find area of overlap region
    (20, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (20, 'Geometry',              'Quadrilateral Geometry',            'Square Area'),

    # Q21 – Grid coloured red/blue/yellow with edge-sharing constraints; count colourings
    (21, 'Counting & Probability','Counting',                          'Casework'),
    (21, 'Counting & Probability','Sets and Partitions',               'Coloring Problems'),

    # Q22 – Random 7-digit number; P(divisible by n | digit sum = k)
    (22, 'Counting & Probability','Probability',                       'Basic Probability'),
    (22, 'Number Theory',         'Modular Arithmetic and Congruences','Divisibility'),

    # Q23 – Two people fill a grid with 1–mn; compare row/column sums (pigeonhole / algebra)
    (23, 'Counting & Probability','Counting',                          'Arrangements'),
    (23, 'Algebra',               'Statistics',                        'Mean'),

    # Q24 – Frog hops on number line with probabilistic rules; find expected position
    (24, 'Counting & Probability','Probability',                       'Expected Value'),
    (24, 'Counting & Probability','Probability',                       'Basic Probability'),

    # Q25 – Path in square reflecting off sides; find length or number of reflections
    (25, 'Geometry',              'Coordinate Geometry',               'Reflections'),
    (25, 'Geometry',              'Quadrilateral Geometry',            'Square Area'),
]


def insert_tags():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    deleted = cur.execute(
        "DELETE FROM problems WHERE year = 2025 AND version = 'B'"
    ).rowcount
    if deleted:
        print(f"Removed {deleted} existing 2025-B rows before re-inserting.")

    rows = [(2025, 'B', q, l1, l2, l3) for q, l1, l2, l3 in TAGS_2025_B]
    cur.executemany(
        "INSERT INTO problems (year, version, question_num, level_1, level_2, level_3) VALUES (?,?,?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"Inserted {len(rows)} topic tag rows for 2025 AMC 10B.")

    result = conn.execute("""
        SELECT question_num, level_1, level_2, level_3
        FROM problems WHERE year = 2025 AND version = 'B'
        ORDER BY question_num, level_1
    """).fetchall()
    for r in result:
        print(f"  Q{r[0]:2d}  {r[1]:<25} {r[2]:<40} {r[3]}")

    print(f"\nTotal rows for 2025-B: {len(result)}")
    conn.close()


if __name__ == '__main__':
    insert_tags()
