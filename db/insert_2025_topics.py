"""
Classifies the 25 AMC 10A 2025 problems and inserts their topic tags
into the `problems` table, matching the existing level_1/level_2/level_3 taxonomy.
Each problem may generate multiple rows (one per topic tag).
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'amc_problems.db')

# (question_num, level_1, level_2, level_3)
# Classified from the actual 2025 AMC 10A problem texts.
TAGS_2025 = [
    # Q1 – Andy & Betsy speed/direction word problem
    (1,  'Algebra',               'Algebraic Application',             'Speed Distance Time'),

    # Q2 – Nut mix percentages (mixture problem)
    (2,  'Algebra',               'Algebraic Application',             'Mixture Problems'),

    # Q3 – Count isosceles triangles with integer sides, longest side 2025
    (3,  'Counting & Probability','Counting',                          'Casework'),
    (3,  'Geometry',              'Triangle Geometry',                 'Triangle Inequality'),

    # Q4 – Students + teachers = 15, Ash joins, ratio question
    (4,  'Algebra',               'Basic Algebra',                     'Ratio and Proportion'),

    # Q5 – 1,2,1,2,3,2,1,… sequence, find 2025th term
    (5,  'Algebra',               'Sequences and Series',              'Patterns'),

    # Q6 – Equilateral triangle with trisected angles → hexagon angle measure
    (6,  'Geometry',              'Triangle Geometry',                 'Equilateral Triangles'),
    (6,  'Geometry',              'Polygon Geometry',                  'Hexagons'),

    # Q7 – Polynomial remainder theorem: p(1)=4, p(2)=6, find b-a
    (7,  'Algebra',               'Polynomials',                       'Remainder Theorem'),

    # Q8 – Agnes's 4 self-referential truth statements (logic puzzle)
    (8,  'Algebra',               'Logic',                             'Making Inferences'),

    # Q9 – f(x)=100x³-300x²+200x; how many real a so f(x-a) passes through (1,25)
    (9,  'Algebra',               'Polynomials',                       'Factoring Polynomials'),
    (9,  'Algebra',               'Equations and Expressions',         'Solving Equations'),

    # Q10 – Semicircle with chord, smaller semicircle tangent to chord, find area
    (10, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (10, 'Geometry',              'Circle Geometry',                   'Tangent Lines'),

    # Q11 – 1,x,y,z arithmetic and 1,p,q,z geometric (integers, z minimal)
    (11, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (11, 'Algebra',               'Sequences and Series',              'Geometric Sequences'),

    # Q12 – 4-digit passcode: exactly one even, exactly one prime, no zeros
    (12, 'Counting & Probability','Counting',                          'Casework'),

    # Q13 – Infinite nested squares with constant ratio, find alternating-square area ratio
    (13, 'Algebra',               'Sequences and Series',              'Geometric Sequences'),
    (13, 'Geometry',              'Quadrilateral Geometry',            'Square Area'),

    # Q14 – 6 chairs around table; P(both students adjacent AND both teachers adjacent)
    (14, 'Counting & Probability','Probability',                       'Basic Probability'),
    (14, 'Counting & Probability','Counting',                          'Circular Arrangements'),

    # Q15 – Rectangle ABEF, AD⊥DE, AF=7, AB=1, AD=5; find area
    (15, 'Geometry',              'Quadrilateral Geometry',            'Rectangle Area'),
    (15, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),

    # Q16 – Expected number of coins in the fullest jar (3 coins, 3 jars)
    (16, 'Counting & Probability','Probability',                       'Expected Value'),

    # Q17 – 273436 mod N = 16, 272760 mod N = 15; find tens digit of N  (GCD approach)
    (17, 'Number Theory',         'Multiples and Divisors',            'GCD'),
    (17, 'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),

    # Q18 – Harmonic mean of a set; algebra to find the set
    (18, 'Algebra',               'Statistics',                        'Mean'),
    (18, 'Algebra',               'Algebraic Application',             'Speed Distance Time: Harmonic Mean'),

    # Q19 – Array where each row = adjacent sums of row above (starts -1,3,1; ends fixed)
    (19, 'Algebra',               'Sequences and Series',              'Recursively Defined Sequences'),
    (19, 'Counting & Probability','Binomial Coefficients',             'Binomial Theorem'),

    # Q20 – Silo (cylinder), line-of-sight tangent from two external points
    (20, 'Geometry',              'Circle Geometry',                   'Tangent Lines'),
    (20, 'Geometry',              'Solid Geometry',                    'Cylinder'),

    # Q21 – Sum-free subsets of {1,…,n}; find maximum size (parity / pigeonhole)
    (21, 'Number Theory',         'Parity',                            'Parity'),
    (21, 'Counting & Probability','Sets and Partitions',               'Pigeonhole'),

    # Q22 – Radius r circle surrounded by tangent circles of radii 1, 2, 3 (Descartes)
    (22, 'Geometry',              'Circle Geometry',                   'Tangent Circles'),
    (22, 'Geometry',              'Circle Geometry',                   'Descartes'),

    # Q23 – Triangle AB=80, BC=45, AC=75; bisector of ∠B meets altitude to AB at P; find BP
    (23, 'Geometry',              'Triangle Geometry',                 'Angle Bisector Theorem'),
    (23, 'Geometry',              'Triangle Geometry',                 'Altitudes'),

    # Q24 – Count "fair" positive integers (no repeats, no 0, no digit flanked by two larger)
    (24, 'Counting & Probability','Counting',                          'Casework'),
    (24, 'Counting & Probability','Counting',                          'Complementary Counting'),

    # Q25 – P inside square ABCD; P(AP neither shortest nor longest side of △APB)
    (25, 'Counting & Probability','Probability',                       'Geometric Probability'),
    (25, 'Geometry',              'Circle Geometry',                   'Circle Area'),
]


def insert_tags():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Remove any previously inserted 2025 rows to allow safe re-runs
    deleted = cur.execute(
        "DELETE FROM problems WHERE year = 2025 AND version = 'A'"
    ).rowcount
    if deleted:
        print(f"Removed {deleted} existing 2025-A rows before re-inserting.")

    rows = [(2025, 'A', q, l1, l2, l3) for q, l1, l2, l3 in TAGS_2025]
    cur.executemany(
        "INSERT INTO problems (year, version, question_num, level_1, level_2, level_3) VALUES (?,?,?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"Inserted {cur.rowcount} topic tag rows for 2025 AMC 10A.")

    # Verification
    print("\n=== 2025 topic tags inserted ===")
    result = conn.execute("""
        SELECT question_num, level_1, level_2, level_3
        FROM problems WHERE year = 2025 AND version = 'A'
        ORDER BY question_num, level_1, level_2
    """).fetchall()
    for r in result:
        print(f"  Q{r[0]:2d}  {r[1]:<25} {r[2]:<40} {r[3]}")

    print(f"\nTotal rows for 2025-A: {len(result)}")
    conn.close()


if __name__ == '__main__':
    insert_tags()
