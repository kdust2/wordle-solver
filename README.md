from __future__ import annotations

import argparse
import os

from game_solver import GenericWordSolver
from image_processor import summarize_board_image
from wordle_solver import WordleSolver


def parse_history(raw_history: list[str]) -> list[tuple[str, str]]:
    history: list[tuple[str, str]] = []
    for item in raw_history:
        if ":" not in item:
            raise ValueError(f"Each history value must be in the form GUESS:PATTERN; got: {item}")
        guess, pattern = item.split(":", 1)
        guess = guess.strip().upper()
        pattern = pattern.strip().upper()
        if len(guess) != 5 or len(pattern) != 5:
            raise ValueError(f"Guess and pattern must both be 5 letters long: {guess!r} {pattern!r}")
        history.append((guess, pattern))
    return history


def solve_wordle(history: list[str]) -> str:
    solver = WordleSolver()
    data = parse_history(history)
    candidates = solver.filter_candidates(data)
    best = solver.recommend_guess(data)
    text = f"Remaining candidates: {len(candidates)}\nBest next guess: {best}\n"
    if len(candidates) <= 20:
        text += f"Candidates: {candidates}\n"
    return text


def solve_custom(length: int, must_contain: str, cannot_contain: str, pattern: str) -> str:
    solver = GenericWordSolver()
    filtered = solver.filter_words(
        length=length,
        must_contain=must_contain.upper(),
        cannot_contain=cannot_contain.upper(),
        pattern=pattern.upper(),
    )
    if not filtered:
        return "No candidates match your rules."
    best = solver.recommend_guess(filtered)
    return f"Candidates found: {len(filtered)}\nBest guess: {best}\nSample: {filtered[:15]}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Universal word game solver")
    parser.add_argument("--game", choices=["wordle", "custom"], default="wordle")
    parser.add_argument("--history", action="append", default=[], help="Entry in GUESS:PATTERN form")
    parser.add_argument("--image", help="Optional screenshot")
    parser.add_argument("--must-contain", default="")
    parser.add_argument("--cannot-contain", default="")
    parser.add_argument("--pattern", default="")
    parser.add_argument("--length", type=int, default=5)
    parser.add_argument("--gui", action="store_true", help="Launch the GUI")
    args = parser.parse_args()

    if args.gui:
        try:
            from gui import WordGameSolverGUI

            app = WordGameSolverGUI()
            app.mainloop()
        except ImportError:
            print("GUI dependencies not available. Install Tkinter or run in CLI mode.")
            return

    if args.game == "wordle":
        if not args.history:
            print("No Wordle history provided. Use --history SLATE:GY___ ...")
            return
        output = solve_wordle(args.history)
        if args.image:
            try:
                output = f"Image detection: {summarize_board_image(args.image)}\n\n{output}"
            except Exception as exc:
                output = f"Image detection failed: {exc}\n\n{output}"
        print(output)
        return

    print(solve_custom(args.length, args.must_contain, args.cannot_contain, args.pattern))


if __name__ == "__main__":
    main()
