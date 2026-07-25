import os
import threading
from typing import Annotated

from fastapi import FastAPI, Header, Response, status

app = FastAPI(title="Health Check Service")

request_counter = 0
counter_lock = threading.Lock()
server_name = os.getenv("SERVER_NAME", "default-server")


@app.get("/health")
def health_check(
    response: Response,
    x_user_token: Annotated[str | None, Header()] = None,
):
    global request_counter
    with counter_lock:
        request_counter += 1
        current_count = request_counter

    # Every 5th request returns status False and HTTP 500
    if current_count % 5 == 0:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": False,
            "request_count": current_count,
            "server_name": server_name,
            "user_token": x_user_token,
        }

    return {
        "status": True,
        "request_count": current_count,
        "server_name": server_name,
        "user_token": x_user_token,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
