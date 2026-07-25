# Python Nginx Loadbalancer - Health Check Service

A simple FastAPI health check service built with `uv`, packaged with Docker, and load-balanced via NGINX with custom header forwarding.

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
```

## Architecture & NGINX Tuning

- **Single NGINX Worker Process (`worker_processes 1;`)**: Configured in [nginx.conf.template](file:///Users/ernstvorsteveld/git/python/python-nginx-loadbalancer/nginx.conf.template) to guarantee 1-to-1 deterministic round-robin load balancing across all requests.
- **`max_fails=0`**: Ensures HTTP 500 responses (which happen every 5th call) do not mark upstream servers as offline.
- **Header Forwarding**: Injects `X-User-Token: ${USER_TOKEN_1}` into all proxied requests.

## Endpoint Response Example (`GET /health`)

```json
{
  "status": true,
  "request_count": 1,
  "server_name": "python-service-1",
  "user_token": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```

## Running with Docker Compose

1. **Start all services:**
   ```bash
   docker compose down && docker compose up -d
   ```

2. **Test NGINX Load Balancer:**
   ```bash
   for i in {1..10}; do curl -s http://localhost:8080/my-service/health; echo ""; done
   ```

3. **Stop Services:**
   ```bash
   docker compose down
   ```
