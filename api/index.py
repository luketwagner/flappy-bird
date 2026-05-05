"""
Minimal Vercel Python entrypoint.

This keeps Vercel import/deploy happy for this repository, which primarily
contains a desktop Pygame game (`flappy_bird.py`).
"""


def app(environ, start_response):
    """Simple WSGI app for Vercel's Python runtime."""
    status = "200 OK"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    body = (
        "Flappy Bird desktop game project.\n"
        "Run locally with: python flappy_bird.py\n"
    )
    return [body.encode("utf-8")]
