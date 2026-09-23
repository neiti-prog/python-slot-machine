import random
import tkinter as tk

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

# How each symbol looks on screen: (glyph, color)
SYMBOL_STYLE = {
    "A": ("★", "#facc15"),
    "B": ("♦", "#f472b6"),
    "C": ("♠", "#60a5fa"),
    "D": ("♣", "#4ade80"),
}

BET_CHIPS = [b for b in (1, 5, 10, 25, 50, 100) if MIN_BET <= b <= MAX_BET]

# Colors
BG = "#1e1b4b"
CARD = "#2b2766"
CELL_BG = "#15123a"
WIN_BG = "#713f12"
ACCENT = "#8b5cf6"
ACCENT_HOVER = "#a78bfa"
TEXT = "#f5f3ff"
MUTED = "#a5a0d6"
GOLD = "#facc15"
GREEN = "#4ade80"
RED = "#f87171"

FONT = "Helvetica"


# ---------- game logic (same as the terminal version) ----------
def check_winnings(columns, lines, bet, values):
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


# ---------- GUI ----------
class SlotApp:
    def __init__(self, root):
        self.root = root
        self.screen = "deposit"
        self.spinning = False

        root.title("Lucky Slots")
        root.geometry("560x780")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.container = tk.Frame(root, bg=BG)
        self.container.pack(fill="both", expand=True, padx=32, pady=24)

        root.bind("<Key>", self.on_key)
        self.show_deposit()

    # ---------- helpers ----------
    def clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, color=ACCENT, hover=ACCENT_HOVER):
        # Label-based button so colors work the same on Windows, macOS and Linux
        btn = tk.Label(
            parent, text=text, font=(FONT, 14, "bold"),
            bg=color, fg="white", padx=24, pady=10, cursor="hand2",
        )
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: (not self.spinning) and btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: (not self.spinning) and btn.config(bg=color))
        return btn

    def make_chip(self, parent, text, command):
        chip = tk.Label(
            parent, text=text, font=(FONT, 12, "bold"),
            bg=CARD, fg=TEXT, padx=12, pady=6, cursor="hand2",
        )
        chip.bind("<Button-1>", lambda e: command())
        return chip

    def on_key(self, event):
        if self.screen == "game" and event.keysym in ("space", "Return"):
            self.spin()

    # ---------- deposit screen ----------
    def show_deposit(self, message="", message_color=MUTED):
        self.screen = "deposit"
        self.spinning = False
        self.clear()

        tk.Label(
            self.container, text="★  ♦  ♠  ♣", font=(FONT, 26, "bold"),
            bg=BG, fg=ACCENT_HOVER,
        ).pack(pady=(50, 0))
        tk.Label(
            self.container, text="LUCKY SLOTS", font=(FONT, 34, "bold"),
            bg=BG, fg=GOLD,
        ).pack(pady=(8, 4))
        tk.Label(
            self.container, text="Match 3 in a row to win.\nHow much would you like to deposit?",
            font=(FONT, 13), bg=BG, fg=MUTED, justify="center",
        ).pack(pady=(0, 24))

        self.deposit_var = tk.StringVar(value="100")
        entry = tk.Entry(
            self.container, textvariable=self.deposit_var, font=(FONT, 20, "bold"),
            bg="white", fg="#1e1b4b", relief="flat", justify="center",
            insertbackground="#1e1b4b", width=10,
        )
        entry.pack(ipady=8)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self.start_game())

        quick = tk.Frame(self.container, bg=BG)
        quick.pack(pady=14)
        for amount in (50, 100, 500):
            self.make_chip(quick, f"${amount}", lambda a=amount: self.deposit_var.set(str(a))).pack(side="left", padx=4)

        self.deposit_msg = tk.Label(
            self.container, text=message, font=(FONT, 12, "bold"),
            bg=BG, fg=message_color, wraplength=440, height=2,
        )
        self.deposit_msg.pack()

        self.make_button(self.container, "Start Playing", self.start_game).pack(pady=(6, 0))

    def start_game(self):
        text = self.deposit_var.get().strip()
        if not text.isdigit():
            self.deposit_msg.config(text="Please enter a number.", fg=RED)
            return
        amount = int(text)
        if amount <= 0:
            self.deposit_msg.config(text="Amount must be greater than 0!", fg=RED)
            return

        self.balance = amount
        self.spins = 0
        self.biggest_win = 0
        self.lines = 1
        self.bet = 5 if 5 in BET_CHIPS else BET_CHIPS[0]
        self.show_game()

    # ---------- game screen ----------
    def show_game(self):
        self.screen = "game"
        self.clear()

        # Top bar: balance + last win
        top = tk.Frame(self.container, bg=BG)
        top.pack(fill="x")

        left = tk.Frame(top, bg=BG)
        left.pack(side="left")
        tk.Label(left, text="BALANCE", font=(FONT, 10, "bold"), bg=BG, fg=MUTED).pack(anchor="w")
        self.balance_label = tk.Label(left, text=f"${self.balance}", font=(FONT, 30, "bold"), bg=BG, fg=GOLD)
        self.balance_label.pack(anchor="w")

        right = tk.Frame(top, bg=BG)
        right.pack(side="right")
        tk.Label(right, text="LAST WIN", font=(FONT, 10, "bold"), bg=BG, fg=MUTED).pack(anchor="e")
        self.win_label = tk.Label(right, text="$0", font=(FONT, 30, "bold"), bg=BG, fg=TEXT)
        self.win_label.pack(anchor="e")

        # Reels
        machine = tk.Frame(self.container, bg=CARD, padx=14, pady=14)
        machine.pack(pady=(18, 0))
        self.indicators = []
        self.cells = []
        for row in range(ROWS):
            ind = tk.Label(machine, text=str(row + 1), font=(FONT, 12, "bold"), width=2, bg=CARD, fg=MUTED)
            ind.grid(row=row, column=0, padx=(0, 8))
            self.indicators.append(ind)

            cell_row = []
            for col in range(COLS):
                cell = tk.Label(machine, text="", font=(FONT, 36, "bold"), width=3, pady=8, bg=CELL_BG)
                cell.grid(row=row, column=col + 1, padx=4, pady=4)
                cell_row.append(cell)
            self.cells.append(cell_row)

        self.show_columns(get_slot_machine_spin(ROWS, COLS, symbol_count))

        # Lines selector
        lines_row = tk.Frame(self.container, bg=BG)
        lines_row.pack(fill="x", pady=(18, 0))
        tk.Label(lines_row, text="LINES", font=(FONT, 10, "bold"), bg=BG, fg=MUTED, width=10, anchor="w").pack(side="left")
        self.line_chips = {}
        for n in range(1, MAX_LINES + 1):
            chip = self.make_chip(lines_row, str(n), lambda n=n: self.set_lines(n))
            chip.pack(side="left", padx=3)
            self.line_chips[n] = chip

        # Bet-per-line selector
        bet_row = tk.Frame(self.container, bg=BG)
        bet_row.pack(fill="x", pady=(10, 0))
        tk.Label(bet_row, text="BET / LINE", font=(FONT, 10, "bold"), bg=BG, fg=MUTED, width=10, anchor="w").pack(side="left")
        self.bet_chips = {}
        for amount in BET_CHIPS:
            chip = self.make_chip(bet_row, f"${amount}", lambda a=amount: self.set_bet(a))
            chip.pack(side="left", padx=3)
            self.bet_chips[amount] = chip

        self.total_label = tk.Label(self.container, text="", font=(FONT, 13, "bold"), bg=BG, fg=TEXT)
        self.total_label.pack(pady=(12, 0))

        # Spin button
        self.spin_btn = self.make_button(self.container, "SPIN", self.spin)
        self.spin_btn.config(font=(FONT, 18, "bold"), pady=14)
        self.spin_btn.pack(fill="x", pady=(12, 0))

        # Message
        self.message = tk.Label(
            self.container, text="Press SPIN or hit Space.", font=(FONT, 13, "bold"),
            bg=BG, fg=MUTED, wraplength=470, height=2,
        )
        self.message.pack(pady=(8, 0))

        # Paytable (built from symbol_value)
        pay = tk.Frame(self.container, bg=BG)
        pay.pack(pady=(4, 0))
        tk.Label(pay, text="PAYS:", font=(FONT, 10, "bold"), bg=BG, fg=MUTED).pack(side="left", padx=(0, 8))
        for symbol, value in symbol_value.items():
            glyph, color = SYMBOL_STYLE[symbol]
            tk.Label(pay, text=f"{glyph} x{value}", font=(FONT, 13, "bold"), bg=BG, fg=color).pack(side="left", padx=8)

        # Footer: stats + cash out
        footer = tk.Frame(self.container, bg=BG)
        footer.pack(fill="x", side="bottom")
        self.stats_label = tk.Label(footer, text="", font=(FONT, 11), bg=BG, fg=MUTED)
        self.stats_label.pack(side="left")
        cash = self.make_button(footer, "Cash Out", self.cash_out, color="#4b4785", hover="#5f5aa0")
        cash.config(font=(FONT, 11, "bold"), padx=14, pady=6)
        cash.pack(side="right")

        self.refresh_controls()
        self.refresh_stats()

    # ---------- display helpers ----------
    def set_cell(self, row, col, symbol, highlight=False):
        glyph, color = SYMBOL_STYLE[symbol]
        self.cells[row][col].config(text=glyph, fg=color, bg=WIN_BG if highlight else CELL_BG)

    def show_columns(self, columns):
        for col, column in enumerate(columns):
            for row, symbol in enumerate(column):
                self.set_cell(row, col, symbol)

    def set_message(self, text, color=MUTED):
        self.message.config(text=text, fg=color)

    def refresh_controls(self):
        for n, chip in self.line_chips.items():
            chip.config(bg=ACCENT if n == self.lines else CARD)
        for amount, chip in self.bet_chips.items():
            chip.config(bg=ACCENT if amount == self.bet else CARD)
        for row, ind in enumerate(self.indicators):
            active = row < self.lines
            ind.config(fg=GOLD if active else MUTED, text="▶" if active else str(row + 1))
        total = self.lines * self.bet
        self.total_label.config(
            text=f"Total bet: ${total}",
            fg=RED if total > self.balance else TEXT,
        )

    def refresh_stats(self):
        self.stats_label.config(text=f"Spins: {self.spins}   Biggest win: ${self.biggest_win}")
        self.balance_label.config(text=f"${self.balance}")

    def set_lines(self, n):
        if self.spinning:
            return
        self.lines = n
        self.refresh_controls()

    def set_bet(self, amount):
        if self.spinning:
            return
        self.bet = amount
        self.refresh_controls()

    # ---------- spinning ----------
    def spin(self):
        if self.spinning:
            return

        total_bet = self.lines * self.bet
        if total_bet > self.balance:
            self.set_message(
                f"Not enough balance for that bet. You have ${self.balance}.", RED
            )
            return

        self.spinning = True
        self.balance -= total_bet
        self.spins += 1
        self.refresh_stats()
        self.set_message("Spinning...", MUTED)
        self.spin_btn.config(text="SPINNING...", bg="#4b4785")

        self.result = get_slot_machine_spin(ROWS, COLS, symbol_count)
        self.stop_ticks = [10, 17, 24]  # reels stop one after another
        self.tick = 0
        self.animate()

    def animate(self):
        symbols = list(SYMBOL_STYLE)
        for col in range(COLS):
            if self.tick < self.stop_ticks[col]:
                for row in range(ROWS):
                    self.set_cell(row, col, random.choice(symbols))
            elif self.tick == self.stop_ticks[col]:
                for row in range(ROWS):
                    self.set_cell(row, col, self.result[col][row])

        self.tick += 1
        if self.tick <= self.stop_ticks[-1]:
            self.root.after(70, self.animate)
        else:
            self.finish_spin()

    def finish_spin(self):
        winnings, winning_lines = check_winnings(self.result, self.lines, self.bet, symbol_value)
        self.balance += winnings
        self.biggest_win = max(self.biggest_win, winnings)

        # Highlight winning rows
        for line in winning_lines:
            row = line - 1
            for col in range(COLS):
                self.set_cell(row, col, self.result[col][row], highlight=True)

        if winnings > 0:
            lines_text = ", ".join(str(n) for n in winning_lines)
            self.set_message(f"You won ${winnings} on line {lines_text}!", GREEN)
            self.win_label.config(text=f"${winnings}", fg=GREEN)
        else:
            self.set_message("No win this time. Try again!", MUTED)
            self.win_label.config(text="$0", fg=TEXT)

        self.spinning = False
        self.spin_btn.config(text="SPIN", bg=ACCENT)
        self.refresh_stats()
        self.refresh_controls()

        if self.balance < MIN_BET:
            self.spinning = True  # lock the machine while the message is shown
            self.root.after(
                1800,
                lambda: self.show_deposit("You ran out of money! Deposit again to keep playing.", RED),
            )

    def cash_out(self):
        if self.spinning:
            return
        self.show_deposit(f"You cashed out with ${self.balance}. Thanks for playing!", GREEN)


if __name__ == "__main__":
    root = tk.Tk()
    SlotApp(root)
    root.mainloop()