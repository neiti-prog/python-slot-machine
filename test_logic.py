import unittest
from collections import Counter

from logic import (
    COLS,
    ROWS,
    check_winnings,
    get_slot_machine_spin,
    symbol_count,
    symbol_value,
    theoretical_rtp,
)

VALUES = {"A": 5, "B": 4, "C": 3, "D": 2}


class CheckWinningsTests(unittest.TestCase):
    def test_single_winning_line_pays_symbol_value_times_bet(self):
        # Row 1 is A A A
        columns = [["A", "B", "C"] for _ in range(3)]
        winnings, lines = check_winnings(columns, lines=1, bet=10, values=VALUES)
        self.assertEqual(winnings, 5 * 10)
        self.assertEqual(lines, [1])

    def test_multiple_winning_lines_add_up(self):
        # Row 1 = A A A, row 2 = B B B, row 3 = C C C
        columns = [["A", "B", "C"] for _ in range(3)]
        winnings, lines = check_winnings(columns, lines=3, bet=2, values=VALUES)
        self.assertEqual(winnings, (5 + 4 + 3) * 2)
        self.assertEqual(lines, [1, 2, 3])

    def test_no_matching_lines_pays_nothing(self):
        columns = [["A", "B", "C"], ["B", "C", "A"], ["C", "A", "B"]]
        winnings, lines = check_winnings(columns, lines=3, bet=5, values=VALUES)
        self.assertEqual(winnings, 0)
        self.assertEqual(lines, [])

    def test_two_of_three_matching_does_not_win(self):
        # Row 1 is A A D (no win), rows 2 and 3 still match
        columns = [["A", "B", "C"], ["A", "B", "C"], ["D", "B", "C"]]
        winnings, lines = check_winnings(columns, lines=1, bet=1, values=VALUES)
        self.assertEqual(winnings, 0)
        self.assertEqual(lines, [])

        winnings, lines = check_winnings(columns, lines=3, bet=1, values=VALUES)
        self.assertEqual(winnings, 4 + 3)
        self.assertEqual(lines, [2, 3])

    def test_only_lines_you_bet_on_can_win(self):
        # Every row matches, but we only bet on the first line
        columns = [["A", "B", "C"] for _ in range(3)]
        winnings, lines = check_winnings(columns, lines=1, bet=4, values=VALUES)
        self.assertEqual(winnings, 5 * 4)
        self.assertEqual(lines, [1])

    def test_winnings_scale_linearly_with_bet(self):
        columns = [["D", "D", "D"] for _ in range(3)]
        small, _ = check_winnings(columns, lines=1, bet=1, values=VALUES)
        large, _ = check_winnings(columns, lines=1, bet=7, values=VALUES)
        self.assertEqual(large, small * 7)

    def test_uses_the_values_it_is_given(self):
        columns = [["A", "B", "C"] for _ in range(3)]
        custom = {"A": 100, "B": 1, "C": 1, "D": 1}
        winnings, _ = check_winnings(columns, lines=1, bet=1, values=custom)
        self.assertEqual(winnings, 100)


class SpinTests(unittest.TestCase):
    def test_spin_has_the_right_shape(self):
        columns = get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.assertEqual(len(columns), COLS)
        for column in columns:
            self.assertEqual(len(column), ROWS)

    def test_custom_dimensions(self):
        columns = get_slot_machine_spin(2, 4, symbol_count)
        self.assertEqual(len(columns), 4)
        self.assertTrue(all(len(column) == 2 for column in columns))

    def test_only_known_symbols_appear(self):
        for _ in range(100):
            for column in get_slot_machine_spin(ROWS, COLS, symbol_count):
                for symbol in column:
                    self.assertIn(symbol, symbol_count)

    def test_column_never_uses_more_of_a_symbol_than_exists(self):
        # Symbols are drawn without replacement inside each column
        for _ in range(300):
            for column in get_slot_machine_spin(ROWS, COLS, symbol_count):
                for symbol, used in Counter(column).items():
                    self.assertLessEqual(used, symbol_count[symbol])

    def test_pool_equal_to_rows_gives_every_symbol_once_per_column(self):
        pool = {"A": 1, "B": 1, "C": 1}
        for _ in range(50):
            for column in get_slot_machine_spin(3, 3, pool):
                self.assertEqual(sorted(column), ["A", "B", "C"])


class TheoreticalRtpTests(unittest.TestCase):
    def test_single_symbol_always_wins(self):
        self.assertAlmostEqual(theoretical_rtp({"A": 1}, {"A": 3}, cols=3), 3.0)

    def test_two_equal_symbols(self):
        # Each symbol wins a line with probability (1/2)^3 = 1/8
        rtp = theoretical_rtp({"A": 1, "B": 1}, {"A": 8, "B": 8}, cols=3)
        self.assertAlmostEqual(rtp, 2 * (1 / 8) * 8)

    def test_default_game_math(self):
        # (0.1^3 * 5) + (0.2^3 * 4) + (0.3^3 * 3) + (0.4^3 * 2) = 0.246
        self.assertAlmostEqual(theoretical_rtp(symbol_count, symbol_value), 0.246)


if __name__ == "__main__":
    unittest.main()