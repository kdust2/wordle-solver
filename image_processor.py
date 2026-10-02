from __future__ import annotations

import os
from collections import Counter
from typing import Sequence


class GenericWordSolver:
    def __init__(self, wordlist_path: str | None = None):
        if wordlist_path is None:
            wordlist_path = os.path.join(os.path.dirname(__file__), "wordlist.txt")

        with open(wordlist_path, "r", encoding="utf-8") as handle:
            self.words = [line.strip().upper() for line in handle if line.strip() and line.strip().isalpha()]

    def filter_words(self, length: int = 5, must_contain: str = "", cannot_contain: str = "", pattern: str = "") -> list[str]:
        must_contain = must_contain.upper()
        cannot_contain = cannot_contain.upper()
        pattern = pattern.upper()

        filtered = []
        for word in self.words:
            if len(word) != length:
                continue
            if must_contain and any(ch not in word for ch in set(must_contain)):
                continue
            if cannot_contain and any(ch in word for ch in set(cannot_contain)):
                continue
            if pattern and not self._matches_pattern(word, pattern):
                continue
            filtered.append(word)

        return filtered

    @staticmethod
    def _matches_pattern(word: str, pattern: str) -> bool:
        pattern = pattern.upper()
        if len(pattern) != len(word):
            return False

        for idx, ch in enumerate(pattern):
            if ch == "*":
                continue
            if ch == "?":
                continue
            if ch == "[":
                end = pattern.find("]", idx)
                if end == -1:
                    return False
                options = pattern[idx + 1 : end]
                if word[idx] not in options:
                    return False
                continue
            if ch != word[idx]:
                return False
        return True

    @staticmethod
    def recommend_guess(candidates: Sequence[str]) -> str:
        if not candidates:
            raise ValueError("No candidates to rank.")
        if len(candidates) == 1:
            return candidates[0]

        letter_counts = Counter(ch for word in candidates for ch in word)
        ranked = sorted(candidates, key=lambda word: (-sum(letter_counts[ch] for ch in set(word)), word))
        return ranked[0]


if __name__ == "__main__":
    solver = GenericWordSolver()
    matches = solver.filter_words(length=5, must_contain="A", pattern="*A***")
    print(matches[:10])
    print("Best guess:", solver.recommend_guess(matches))
