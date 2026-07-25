import os
import random
import threading
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI(title="Health Check Service")

# Read environment variables for failure threshold range
fail_min = int(os.getenv("FAIL_MIN", "3"))
fail_max = int(os.getenv("FAIL_MAX", "7"))

total_request_counter = 0
cycle_request_counter = 0
counter_lock = threading.Lock()
server_name = os.getenv("SERVER_NAME", "default-server")


@app.get("/health")
def health_check(
    x_user_token: Annotated[str | None, Header()] = None,
):
    global total_request_counter, cycle_request_counter

    with counter_lock:
        total_request_counter += 1
        cycle_request_counter += 1

        total_count = total_request_counter
        current_count = cycle_request_counter

        # Generate target_failure_count on any request
        target_failure_count = random.randint(fail_min, fail_max)

        is_failure = current_count == target_failure_count
        if current_count >= fail_max:
            cycle_request_counter = 0

    return {
        "status": not is_failure,
        "total_request_count": total_count,
        "request_count": current_count,
        "server_name": server_name,
        "user_token": x_user_token,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
