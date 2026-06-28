## dataflow.md  

### System Dataflow Architecture for **query‑craft**

```
+-------------------+        +-------------------+        +-------------------+
|  External Data    |  -->   |   Ingestion Layer |  -->   |   Processing /   |
|  Sources          |        |   (API / Connect) |        |   Transform Tier |
|  (RDBMS, DW,      |        |   - Kafka / Kinesis|        |   - Spark / Flink |
|   SaaS, Files)   |        |   - DB Connectors |        |   - SQL Parser   |
+-------------------+        +-------------------+        +-------------------+
        |                           |                           |
        |                           v                           v
        |                     +-------------------+      +-------------------+
        |                     |   Storage Tier    |      |   Query / Serving |
        |                     |   (Lakehouse)     |      |   Layer           |
        |                     | - S3 / ADLS Gen2  |      | - Presto / Trino  |
        |                     | - Delta Lake      |      | - GraphQL API     |
        |                     | - Metadata Store  |      | - REST Endpoints  |
        |                     +-------------------+      +-------------------+
        |                           |                           |
        |                           v                           v
        |                     +-------------------+      +-------------------+
        |                     |   Auth / Security |      |   Egress to User  |
        |                     |   (IAM, OIDC)     |      |   (Web UI, CLI,  |
        |                     +-------------------+      |    SDKs)          |
        |                                                +-------------------+
        +--------------------------------------------------------------+
```

---

### 1. External Data Sources  
- **Relational DBs:** PostgreSQL, MySQL, SQL Server, Oracle  
- **Data Warehouses:** Snowflake, BigQuery, Redshift, Azure Synapse  
- **SaaS APIs:** Salesforce, HubSpot, Marketo (via native connectors)  
- **File Stores:** CSV/Parquet on S3, Azure Blob, GCS, on‑prem NFS  

### 2. Ingestion Layer  
| Component | Role | Tech / Config |
|-----------|------|---------------|
| **Connector Service** | Pulls data via JDBC/ODBC, REST, or CDC | Apache NiFi, Airbyte, or custom Go micro‑service |
| **Message Bus** | Buffers change events & batch loads | Kafka (confluent) or AWS Kinesis |
| **Auth Boundary** | Enforces source‑specific credentials & least‑privilege | Vault / AWS Secrets Manager + IAM roles |
| **Schema Registry** | Stores source schemas for downstream parsing | Confluent Schema Registry (Avro/JSON) |

### 3. Processing / Transform Layer  
- **SQL Parser & Normalizer** – ANTLR‑based parser that rewrites ad‑hoc queries into canonical form.  
- **Query Optimizer** – Leverages Apache Calcite to generate cost‑based plans.  
- **Transformation Engine** – Spark Structured Streaming / Flink for real‑time enrichment, masking, and denormalization.  
- **Metadata Enrichment** – Adds lineage, data‑quality tags, and business glossary terms (via OpenMetadata).  

**Auth Boundary:** Execution runs under a dedicated service account with scoped permissions on the storage tier; all jobs signed with JWT issued by internal Auth Service.

### 4. Storage Tier (Lakehouse)  
- **Object Store** – Amazon S3 (or Azure ADLS Gen2) as immutable raw zone.  
- **Delta Lake / Iceberg** – Provides ACID transactions, time‑travel, and schema evolution for curated tables.  
- **Metadata Catalog** – AWS Glue Data Catalog or Hive Metastore for table discovery.  
- **Security** – Bucket policies + SSE‑KMS encryption; row‑level security enforced via Delta Lake’s column‑masking features.  

### 5. Query / Serving Layer  
- **SQL Engine** – Trino (formerly PrestoSQL) for federated, low‑latency query execution across raw & curated zones.  
- **API Gateway** – Kong / AWS API Gateway exposing:  
  - **GraphQL endpoint** for dynamic query composition.  
  - **REST endpoints** for CRUD on saved queries, templates, and execution results.  
- **Cache** – Redis (TTL‑based) for frequently executed query results.  
- **Auth Boundary:** OAuth2 / OIDC tokens validated at API Gateway; fine‑grained ACLs stored in the Metadata Catalog (who can query which datasets).  

### 6. Egress to User  
- **Web UI** – React SPA with embedded SQL editor (Monaco) and visual query builder.  
- **CLI / SDK** – Python & Go client libraries for programmatic access (pip install query‑craft‑sdk).  
- **Export Options** – CSV, Parquet, JSON, or direct push to downstream tools (Looker, PowerBI via ODBC).  
- **Notification Service** – Slack / Teams webhook integration for query completion alerts.  

**Auth Boundary:** End‑user authentication via corporate IdP (SAML/OIDC). Session tokens scoped to user roles (analyst, data‑engineer, admin). All outbound traffic encrypted (TLS 1.3).  

---  

### Summary of Auth Boundaries  

| Boundary | Enforced By | Scope |
|----------|--------------|-------|
| Source Credential Store | Vault / Secrets Manager | Ingestion |
| Service‑to‑Service JWT | Internal Auth Service | Ingestion → Processing |
| Execution Service Account | IAM Role | Processing → Storage |
| API Gateway Token Validation | Kong/OAuth2 Provider | Query/Serving → Egress |
| End‑User Session | Corporate IdP (SAML/OIDC) | UI/CLI/SDK |

---  

*All components are container‑orchestrated via Kubernetes (EKS/AKS) with Helm charts for reproducible deployments and autoscaling.*