from __future__ import annotations

import cv2

from ocr_handler import OCRHandler


class BoardParser:
    @staticmethod
    def find_grid_bounds(image_path: str) -> tuple[int, int, int, int] | None:
        image = cv2.imread(image_path)
        if image is None:
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(blur, 80, 200)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        ratio = w / h if h else 0
        if not (0.7 < ratio < 1.3):
            return None

        return (x, y, w, h)

    @staticmethod
    def extract_grid_cells(x: int, y: int, w: int, h: int, rows: int = 6, cols: int = 5) -> list[tuple[int, int, int, int]]:
        cell_w = w // cols
        cell_h = h // rows
        cells = []

        for row in range(rows):
            for col in range(cols):
                cell_x = x + col * cell_w
                cell_y = y + row * cell_h
                cells.append((cell_x, cell_y, cell_w, cell_h))

        return cells

    @staticmethod
    def parse_board_image(image_path: str) -> dict:
        bounds = BoardParser.find_grid_bounds(image_path)
        if not bounds:
            raise ValueError("Could not detect a Wordle-like board in the image.")

        x, y, w, h = bounds
        cells = BoardParser.extract_grid_cells(x, y, w, h, rows=6, cols=5)
        board_data = OCRHandler.read_board_from_image(image_path, cells)
        board_data["bounds"] = bounds
        board_data["grid_cells"] = cells
        return board_data

    @staticmethod
    def board_to_guess_pattern(board_data: dict, row: int = 0) -> tuple[str, str] | None:
        start = row * 5
        end = start + 5

        letters = board_data["letters"][start:end]
        colors = board_data["colors"][start:end]
        guess = "".join([ch if ch != "?" else "X" for ch in letters])
        pattern = "".join(colors)

        if len(guess) < 5 or "X" in guess:
            return None
        return (guess, pattern)
