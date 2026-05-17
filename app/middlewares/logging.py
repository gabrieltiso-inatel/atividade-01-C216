from fastapi import Request
import time


async def log_requests(request: Request, call_next):
    start = time.time()

    print(f"➡️ {request.method} {request.url}")

    response = await call_next(request)

    duration = time.time() - start
    print(f"⬅️ {response.status_code} - {duration:.4f}s")

    return response
