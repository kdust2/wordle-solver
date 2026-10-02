# Word Game Solver

A universal solver for word games that can analyze board images or manual inputs and generate solutions for **any word puzzle**.

## Supported Game Types

- **Wordle** — 5-letter guessing with color feedback
- **Quordle** — 4 simultaneous Wordles
- **Waffle** — 5x5 grid word puzzle
- **Spelling Bee** — Center letter + 6 surrounding letters
- **Crossword** — Any grid-based word puzzle
- **Custom** — Define your own rules and board layout

## Features

✅ **Flexible Input Methods:**
- Screenshot/image upload (auto-detect board)
- Manual word entry
- Paste game board text
- Define custom constraints

✅ **Smart Solving:**
- Candidate filtering based on constraints
- Best-next-guess recommendation
- Multi-word solution support
- Constraint propagation (green, yellow, gray, etc.)

✅ **Universal Board Detection:**
- Auto-detect 5x5, 5x6, 6x6 grids
- Color extraction (green, yellow, gray)
- OCR for letter recognition
- Support for multiple board layouts

✅ **Game-Specific Rules:**
- Standard Wordle rules (G/Y/_ patterns)
- Spelling Bee constraints (center letter required)
- Waffle adjacency rules
- Custom constraint definitions

## Quick Start

### Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Solve Wordle from Guesses

```bash
python main.py --game wordle --history "SLATE:GY___" --history "CRANE:YY_YY"
```

### Solve from Screenshot

```bash
python main.py --game wordle --image screenshot.png
```

### Solve Spelling Bee

```bash
python main.py --game spelling-bee --center S --letters RTCALY
```

### Solve Waffle

```bash
python main.py --game waffle --image waffle-board.png
```

### Custom Game with Manual Constraints

```bash
python main.py --game custom \
  --must-contain "AEIOU" \
  --cannot-contain "XYZ" \
  --length 5 \
  --pattern "S____"
```

## Pattern Format

### Wordle / Standard

- `G` = Green (correct letter, correct position)
- `Y` = Yellow (correct letter, wrong position)
- `_` = Gray (letter not in word)

Example: `SLATE:GY___` means S is green, L is yellow, others are gray.

### Custom Patterns

- `*` = Any letter
- `[ABC]` = One of A, B, or C
- `[^XYZ]` = Any letter except X, Y, Z
- Position-based: `S*A**` means S at position 0, A at position 2

## Project Structure

```
wordle-solver/
├── main.py                 # CLI entry point
├── game_solver.py          # Universal solver engine
├── game_rules/
│   ├── wordle_rules.py     # Wordle-specific rules
│   ├── spelling_bee.py     # Spelling Bee solver
│   ├── waffle_rules.py     # Waffle-specific rules
│   └── custom_rules.py     # Custom constraint support
├── image_processor.py      # Screenshot parsing & OCR
├── wordlist.txt            # Standard dictionary
├── wordlist_extended.txt   # Extended word list
└── requirements.txt        # Dependencies
```

## Examples

### Example 1: Wordle with History

```bash
python main.py --game wordle \
  --history "SLATE:GY___" \
  --history "CRANE:YY_YY" \
  --history "STOKE:G_Y__"
```

Output:
```
Candidates remaining: 12
Best next guess: THEIR
```

### Example 2: Screenshot-Based Solver

```bash
python main.py --game wordle --image my-wordle.png --show-candidates
```

### Example 3: Spelling Bee

```bash
python main.py --game spelling-bee --center E --letters ARLTON
```

Output:
```
Possible words: LATER, LEARN, NEAR, RENT, TORN, etc.
Best score: ORIENTAL (8 letters)
```

### Example 4: Custom Game

```bash
python main.py --game custom \
  --must-contain "QU" \
  --length 6 \
  --pattern "[QU]****"
```

## How It Works

1. **Parse Input** — Accept screenshot, text, or manual constraints
2. **Detect Board** — Auto-identify grid type and layout from image
3. **Extract Letters** — Use OCR to read letters and colors
4. **Build Constraints** — Convert board state to filterable rules
5. **Filter Candidates** — Apply constraints to word list
6. **Rank Solutions** — Score by letter frequency or game-specific heuristics
7. **Return Answers** — Display best guesses or all valid words

## Roadmap

- [ ] Desktop GUI with drag-and-drop image support
- [ ] Webcam live capture for real-time solving
- [ ] More game types (Semantle, Wordle Unlimited, Connections)
- [ ] Advanced OCR with color detection
- [ ] Win/Mac/Linux executable packaging
- [ ] Mobile app (React Native / Flutter)
- [ ] Browser extension for inline solving

## Notes

This is a working MVP designed to be lightweight, extensible, and easy to run locally. The image-based detection works best with high-contrast, well-lit board screenshots. For maximum accuracy, combine screenshot input with manual constraint refinement.

## License

MIT

