## tech‑spec.md – query‑craft v1  

---  

### 1. Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | **Python 3.11** | Mature ecosystem for SQL parsing, async I/O, and data‑science libs; easy to embed in CI/CD. |
| **Web framework** | **FastAPI** | High‑performance async, automatic OpenAPI docs, built‑in validation (pydantic). |
| **SQL engine** | **SQLGlot** (parser + transpiler) + **sql‑alchemy** (engine abstraction) | Handles dialect‑agnostic parsing, safe auto‑generation, and DB‑agnostic connections. |
| **Task queue** | **Celery 5** with **Redis** broker | Off‑load long‑running query generation & execution; supports retries & rate‑limiting. |
| **Container runtime** | **Docker** (official python:3.11‑slim) | Portable, reproducible builds; works on any cloud free tier. |
| **Orchestration** | **Docker Compose** (local) → **Fly.io** (free tier) for production | Fly.io offers free‑tier VMs with persistent volumes and global edge routing; simple `flyctl` deploy. |
| **Testing** | **pytest** + **httpx** (async client) | Fast, expressive unit/integration tests. |
| **Lint/format** | **ruff** (lint) + **black** (format) | Enforces code quality automatically in CI. |

---  

### 2. Hosting (free‑tier‑first)  

| Environment | Provider | Resources (Free Tier) | Deployment Model |
|-------------|----------|-----------------------|------------------|
| **Development / CI** | GitHub Actions | 2 k min/month, 20 GB storage | Build Docker image, run unit tests, push to GitHub Packages. |
| **Staging** | Fly.io (free VM) | 1 CPU, 256 MiB RAM, 1 GB persistent storage | `fly deploy --stage staging`. |
| **Production** | Fly.io (free VM) → optional upgrade to paid plan after validation | Same as staging; can scale to 2 VMs for HA after revenue validation. |
| **Secrets store** | Fly.io secrets (encrypted at rest) | Unlimited key/value pairs | `fly secrets set`. |
| **Static assets (OpenAPI UI)** | Served directly by FastAPI (no CDN needed). |

*If Fly.io capacity is exhausted, fallback to **Render.com** free web service (512 MiB RAM) – same Docker image.*  

---  

### 3. Data Model  

| Table / Collection | Description | Key Fields |
|--------------------|-------------|------------|
| **users** | Account records (internal SaaS users). | `id (UUID PK)`, `email (unique)`, `hashed_pw`, `role (enum: admin, user)`, `created_at`. |
| **api_keys** | Long‑lived tokens for programmatic access. | `id (UUID PK)`, `user_id (FK)`, `key (hashed)`, `name`, `scopes (json)`, `expires_at`, `created_at`. |
| **queries** | Persisted ad‑hoc query templates & execution metadata. | `id (UUID PK)`, `user_id (FK)`, `name`, `sql_template (text)`, `dialect (enum)`, `created_at`, `last_used_at`. |
| **jobs** | Celery task tracking for async query generation/execution. | `id (UUID PK)`, `query_id (FK)`, `status (enum)`, `result_location (s3‑compatible URI)`, `started_at`, `finished_at`, `error_msg`. |
| **audit_log** | Immutable audit trail for security/compliance. | `id (UUID PK)`, `user_id (FK)`, `action (enum)`, `resource_type`, `resource_id`, `timestamp`, `ip_address`. |

*All tables stored in **PostgreSQL** (Fly.io managed Postgres free tier, 1 GB).*

---  

### 4. API Surface  

| Method | Path | Purpose | Request Body (JSON) | Response |
|--------|------|---------|---------------------|----------|
| **POST** | `/auth/login` | Username/password → JWT | `{email, password}` | `{access_token, token_type:"bearer", expires_in}` |
| **POST** | `/auth/apikey` | Create a new API key (admin/user) | `{name, scopes[], expires_at?}` | `{key, id, created_at}` |
| **GET** | `/queries` | List saved query templates (paginated) | – | `{items:[{id,name,dialect,created_at}], next_cursor}` |
| **POST** | `/queries` | Save a new query template | `{name, sql_template, dialect}` | `{id, created_at}` |
| **GET** | `/queries/{id}` | Retrieve a single template | – | `{id,name,sql_template,dialect,created_at}` |
| **POST** | `/queries/{id}/run` | Trigger async generation + execution | `{params: {key: value}}` | `{job_id}` |
| **GET** | `/jobs/{job_id}` | Poll job status / result location | – | `{status, result_url?, error_msg?}` |
| **DELETE** | `/queries/{id}` | Delete a saved template (owner or admin) | – | `{deleted:true}` |
| **GET** | `/audit` | (admin) fetch audit entries (filterable) | query params `user_id, action, from, to` | `{items:[...], next_cursor}` |

