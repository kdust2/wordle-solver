from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from board_parser import BoardParser
from game_solver import GenericWordSolver
from image_processor import summarize_board_image
from wordle_solver import WordleSolver


class WordGameSolverGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Word Game Solver")
        self.geometry("1200x800")
        self.minsize(1000, 650)
        self.configure(bg="#f3f5f7")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f5f7")
        style.configure("TLabel", background="#f3f5f7", foreground="#222")
        style.configure("Header.TLabel", background="#f3f5f7", foreground="#111", font=("Helvetica", 15, "bold"))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"))

        self.game_var = tk.StringVar(value="wordle")
        self.image_path = tk.StringVar()
        self.must_contain = tk.StringVar()
        self.cannot_contain = tk.StringVar()
        self.pattern = tk.StringVar()
        self.length = tk.IntVar(value=5)
        self.board_data = None

        self.create_widgets()

    def create_widgets(self) -> None:
        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        header = ttk.Label(main, text="Word Game Solver", style="Header.TLabel")
        header.pack(fill="x", pady=(0, 20))

        controls = ttk.Frame(main)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Label(controls, text="Game type:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        game_combo = ttk.Combobox(controls, textvariable=self.game_var, values=["wordle", "custom"], state="readonly", width=18)
        game_combo.grid(row=0, column=1, sticky="w", padx=(0, 30))
        game_combo.bind("<<ComboboxSelected>>", lambda _e: self.update_mode())

        ttk.Label(controls, text="Screenshot:").grid(row=0, column=2, sticky="w", padx=(0, 10))
        image_entry = ttk.Entry(controls, textvariable=self.image_path, width=52)
        image_entry.grid(row=0, column=3, sticky="ew", padx=(0, 10))
        ttk.Button(controls, text="Browse", command=self.pick_image).grid(row=0, column=4, sticky="e", padx=(0, 8))
        ttk.Button(controls, text="Parse board", command=self.parse_board).grid(row=0, column=5, sticky="e")

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True, pady=(10, 0))

        left = ttk.Frame(content)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        ttk.Label(left, text="Wordle history (GUESS:PATTERN)", font=("Helvetica", 11, "bold")).pack(fill="x", pady=(0, 8))
        self.history_box = tk.Text(left, height=14, width=55, font=("Courier New", 10), wrap="word")
        self.history_box.pack(fill="both", expand=True)
        self.history_box.insert("end", "SLATE:GY___\nCRANE:YY___\n")

        right = ttk.Frame(content)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(right, text="Custom solver options", font=("Helvetica", 11, "bold")).pack(fill="x", pady=(0, 12))

        row1 = ttk.Frame(right)
        row1.pack(fill="x", pady=(0, 10))
        ttk.Label(row1, text="Must contain:", width=14).pack(side="left")
        ttk.Entry(row1, textvariable=self.must_contain, width=30).pack(side="left", fill="x", expand=True)

        row2 = ttk.Frame(right)
        row2.pack(fill="x", pady=(0, 10))
        ttk.Label(row2, text="Cannot contain:", width=14).pack(side="left")
        ttk.Entry(row2, textvariable=self.cannot_contain, width=30).pack(side="left", fill="x", expand=True)

        row3 = ttk.Frame(right)
        row3.pack(fill="x", pady=(0, 10))
        ttk.Label(row3, text="Pattern:", width=14).pack(side="left")
        ttk.Entry(row3, textvariable=self.pattern, width=30).pack(side="left", fill="x", expand=True)

        row4 = ttk.Frame(right)
        row4.pack(fill="x", pady=(0, 10))
        ttk.Label(row4, text="Length:", width=14).pack(side="left")
        ttk.Spinbox(row4, from_=3, to_=12, textvariable=self.length, width=12).pack(side="left")

        help_text = "Pattern: use * for any, [AEI] for choice\nExample: S*A** or [AEI]****"
        ttk.Label(right, text=help_text, justify="left", foreground="#555", font=("Helvetica", 9)).pack(fill="x", pady=(12, 0))

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(15, 10))
        ttk.Button(buttons, text="Solve", command=self.solve, style="Accent.TButton").pack(side="left", padx=(0, 12))
        ttk.Button(buttons, text="Clear results", command=self.clear_output).pack(side="left")

        ttk.Label(main, text="Results", font=("Helvetica", 11, "bold")).pack(fill="x", pady=(8, 8))
        self.output = tk.Text(main, height=14, width=100, wrap="word", font=("Courier New", 10))
        self.output.pack(fill="both", expand=True)
        self.output.config(state="disabled")

        self.update_mode()

    def update_mode(self) -> None:
        if self.game_var.get() == "wordle":
            self.history_box.config(state="normal")
        else:
            self.history_box.config(state="disabled")

    def pick_image(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")])
        if path:
            self.image_path.set(path)

    def parse_board(self) -> None:
        if not self.image_path.get():
            messagebox.showwarning("Missing file", "Please select an image first.")
            return

        try:
            self.board_data = BoardParser.parse_board_image(self.image_path.get())
            self.display_output(
                f"Board parsed successfully!\n"
                f"Grid detected at: {self.board_data['bounds']}\n"
                f"Cells extracted: {len(self.board_data['grid_cells'])}\n\n"
                f"Letters detected: {self.board_data['letters']}\n"
                f"Colors detected: {self.board_data['colors']}\n\n"
                f"Note: OCR is basic and may need manual cleanup."
            )
        except Exception as exc:
            messagebox.showerror("Board parsing failed", str(exc))

    def clear_output(self) -> None:
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    def solve(self) -> None:
        try:
            if self.game_var.get() == "wordle":
                self.solve_wordle()
            else:
                self.solve_custom()
        except Exception as exc:
            messagebox.showerror("Solver error", str(exc))

    def solve_wordle(self) -> None:
        history_lines = [line.strip() for line in self.history_box.get("1.0", "end").splitlines() if line.strip()]
        if not history_lines:
            messagebox.showwarning("Missing input", "Please enter at least one Wordle guess.")
            return

        try:
            history = self.parse_history(history_lines)
        except ValueError as exc:
            messagebox.showerror("Input error", str(exc))
            return

        solver = WordleSolver()
        candidates = solver.filter_candidates(history)
        best = solver.recommend_guess(history)

        output = f"Remaining candidates: {len(candidates)}\nBest next guess: {best}\n"
        if len(candidates) <= 25:
            output += f"Candidates:\n{', '.join(candidates)}\n"
        else:
            output += f"Top candidates:\n{', '.join(candidates[:25])}\n"

        if self.image_path.get():
            try:
                summary = summarize_board_image(self.image_path.get())
                output = f"Screenshot analysis:\n{summary}\n\n{output}"
            except Exception as exc:
                output = f"Screenshot analysis failed: {exc}\n\n{output}"

        self.display_output(output)

    def solve_custom(self) -> None:
        solver = GenericWordSolver()
        filtered = solver.filter_words(
            length=int(self.length.get()),
            must_contain=self.must_contain.get().upper(),
            cannot_contain=self.cannot_contain.get().upper(),
            pattern=self.pattern.get().upper(),
        )
        if not filtered:
            self.display_output("No words match your rules.")
            return

        best = solver.recommend_guess(filtered)
        output = f"Candidates found: {len(filtered)}\nBest guess: {best}\n"
        if len(filtered) <= 25:
            output += f"Matches:\n{', '.join(filtered)}\n"
        else:
            output += f"Top matches:\n{', '.join(filtered[:25])}\n"
        self.display_output(output)

    @staticmethod
    def parse_history(raw_history: list[str]) -> list[tuple[str, str]]:
        history: list[tuple[str, str]] = []
        for item in raw_history:
            if ":" not in item:
                raise ValueError(f"Invalid format: {item}. Use GUESS:PATTERN (e.g. SLATE:GY___)")
            guess, pattern = item.split(":", 1)
            guess = guess.strip().upper()
            pattern = pattern.strip().upper()
            if len(guess) != 5 or len(pattern) != 5:
                raise ValueError(f"Guess and pattern must both be 5 characters long: {guess!r} / {pattern!r}")
            history.append((guess, pattern))
        return history

    def display_output(self, text: str) -> None:
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.config(state="disabled")


if __name__ == "__main__":
    app = WordGameSolverGUI()
    app.mainloop()
