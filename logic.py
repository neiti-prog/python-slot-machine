"""Game logic for the slot machine (no GUI code here, so it is easy to test)."""

import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

# How many of each symbol are in the pool (lower = rarer)
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

# Payout multiplier for a winning line (multiplied by the bet per line)
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}


def check_winnings(columns, lines, bet, values):
    """Return (total winnings, list of winning line numbers) for a spin.

    `columns` is a list of columns, each a list of symbols top to bottom.
    A line (row) wins when every column shows the same symbol on that row.
    """
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """Build a random spin: `cols` columns of `rows` symbols each.

    Symbols are drawn without replacement inside a column, so a column can
    never show more of a symbol than exists in the pool.
    """
    all_symbols = []
    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns


def theoretical_rtp(symbols=symbol_count, values=symbol_value, cols=COLS):
    """Exact return-to-player per line bet, worked out from the odds.

    Each column is drawn independently, and by symmetry any single cell shows
    symbol s with probability count(s) / total. A line therefore wins with
    symbol s with probability (count(s) / total) ** cols.
    """
    total = sum(symbols.values())
    return sum(((count / total) ** cols) * values[s] for s, count in symbols.items())