# Flappy Bird Clone

This project now includes:
- A browser version (`index.html`) using HTML5 Canvas + JavaScript
- A desktop version (`flappy_bird.py`) using Python + Pygame

## Requirements

- Python 3.10+ recommended
- `pygame` (installed from `requirements.txt`)

## Setup

1. Open a terminal in this folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run In Browser (Recommended)

Open `index.html` directly in your browser, or serve the folder locally:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Run Desktop Version (Pygame)

```bash
python flappy_bird.py
```

## Controls

- `SPACE`:
  - Start game from start screen
  - Make the bird jump while playing
  - Restart after game over
- Close window to quit.

## Gameplay

- Avoid pipes and the ground.
- Score increases by 1 each time you pass a pipe.

## Vercel Note

- Vercel deploys the browser game from `index.html` as a static site.
