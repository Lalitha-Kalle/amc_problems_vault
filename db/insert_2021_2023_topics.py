"""
Topic tags for AMC 10 2021A, 2021B, 2022A, 2022B, 2023A, 2023B.
Classified by scanning each problem's content directly.
"""

import sqlite3, os
from pathlib import Path

DB_PATH = Path(__file__).parent / "amc_problems.db"

# ── 2021 AMC 10A ──────────────────────────────────────────────────────────────
TAGS_2021A = [
    (1,  'Algebra',               'Basic Algebra',                     'Order of Operations'),
    (2,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (3,  'Number Theory',         'Place Values',                      'Place Value'),
    (3,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (4,  'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (5,  'Algebra',               'Statistics',                        'Mean'),
    (5,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (6,  'Algebra',               'Algebraic Application',             'Speed Distance Time'),
    (7,  'Algebra',               'Logic',                             'Making Inferences'),
    (8,  'Number Theory',         'Decimal Representation',            'Decimal Representation'),
    (8,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (9,  'Algebra',               'Equations and Expressions',         'Optimization'),
    (9,  'Algebra',               'Inequalities',                      'AM/GM'),
    (10, 'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (10, 'Algebra',               'Sequences and Series',              'Telescoping'),
    (11, 'Number Theory',         'Bases',                             'Bases'),
    (11, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (12, 'Geometry',              'Solid Geometry',                    'Volume'),
    (13, 'Geometry',              'Solid Geometry',                    'Volume'),
    (13, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (14, 'Algebra',               'Polynomials',                       "Vieta's"),
    (15, 'Counting & Probability','Counting',                          'Casework'),
    (15, 'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (16, 'Algebra',               'Statistics',                        'Median'),
    (16, 'Algebra',               'Sequences and Series',              'Patterns'),
    (17, 'Geometry',              'Quadrilateral Geometry',            'Trapezoid Area'),
    (17, 'Geometry',              'Triangle Geometry',                 'Similar Triangles'),
    (18, 'Algebra',               'Equations and Expressions',         'Functional Equations'),
    (18, 'Number Theory',         'Primes and Composites',             'Prime Factorization'),
    (19, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (19, 'Algebra',               'Special Functions',                 'Absolute Values'),
    (20, 'Counting & Probability','Counting',                          'Arrangements'),
    (20, 'Counting & Probability','Counting',                          'Casework'),
    (21, 'Geometry',              'Polygon Geometry',                  'Hexagons'),
    (21, 'Geometry',              'Triangle Geometry',                 'Similar Triangles'),
    (22, 'Algebra',               'Sequences and Series',              'Consecutive Integers'),
    (22, 'Counting & Probability','Counting',                          'Casework'),
    (23, 'Counting & Probability','Probability',                       'Basic Probability'),
    (24, 'Algebra',               'Coordinate Geometry',               'Region bounded by Graphs'),
    (24, 'Algebra',               'Special Functions',                 'Absolute Values'),
    (25, 'Counting & Probability','Counting',                          'Arrangements'),
    (25, 'Counting & Probability','Counting',                          'Casework'),
]

# ── 2021 AMC 10B ──────────────────────────────────────────────────────────────
TAGS_2021B = [
    (1,  'Algebra',               'Special Functions',                 'Absolute Values'),
    (2,  'Algebra',               'Exponents and Radicals',            'Radicals'),
    (2,  'Algebra',               'Special Functions',                 'Absolute Values'),
    (3,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (3,  'Algebra',               'Basic Algebra',                     'Percentages'),
    (4,  'Counting & Probability','Counting',                          'Casework'),
    (5,  'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (5,  'Counting & Probability','Counting',                          'Casework'),
    (6,  'Algebra',               'Statistics',                        'Mean'),
    (6,  'Algebra',               'Basic Algebra',                     'Ratio and Proportion'),
    (7,  'Geometry',              'Circle Geometry',                   'Circle Area'),
    (7,  'Counting & Probability','Counting',                          'Casework'),
    (8,  'Algebra',               'Sequences and Series',              'Patterns'),
    (8,  'Number Theory',         'Place Values',                      'Place Value'),
    (9,  'Geometry',              'Transformations',                   'Rotations'),
    (9,  'Geometry',              'Transformations',                   'Reflections'),
    (10, 'Geometry',              'Solid Geometry',                    'Volume'),
    (10, 'Geometry',              'Solid Geometry',                    'Cylinder'),
    (11, 'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (11, 'Algebra',               'Algebraic Application',             'Basic Word Problems'),
    (12, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (12, 'Number Theory',         'Primes and Composites',             'Prime Factorization'),
    (13, 'Number Theory',         'Bases',                             'Bases'),
    (13, 'Algebra',               'Equations and Expressions',         'System of Equations'),
    (14, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (14, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (15, 'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (15, 'Algebra',               'Polynomials',                       'Factoring Polynomials'),
    (16, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (16, 'Number Theory',         'Place Values',                      'Place Value'),
    (17, 'Algebra',               'Logic',                             'Determining Order'),
    (17, 'Algebra',               'Equations and Expressions',         'System of Equations'),
    (18, 'Counting & Probability','Probability',                       'Conditional Probability'),
    (18, 'Counting & Probability','Counting',                          'Casework'),
    (19, 'Algebra',               'Statistics',                        'Mean'),
    (19, 'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (20, 'Geometry',              'Triangle Geometry',                 'Triangle Area'),
    (20, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (21, 'Geometry',              'Quadrilateral Geometry',            'Square Area'),
    (21, 'Geometry',              'Triangle Geometry',                 'Similar Triangles'),
    (22, 'Counting & Probability','Probability',                       'Basic Probability'),
    (22, 'Counting & Probability','Counting',                          'Casework'),
    (23, 'Counting & Probability','Probability',                       'Geometric Probability'),
    (23, 'Geometry',              'Triangle Geometry',                 'Triangle Area'),
    (24, 'Counting & Probability','Counting',                          'Casework'),
    (25, 'Geometry',              'Coordinate Geometry',               'Lattice Points'),
    (25, 'Algebra',               'Coordinate Geometry',               'Equation of Lines'),
]

# ── 2022 AMC 10A ──────────────────────────────────────────────────────────────
TAGS_2022A = [
    (1,  'Algebra',               'Fractions',                         'Continued Fractions'),
    (2,  'Algebra',               'Basic Algebra',                     'Ratio and Proportion'),
    (3,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (4,  'Algebra',               'Basic Algebra',                     'Unit Conversions'),
    (5,  'Geometry',              'Quadrilateral Geometry',            'Square Area'),
    (5,  'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (6,  'Algebra',               'Special Functions',                 'Absolute Values'),
    (6,  'Algebra',               'Exponents and Radicals',            'Radicals'),
    (7,  'Number Theory',         'Multiples and Divisors',            'LCM'),
    (7,  'Number Theory',         'Multiples and Divisors',            'GCD'),
    (8,  'Algebra',               'Statistics',                        'Mean'),
    (8,  'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (9,  'Counting & Probability','Counting',                          'Casework'),
    (10, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (10, 'Algebra',               'Equations and Expressions',         'Setting up Equations'),
    (11, 'Algebra',               'Exponents and Radicals',            'Exponential Equations'),
    (11, 'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (12, 'Algebra',               'Logic',                             'Truth vs. Lies'),
    (13, 'Geometry',              'Triangle Geometry',                 'Angle Bisector Theorem'),
    (13, 'Geometry',              'Triangle Geometry',                 'Similar Triangles'),
    (14, 'Counting & Probability','Counting',                          'Casework'),
    (15, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (15, 'Geometry',              'Triangle Geometry',                 'Right Triangles'),
    (16, 'Algebra',               'Polynomials',                       "Vieta's"),
    (16, 'Geometry',              'Solid Geometry',                    'Volume'),
    (17, 'Number Theory',         'Decimal Representation',            'Decimal Representation'),
    (17, 'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (18, 'Geometry',              'Transformations',                   'Rotations'),
    (18, 'Geometry',              'Transformations',                   'Reflections'),
    (18, 'Number Theory',         'Modular Arithmetic and Congruences','Mods'),
    (19, 'Number Theory',         'Multiples and Divisors',            'LCM'),
    (19, 'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),
    (20, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (20, 'Algebra',               'Sequences and Series',              'Geometric Sequences'),
    (21, 'Geometry',              'Polygon Geometry',                  'Hexagons'),
    (21, 'Geometry',              'Polygon Geometry',                  'Regular Polygons'),
    (22, 'Counting & Probability','Counting',                          'Arrangements'),
    (22, 'Counting & Probability','Counting',                          'Casework'),
    (23, 'Geometry',              'Quadrilateral Geometry',            'Trapezoid Area'),
    (23, 'Algebra',               'Equations and Expressions',         'Setting up Equations'),
    (24, 'Counting & Probability','Counting',                          'Casework'),
    (24, 'Counting & Probability','Counting',                          'Constructive Counting'),
    (25, 'Geometry',              'Coordinate Geometry',               'Lattice Points'),
    (25, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
]

# ── 2022 AMC 10B ──────────────────────────────────────────────────────────────
TAGS_2022B = [
    (1,  'Algebra',               'Functions',                         'Special Operations'),
    (1,  'Algebra',               'Special Functions',                 'Absolute Values'),
    (2,  'Geometry',              'Quadrilateral Geometry',            'Parallelograms'),
    (2,  'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (3,  'Counting & Probability','Counting',                          'Casework'),
    (4,  'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (4,  'Number Theory',         'Modular Arithmetic and Congruences','Remainders'),
    (5,  'Algebra',               'Fractions',                         'Comparing Fractions'),
    (5,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (6,  'Number Theory',         'Primes and Composites',             'Primes'),
    (6,  'Algebra',               'Sequences and Series',              'Patterns'),
    (7,  'Algebra',               'Polynomials',                       "Vieta's"),
    (7,  'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (8,  'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (8,  'Counting & Probability','Counting',                          'Casework'),
    (9,  'Algebra',               'Sequences and Series',              'Telescoping'),
    (9,  'Algebra',               'Special Functions',                 'Factorials'),
    (10, 'Algebra',               'Statistics',                        'Mean'),
    (10, 'Algebra',               'Statistics',                        'Median'),
    (10, 'Algebra',               'Statistics',                        'Mode'),
    (11, 'Algebra',               'Logic',                             'Logic'),
    (11, 'Algebra',               'Logic',                             'Making Inferences'),
    (12, 'Counting & Probability','Probability',                       'Basic Probability'),
    (13, 'Number Theory',         'Primes and Composites',             'Primes'),
    (13, 'Algebra',               'Equations and Expressions',         'Setting up Equations'),
    (14, 'Counting & Probability','Sets and Partitions',               'Pigeonhole'),
    (14, 'Number Theory',         'Parity',                            'Parity'),
    (15, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (16, 'Geometry',              'Quadrilateral Geometry',            'Square Area'),
    (16, 'Geometry',              'Quadrilateral Geometry',            'Rectangle Area'),
    (16, 'Geometry',              'Triangle Geometry',                 'Triangle Area'),
    (17, 'Number Theory',         'Modular Arithmetic and Congruences','Mods'),
    (17, 'Number Theory',         'Primes and Composites',             'Primes'),
    (18, 'Counting & Probability','Counting',                          'Casework'),
    (18, 'Algebra',               'Equations and Expressions',         'System of Equations'),
    (19, 'Algebra',               'Logic',                             'Logic'),
    (19, 'Counting & Probability','Counting',                          'Casework'),
    (20, 'Geometry',              'Angle Geometry',                    'Angle Chasing'),
    (20, 'Geometry',              'Quadrilateral Geometry',            'Parallelograms'),
    (21, 'Algebra',               'Polynomials',                       'Remainder Theorem'),
    (21, 'Algebra',               'Equations and Expressions',         'System of Equations'),
    (22, 'Geometry',              'Circle Geometry',                   'Tangent Circles'),
    (22, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (23, 'Counting & Probability','Probability',                       'Expected Value'),
    (23, 'Counting & Probability','Probability',                       'Basic Probability'),
    (24, 'Algebra',               'Inequalities',                      'Inequalities'),
    (24, 'Algebra',               'Equations and Expressions',         'Optimization'),
    (25, 'Number Theory',         'Modular Arithmetic and Congruences','Mods'),
    (25, 'Number Theory',         'Bases',                             'Bases'),
]

# ── 2023 AMC 10A ──────────────────────────────────────────────────────────────
TAGS_2023A = [
    (1,  'Algebra',               'Algebraic Application',             'Speed Distance Time'),
    (2,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (2,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),
    (3,  'Number Theory',         'Multiples and Divisors',            'Perfect Squares'),
    (3,  'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (4,  'Geometry',              'Triangle Geometry',                 'Triangle Inequality'),
    (4,  'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (5,  'Number Theory',         'Primes and Composites',             'Prime Factorization'),
    (5,  'Number Theory',         'Place Values',                      'Place Value'),
    (6,  'Algebra',               'Basic Algebra',                     'Algebraic Manipulations'),
    (7,  'Counting & Probability','Probability',                       'Basic Probability'),
    (7,  'Counting & Probability','Counting',                          'Casework'),
    (8,  'Algebra',               'Coordinate Geometry',               'Equation of Lines'),
    (8,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (9,  'Counting & Probability','Counting',                          'Casework'),
    (10, 'Algebra',               'Statistics',                        'Mean'),
    (10, 'Algebra',               'Basic Algebra',                     'System of Equations'),
    (11, 'Geometry',              'Quadrilateral Geometry',            'Square Area'),
    (11, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (12, 'Number Theory',         'Multiples and Divisors',            'Divisibility'),
    (12, 'Counting & Probability','Counting',                          'Casework'),
    (13, 'Geometry',              'Circle Geometry',                   'Inscribed Angles'),
    (13, 'Geometry',              'Trigonometry',                      'Law of Cosines'),
    (14, 'Counting & Probability','Probability',                       'Basic Probability'),
    (14, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (15, 'Geometry',              'Circle Geometry',                   'Circle Area'),
    (15, 'Algebra',               'Sequences and Series',              'Geometric Sequences'),
    (16, 'Algebra',               'Algebraic Application',             'Basic Word Problems'),
    (16, 'Algebra',               'Basic Algebra',                     'System of Equations'),
    (17, 'Geometry',              'Triangle Geometry',                 'Pythagorean Theorem'),
    (17, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (18, 'Geometry',              'Solid Geometry',                    "Euler's Polyhedron Formula"),
    (19, 'Geometry',              'Transformations',                   'Rotations'),
    (19, 'Algebra',               'Coordinate Geometry',               'Distance Formula'),
    (20, 'Counting & Probability','Counting',                          'Casework'),
    (21, 'Algebra',               'Polynomials',                       'Factoring Polynomials'),
    (21, 'Algebra',               'Polynomials',                       "Vieta's"),
    (22, 'Geometry',              'Circle Geometry',                   'Tangent Circles'),
    (23, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (23, 'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (24, 'Geometry',              'Polygon Geometry',                  'Hexagons'),
    (24, 'Algebra',               'Equations and Expressions',         'Setting up Equations'),
    (25, 'Counting & Probability','Counting',                          'Casework'),
    (25, 'Geometry',              'Solid Geometry',                    "Euler's Polyhedron Formula"),
]

# ── 2023 AMC 10B ──────────────────────────────────────────────────────────────
TAGS_2023B = [
    (1,  'Algebra',               'Basic Algebra',                     'Fractions'),
    (1,  'Algebra',               'Algebraic Application',             'Basic Word Problems'),
    (2,  'Algebra',               'Basic Algebra',                     'Percentages'),
    (3,  'Geometry',              'Circle Geometry',                   'Circle Area'),
    (3,  'Geometry',              'Triangle Geometry',                 'Circumcircles'),
    (4,  'Algebra',               'Basic Algebra',                     'Unit Conversions'),
    (5,  'Algebra',               'Basic Algebra',                     'System of Equations'),
    (6,  'Algebra',               'Sequences and Series',              'Fibonacci Sequences'),
    (6,  'Number Theory',         'Parity',                            'Parity'),
    (7,  'Geometry',              'Transformations',                   'Rotations'),
    (7,  'Geometry',              'Angle Geometry',                    'Angle Chasing'),
    (8,  'Number Theory',         'Modular Arithmetic and Congruences','Last Digits'),
    (9,  'Number Theory',         'Multiples and Divisors',            'Perfect Squares'),
    (9,  'Algebra',               'Sequences and Series',              'Consecutive Integers'),
    (10, 'Algebra',               'Logic',                             'Logic'),
    (10, 'Counting & Probability','Counting',                          'Casework'),
    (11, 'Counting & Probability','Counting',                          'Casework'),
    (11, 'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (12, 'Algebra',               'Polynomials',                       'Factoring Polynomials'),
    (12, 'Number Theory',         'Parity',                            'Parity'),
    (13, 'Algebra',               'Special Functions',                 'Absolute Values'),
    (13, 'Algebra',               'Coordinate Geometry',               'Region bounded by Graphs'),
    (14, 'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (14, 'Number Theory',         'Multiples and Divisors',            'Factors and Multiples'),
    (15, 'Number Theory',         'Primes and Composites',             'Prime Factorization'),
    (15, 'Number Theory',         'Multiples and Divisors',            'Perfect Squares'),
    (16, 'Counting & Probability','Counting',                          'Casework'),
    (16, 'Number Theory',         'Place Values',                      'Place Value'),
    (17, 'Algebra',               'Polynomials',                       "Vieta's"),
    (17, 'Geometry',              'Solid Geometry',                    'Volume'),
    (18, 'Number Theory',         'Multiples and Divisors',            'GCD'),
    (18, 'Number Theory',         'Primes and Composites',             'Relatively Prime'),
    (19, 'Counting & Probability','Probability',                       'Geometric Probability'),
    (20, 'Geometry',              'Solid Geometry',                    'Sphere Volume'),
    (20, 'Geometry',              'Circle Geometry',                   'Arc Length'),
    (21, 'Counting & Probability','Probability',                       'Basic Probability'),
    (21, 'Counting & Probability','Binomial Coefficients',             'Binomial Theorem'),
    (22, 'Algebra',               'Special Functions',                 'Floor Function'),
    (22, 'Algebra',               'Equations and Expressions',         'Solving Equations'),
    (23, 'Algebra',               'Sequences and Series',              'Arithmetic Sequences'),
    (23, 'Algebra',               'Equations and Expressions',         'Diophantine Equations'),
    (24, 'Algebra',               'Coordinate Geometry',               'Shoelace'),
    (24, 'Geometry',              'Coordinate Geometry',               'Distance Formula'),
    (25, 'Geometry',              'Polygon Geometry',                  'Pentagons'),
    (25, 'Geometry',              'Triangle Geometry',                 'Similar Triangles'),
]

# ── insert ────────────────────────────────────────────────────────────────────
ALL = [
    (2021, 'A', TAGS_2021A),
    (2021, 'B', TAGS_2021B),
    (2022, 'A', TAGS_2022A),
    (2022, 'B', TAGS_2022B),
    (2023, 'A', TAGS_2023A),
    (2023, 'B', TAGS_2023B),
]


def insert_all():
    with sqlite3.connect(DB_PATH) as conn:
        total = 0
        for year, version, tags in ALL:
            deleted = conn.execute(
                "DELETE FROM problems WHERE year = ? AND version = ?",
                (year, version)
            ).rowcount
            if deleted:
                print(f"  Removed {deleted} existing rows for {year}-{version}.")

            rows = [(year, version, qn, l1, l2, l3) for qn, l1, l2, l3 in tags]
            conn.executemany(
                "INSERT INTO problems (year, version, question_num, level_1, level_2, level_3) "
                "VALUES (?,?,?,?,?,?)",
                rows,
            )
            print(f"  Inserted {len(rows)} tag rows for {year} AMC 10{version}.")
            total += len(rows)

        conn.commit()
        print(f"\nDone. Total rows inserted: {total}")

        print("\n=== problems table: 2021-2023 summary ===")
        for row in conn.execute(
            "SELECT year, version, COUNT(*) FROM problems "
            "WHERE year BETWEEN 2021 AND 2023 "
            "GROUP BY year, version ORDER BY year, version"
        ):
            print(f"  {row[0]}  {row[1]}  {row[2]} tag rows")


if __name__ == "__main__":
    insert_all()
