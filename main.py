"""
Root-level fallback Python entrypoint for Vercel detection.
"""


def app(environ, start_response):
    status = "200 OK"
    headers = [("Content-Type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return [b"Flappy Bird project is configured for Vercel Python runtime.\n"]
