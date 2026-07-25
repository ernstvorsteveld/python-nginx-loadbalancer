# Python Nginx Loadbalancer - Health Check Service

A simple FastAPI health check service built with `uv`, packaged with Docker, and load-balanced via NGINX.

## Architecture

- **`app1`**: Exposed on host port `8181` (`SERVER_NAME=python-service-1`)
- **`app2`**: Exposed on host port `8182` (`SERVER_NAME=python-service-2`)
- **`nginx`**: Exposed on host port `8080`
  - Serves: `http://localhost:8080/my-service/health`
  - Upstreams requests to `host.docker.internal:8181` and `host.docker.internal:8182`.

## Endpoint Behavior (`GET /health`)

Returns JSON response including `status`, `request_count`, and `server_name`:
```json
{
  "status": true,
  "request_count": 1,
  "server_name": "python-service-1"
}
```
Every 5th request on a given instance returns `"status": false` with HTTP 500 status code.

## Running with Docker Compose

1. **Start all services:**
   ```bash
   docker compose up -d --build
   ```

2. **Test NGINX Load Balancer:**
   ```bash
   for i in {1..10}; do curl -i http://localhost:8080/my-service/health; echo ""; done
   ```

3. **Direct instance checks:**
   - App 1 (`python-service-1`): `curl -i http://localhost:8181/health`
   - App 2 (`python-service-2`): `curl -i http://localhost:8182/health`

4. **Stop Services:**
   ```bash
   docker compose down
   ```