*All endpoints require a Bearer JWT or valid API‑key header (`Authorization: Bearer <token>`).*  

---  

### 5. Security Model  

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | JWT (HS256) signed with secret stored in Fly.io secrets (`JWT_SECRET`). Token lifetime 1 h; refresh via `/auth/login`. API‑key auth uses same header, validated against hashed keys in DB. |
| **Authorization** | Role‑based (RBAC). `admin` can manage any user/query; `user` can only CRUD own queries and view own jobs. Scopes on API keys further restrict (e.g., `queries:read`, `jobs:run`). |
| **Secret Management** | - DB password, JWT secret, Celery broker URL stored as Fly.io secrets. <br>- No secrets baked into Docker image. |
| **IAM / Least Privilege** | PostgreSQL user with `SELECT, INSERT, UPDATE, DELETE` only on needed tables. Separate read‑only user for audit queries. |
| **Input Validation** | FastAPI + Pydantic models; SQLGlot sanitizes generated SQL, rejects dangerous statements (`DROP`, `ALTER`, `TRUNCATE`). |
| **Rate Limiting** | Per‑user token bucket (10 req/s) enforced by **slowapi** middleware; API‑key tokens have separate quota (e.g., 100 req/min). |
| **Transport Security** | All traffic via HTTPS (Fly.io terminates TLS with automatic certs). |
| **Data at Rest** | PostgreSQL encrypted at rest (Fly.io default). Result files stored in **MinIO** (self‑hosted on same VM) with server‑side encryption. |
| **Compliance** | Audit logs immutable, retained 90 days (configurable). |

---  

### 6. Observability  

| Component | Logs | Metrics | Traces |
|-----------|------|---------|--------|
| **FastAPI** | Structured JSON logs (timestamp, level, request_id, path, status). Sent to **stdout** → captured by Fly.io logs. | Prometheus metrics via **starlette‑exporter** (`http_requests_total`, `request_duration_seconds`). | **OpenTelemetry** (Python SDK) auto‑instrumented for incoming requests. |
| **Celery Workers** | Task start/finish logs with `job_id`. | `celery_task_success_total`, `celery_task_failure_total`, `celery_task_runtime_seconds`. | OpenTelemetry spans for each task (generation → execution). |
| **PostgreSQL** | Enable `log_min_duration_statement = 200ms`. | Exported via **postgres_exporter** (Fly.io sidecar). | N/A (DB traces via OpenTelemetry pg driver). |
| **MinIO** | Access logs to stdout. | `minio_requests_total`, `minio_bytes_sent`. | N/A. |
| **Alerting** | Fly.io alerts on container restarts, high CPU (>80%). | Prometheus Alertmanager rules: job failures > 5/min, 5xx rate > 1%. | Integrated with OpenTelemetry Collector → exported to **Grafana Cloud** (free tier). |

---  

### 7. Build / CI  

| Stage | Tool | Steps |
|-------|------|-------|
| **Lint** | `ruff` + `black` | `ruff . --fix && black .` |
| **Unit Tests** | `pytest` | `pytest -q --cov=app` |
| **Security Scan** | **Bandit** + **Safety** | `bandit -r app && safety check --full-report` |
| **Docker Build** | GitHub Actions | `docker build -t ghcr.io/arkashira/query-craft:${{ github.sha }}` |
| **Publish Image** | GitHub Packages | `docker push ghcr.io/arkashira/query-craft:${{ github.sha }}` |
| **Deploy Staging** | Fly.io CLI | `fly deploy --app query-craft-staging --image ghcr.io/arkashira/query-craft:${{ github.sha }}` |
| **Smoke Test** | `httpx` script | Verify `/healthz` returns 200. |
| **Tag Release** | GitHub Release workflow | On `main` merge with `v*` tag → creates GitHub Release, bumps version in `pyproject.toml`. |

*All workflows run on Ubuntu‑latest runners; caching enabled for pip packages.*  

---  

**End of tech‑spec.md**.  