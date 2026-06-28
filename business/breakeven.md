# Breakeven Analysis

## Cost per Active User (COGS)
*Based on a serverless architecture (AWS Lambda/Firebase) + LLM API usage for SQL generation/optimization.*

- **Compute (API Execution):** $4.50
  - Includes stateless containers for parsing and formatting requests.
- **LLM Inference (GPT-4o/Claude 3.5 Sonnet):** $5.00
  - Estimated 150 complex query generations/optimizations per month per active user.
- **Storage (Query History & Metadata):** $1.20
  - Encrypted storage for past queries, connection strings, and user preferences.
- **Bandwidth (Egress):** $0.30
  - Minimal text payload (JSON responses).
- **Total COGS:** **$11.00 per active user/month**

## Pricing Tiers

| Tier | Price | Target | Features |
| :--- | :--- | :--- | :--- |
| **Starter** | $0/mo | Students/Individuals | - 50 queries/mo<br>- Single data source connection<br>- Community support |
| **Pro** | $29/mo | Analysts/ Freelancers | - Unlimited queries<br>- 5 data source connections<br>- SQL optimization & auto-fix<br>- Query history & versioning<br>- Priority support |
| **Team** | $99/user/mo | Data Teams/Startups | - Everything in Pro<br>- SSO & RBAC<br>- Shared query snippets library<br>- Audit logs<br>- Slack/Teams integration<br>- Dedicated success manager |

## CAC Range
- **Range:** **$85 – $220**
- **Rationale:**
  - **Low end ($85):** Product-led growth (PLG) via GitHub stars, technical blog posts, and organic SEO for "SQL optimizer" keywords.
  - **High end ($220):** Targeted LinkedIn ads to "Head of Data" and "Data Engineer" titles, plus demo request conversion costs.

## LTV Estimate
- **Estimated LTV:** **$525**
- **Assumptions:**
  - **ARPU (Average Revenue Per User):** $35 (Weighted average of Pro and Team seats).
  - **Gross Margin:** ~62% (Revenue $35 - COGS $11 = $24 contribution).
  - **Average Customer Lifespan:** 22 months (High stickiness once integrated into daily workflow; churn risk only during platform migration).

## Break-even Users Count
- **Fixed Monthly Costs:** $3,500
  - Infrastructure baseline, monitoring tools, domain/SSL, and administrative overhead (excluding AxentX workforce labor).
- **Contribution Margin (Pro Tier):** $18.00 ($29 Price - $11 COGS)
- **Break-even Point:** **~195 users** (on the Pro plan).
  - *Calculation: $3,500 / $18 = 194.4*

## Path to $10K MRR
To achieve $10,000 MRR, we will pursue a hybrid "Bottom-Up + Land & Expand" strategy:

1.  **Phase 1: The Analyst Base (Months 1-3)**
    - **Target:** 300 Pro users @ $29/mo
    - **Revenue:** $8,700
    - **Strategy:** Aggressive content marketing on Reddit (r/dataengineering, r/SQL) and HackerNews. Focus on the "auto-fix" feature to hook frustrated analysts.

2.  **Phase 2: The Team Upsell (Months 3-5)**
    - **Target:** 15 Team seats (3 small teams of 5) @ $99/mo
    - **Revenue:** $1,485
    - **Strategy:** Identify Pro users with >5 active connections and offer a free Team trial to convert their department.

**Total MRR at Target:** **$10,185**
**Total Active Users:** **315**