from __future__ import annotations

import cv2
import numpy as np


def detect_wordle_grid(image_path: str) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No board-like contours found in the image. Try a clearer screenshot.")

    board = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(board)

    if w < 80 or h < 80:
        raise ValueError("Detected a board region that is too small.")

    cell_w = w / 5
    cell_h = h / 6
    cells: list[tuple[int, int, int, int]] = []
    for row in range(6):
        for col in range(5):
            cells.append((int(x + col * cell_w), int(y + row * cell_h), int(cell_w), int(cell_h)))

    return image, cells


def summarize_board_image(image_path: str) -> dict:
    image, cells = detect_wordle_grid(image_path)
    return {
        "width": int(image.shape[1]),
        "height": int(image.shape[0]),
        "estimated_cells": len(cells),
        "message": "A Wordle-like board region was detected. This is a best-effort pass; for best accuracy, provide a clear screenshot or manual board input.",
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_processor.py path/to/board-image.png")
        raise SystemExit(1)

    try:
        print(summarize_board_image(sys.argv[1]))
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)
