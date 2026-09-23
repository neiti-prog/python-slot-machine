# Lucky Slots

A slot machine game for the desktop, built with Python and tkinter. Deposit some money, choose your lines and bet, and spin the animated reels. Your balance is saved between sessions. No external libraries needed.


## Features

- Animated reels that stop one at a time
- Bet on 1-3 lines, with bet sizes from $1 to $100 per line
- Winning lines are highlighted and the win amount is shown
- **Saved progress:** balance, best win, and total spins persist between sessions, so you can pick up where you left off
- Live balance, total bet, and stats
- Paytable generated from the payout values in the code
- Cash Out and game-over screens
- Keyboard shortcut: press `Space` or `Enter` to spin

## Getting started

You need Python 3.8 or newer. tkinter comes with the standard Python installers for Windows and macOS. On Linux you may need to install it (for example `sudo apt install python3-tk`).

```bash
git clone https://github.com/neiti-prog/python-slot-machine.git
cd YOUR-REPO-NAME
python slot_machine_gui.py
```

Progress is stored in a `save.json` file next to the game. Delete it to reset everything.

## How it works

Each spin fills a 3x3 grid, one column at a time, by randomly drawing symbols from a weighted pool:

| Symbol | Shown as | Appears in pool | Payout (x bet per line) |
|--------|----------|-----------------|-------------------------|
| A      | ★        | 2               | 5                       |
| B      | ♦        | 4               | 4                       |
| C      | ♠        | 6               | 3                       |
| D      | ♣        | 8               | 2                       |

Rarer symbols pay more. You choose how many rows (lines) to bet on. A line wins when all three symbols across that row match, and the payout is that symbol's multiplier times your bet per line.

The code is split so the game rules are separate from the interface:

- `logic.py` has the constants, `get_slot_machine_spin()` (builds the random columns), `check_winnings()` (finds winning lines and totals the payout), and `theoretical_rtp()` (works out the exact odds)
- `slot_machine_gui.py` is the tkinter interface and the save/load code

## Tests

The game logic has unit tests written with Python's built-in `unittest`. They cover winning and losing lines, multiple lines, partial matches, bet scaling, the shape and contents of a spin, and the RTP math.

```bash
python -m unittest -v
```

## Odds simulator

`simulate.py` plays a large number of spins and reports the return to player (RTP), how often a spin wins (hit rate), and the biggest win.

```bash
python simulate.py                  # 200,000 spins per line setting
python simulate.py --spins 1000000
```

It also prints the exact RTP calculated from the symbol odds, so you can check that the simulation agrees with the math. With the default payouts, players get back about 24.6% of the money they wager over time. To tune the game, change `symbol_count` and `symbol_value` in `logic.py` and re-run the simulator.

## Project structure

```
.
├── slot_machine_gui.py   # the game (tkinter interface, saved progress)
├── logic.py              # game rules and odds math
├── test_logic.py         # unit tests
├── simulate.py           # RTP simulator
├── screenshots/          # images used in this README
├── .gitignore
└── README.md
```

## Tweaking the game

- `symbol_count`, `symbol_value`, `MIN_BET`, `MAX_BET`, `MAX_LINES` in `logic.py`: odds, payouts, and betting limits
- `SYMBOL_STYLE` in `slot_machine_gui.py`: the glyph and color for each symbol
- Color constants (`BG`, `CARD`, `ACCENT`, etc.): the theme

## What I practiced

- Building a GUI with tkinter: layouts, custom widgets, event handling, and animation with `after()`
- Separating game logic from the interface so it can be tested
- Writing unit tests with `unittest`
- Reading and writing JSON to save progress, with handling for missing or corrupt files
- Checking a simulation against the underlying probability math
- Using Git and GitHub

## Ideas for the future

- Sound effects
- Wild and scatter symbols, diagonal paylines, and bonus rounds
- Autoplay
- Packaging as a standalone `.exe`