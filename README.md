# Flappy Bird Clone (Pygame)

A complete Flappy Bird clone using Python and Pygame with start, playing, and game-over states.

## Requirements

- Python 3.10+ recommended
- `pygame` (installed from `requirements.txt`)

## Setup

1. Open a terminal in this folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

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

- This repository now includes `api/index.py` as a minimal Python entrypoint so Vercel can import/deploy it.
- It also includes `main.py` and `vercel.json` to make entrypoint detection explicit.
- The actual game is still a desktop Pygame app and should be played locally with `python flappy_bird.py`.
