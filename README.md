# Python Nginx Loadbalancer - Health Check Service

A simple FastAPI health check service built with `uv`, packaged with Docker, and load-balanced via NGINX with custom header forwarding and randomized failure targets.

## Directory Structure

- `python/`: Python application directory.
  - [python/main.py](file:///Users/ernstvorsteveld/git/python/python-nginx-loadbalancer/python/main.py): FastAPI service with `/health` endpoint.
  - [python/Dockerfile](file:///Users/ernstvorsteveld/git/python/python-nginx-loadbalancer/python/Dockerfile): Multi-stage Docker setup using `uv`.
  - [python/pyproject.toml](file:///Users/ernstvorsteveld/git/python/python-nginx-loadbalancer/python/pyproject.toml) & `uv.lock`: Dependency definitions.
- `nginx/`: NGINX configuration directory.
  - [nginx/nginx.conf.template](file:///Users/ernstvorsteveld/git/python/python-nginx-loadbalancer/nginx/nginx.conf.template): NGINX configuration template.
- `docker-compose.yml`: Docker Compose configuration.
- `.env`: Environment variables.

## Environment Variables (`.env`)

```env
# Ports
NGINX_PORT=8080
APP1_PORT=8181
APP2_PORT=8182

# Service Names
APP1_SERVER_NAME=python-service-1
APP2_SERVER_NAME=python-service-2

# Tokens
USER_TOKEN_1=9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d

# Failure interval range (random integer between MIN and MAX)
FAIL_MIN=3
FAIL_MAX=7
```

## Behavior (`GET /health`)

- **HTTP Status Code**: Always returns `200 OK`.
- On every request, a `target_failure_count` is generated (`random.randint(FAIL_MIN, FAIL_MAX)`).
- If `request_count == target_failure_count`, `status` returns `false` and `request_count` resets to 0.
- If `request_count` reaches `FAIL_MAX` (upper bound), `request_count` resets to 0.
- `total_request_count` monotonically increments across all requests.

Example Response:
```json
{
  "status": true,
  "total_request_count": 14,
  "request_count": 3,
  "server_name": "python-service-1",
  "user_token": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```

## Running with Docker Compose

1. **Start/Rebuild Services:**
   ```bash
   docker compose down && docker compose up -d --build
   ```

2. **Test NGINX Load Balancer:**
   ```bash
   for i in {1..10}; do curl -s http://localhost:8080/my-service/health; echo ""; done
   ```

3. **Stop Services:**
   ```bash
   docker compose down
   ```
