"""
Classifies the 25 AMC 10A 2024 problems and inserts their topic tags
into the `problems` table, matching the existing level_1/level_2/level_3 taxonomy.
Each problem may generate multiple rows (one per topic tag).
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'amc_problems.db')

# (question_num, level_1, level_2, level_3)
TAGS_2024 = [
    # Q1 – Evaluate arithmetic expression (order of operations / algebraic manipulation)
    (1,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),

    # Q2 – Hiking time model T = aD + bG; solve for constants using two data points
    (2,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (2,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q3 – Least prime that is the sum of distinct prime numbers
    (3,  'Number Theory',         'Primes and Composites',             'Primes'),

    # Q4 – Write 2024 as a sum of fewest two-digit numbers
    (4,  'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (4,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),

    # Q5 – Least n such that n! is a multiple of a given number
    (5,  'Number Theory',         'Primes and Composites',             'Prime Factorization'),
    (5,  'Number Theory',         'Primes and Composites',             'Factorials'),

    # Q6 – Minimum adjacent letter swaps to rearrange ABCABC to a target string
    (6,  'Counting & Probability','Counting',                          'Rearrangements'),
    (6,  'Counting & Probability','Counting',                          'Casework'),

    # Q7 – Product of three integers = N; find least possible positive sum
    (7,  'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),

    # Q8 – Amy/Bomani/Charlie/Daria packing chocolates at given rates; finish together
    (8,  'Algebra',               'Algebraic Application',             'Work Problems'),

    # Q9 – Juniors and seniors forming disjoint teams with fixed composition
    (9,  'Counting & Probability','Counting',                          'Committee Selection'),

    # Q10 – Recursive operation (÷4 if divisible by 4, else +4); find value after N steps
    (10, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (10, 'Algebra',               'Sequences and Series',              'Recursively Defined Sequences'),

    # Q11 – Count ordered integer pairs satisfying a given equation
    (11, 'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (11, 'Counting & Probability','Counting',                          'Casework'),

    # Q12 – Bar chart of daily score changes; find average score over the period
    (12, 'Algebra',               'Statistics',                        'Mean'),

    # Q13 – Which pairs of four transformations (translate, rotate, reflect, dilate) commute
    (13, 'Geometry',              'Transformations',                   'Translations'),
    (13, 'Geometry',              'Transformations',                   'Rotations'),
    (13, 'Geometry',              'Transformations',                   'Reflections'),

    # Q14 – Equilateral triangle on a line; circle tangent to line and triangle; find area
    (14, 'Geometry',              'Triangle Geometry',                 'Equilateral Triangles'),
    (14, 'Geometry',              'Circle Geometry',                   'Tangent Lines'),
    (14, 'Geometry',              'Circle Geometry',                   'Circle Area'),

    # Q15 – Greatest integer n so that two expressions are both perfect squares
    (15, 'Number Theory',         'Multiples and Divisors',            'Perfect Squares'),

    # Q16 – Figure of similar rectangles with areas labelled; find a side length
    (16, 'Geometry',              'Quadrilateral Geometry',            'Rectangle Area'),
    (16, 'Algebra',               'Basic Algebra',                     'Ratio and Proportion'),

    # Q17 – Best-of-3 playoff; home/away win probabilities; find P(team A wins series)
    (17, 'Counting & Probability','Probability',                       'Basic Probability'),
    (17, 'Counting & Probability','Probability',                       'Tree Diagram'),

    # Q18 – Count positive integers where a base-b representation is divisible by a given n
    (18, 'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),
    (18, 'Counting & Probability','Counting',                          'Casework'),

    # Q19 – Geometric sequence with three integer first terms; minimize and find digit sum
    (19, 'Algebra',               'Sequences and Series',              'Geometric Sequences'),
    (19, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),

    # Q20 – Max-size subset of integers with two pairwise-difference conditions
    (20, 'Counting & Probability','Sets and Partitions',               'Pigeonhole'),
    (20, 'Number Theory',         'Parity',                            'Parity'),

    # Q21 – 5×5 array where every row and column is an AP; find a missing entry
    (21, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),

    # Q22 – Kite from two right triangles; 8 copies form polygon; find triangle area
    (22, 'Geometry',              'Quadrilateral Geometry',            'Kite Area'),
    (22, 'Geometry',              'Triangle Geometry',                 'Triangle Area'),

    # Q23 – Integers a, b, c satisfying a system of conditions; find the target value
    (23, 'Algebra',               'Equations and Expressions',         'System of Equations'),
    (23, 'Number Theory',         'Modular Arithmetic and Congruences','Mods'),

    # Q24 – Bee moves in 3-D based on die rolls; find expected squared distance from origin
    (24, 'Counting & Probability','Probability',                       'Expected Value'),
    (24, 'Geometry',              'Coordinate Geometry',               'Distance Formula'),

    # Q25 – Toothpick closed loop on a dotted grid satisfying cell-side counts
    (25, 'Counting & Probability','Counting',                          'Toothpick Problems'),
    (25, 'Counting & Probability','Counting',                          'Casework'),
]


def insert_tags():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    deleted = cur.execute(
        "DELETE FROM problems WHERE year = 2024 AND version = 'A'"
    ).rowcount
    if deleted:
        print(f"Removed {deleted} existing 2024-A rows before re-inserting.")

    rows = [(2024, 'A', q, l1, l2, l3) for q, l1, l2, l3 in TAGS_2024]
    cur.executemany(
        "INSERT INTO problems (year, version, question_num, level_1, level_2, level_3) VALUES (?,?,?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"Inserted {len(rows)} topic tag rows for 2024 AMC 10A.")

    print("\n=== 2024 topic tags inserted ===")
    result = conn.execute("""
        SELECT question_num, level_1, level_2, level_3
        FROM problems WHERE year = 2024 AND version = 'A'
        ORDER BY question_num, level_1, level_2
    """).fetchall()
    for r in result:
        print(f"  Q{r[0]:2d}  {r[1]:<25} {r[2]:<40} {r[3]}")

    print(f"\nTotal rows for 2024-A: {len(result)}")
    conn.close()


if __name__ == '__main__':
    insert_tags()
