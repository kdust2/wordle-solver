from __future__ import annotations

import cv2
import numpy as np


class OCRHandler:
    """Simple OCR-like extraction for a grid of Wordle cells."""

    @staticmethod
    def extract_cell_letter(cell_image: np.ndarray) -> str | None:
        if cell_image is None or cell_image.size == 0:
            return None

        gray = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY) if len(cell_image.shape) == 3 else cell_image
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        if w < 5 or h < 5:
            return None

        roi = gray[y : y + h, x : x + w]
        variance = float(np.var(roi))
        if variance < 20:
            return None

        return "?"

    @staticmethod
    def detect_cell_color(cell_image: np.ndarray) -> str:
        if cell_image is None or cell_image.size == 0:
            return "_"

        hsv = cv2.cvtColor(cell_image, cv2.COLOR_BGR2HSV) if len(cell_image.shape) == 3 else cell_image
        green_mask = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([90, 255, 255]))
        yellow_mask = cv2.inRange(hsv, np.array([15, 50, 50]), np.array([35, 255, 255]))
        gray_mask = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([180, 50, 200]))

        green_count = cv2.countNonZero(green_mask)
        yellow_count = cv2.countNonZero(yellow_mask)
        gray_count = cv2.countNonZero(gray_mask)

        if green_count > yellow_count and green_count > gray_count:
            return "G"
        if yellow_count > gray_count:
            return "Y"
        return "_"

    @staticmethod
    def read_board_from_image(image_path: str, grid_cells: list[tuple[int, int, int, int]]) -> dict:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        letters = []
        colors = []

        for x, y, w, h in grid_cells:
            cell = image[y : y + h, x : x + w]
            letter = OCRHandler.extract_cell_letter(cell) or "?"
            color = OCRHandler.detect_cell_color(cell)
            letters.append(letter)
            colors.append(color)

        return {"letters": letters, "colors": colors}
