# ATS Integration Microservice

A serverless Python microservice that provides a unified REST API for integrating with multiple Applicant Tracking Systems (ATS) like Zoho, Greenhouse, and Workable.

---

## 1. ATS Setup & Access

This service abstracts the complexity of different ATS providers. To use it, you need to set up accounts and generate credentials.

### How to Create a Sandbox / Free Trial
*   **Zoho Recruit**: Visit the [Zoho Recruit Free Trial](https://www.zoho.com/recruit/signup.html) page. They offer a 15-day free trial of their enterprise features.
*   **Greenhouse**: Standard sandboxes are usually reserved for customers or partners. You can explore their APIs using their [Developer Portal](https://developers.greenhouse.io/).
*   **Workable**: Sign up for a 15-day free trial on the [Workable website](https://www.workable.com/free-trial/). No credit card is required.

### How to Generate API Keys / Tokens

#### Zoho Recruit (OAuth 2.0)
Zoho requires a more detailed setup compared to others. Follow these steps:

1.  **Register Zoho Client**:
    - Go to the [Zoho API Console](https://api-console.zoho.com/).
    - Click **Add Client** -> **Server-based Applications**.
    - Set **Homepage URL** and **Authorized Redirect URIs** (e.g., `http://localhost:3000/callback`).
    - Copy the **Client ID** and **Client Secret**.

2.  **Generate Grant Token**:
    - In the Console, go to the **Generate Code** tab of your client.
    - Scopes: `ZohoRecruit.modules.ALL,ZohoRecruit.settings.ALL`
    - Click **Generate** and copy the **Grant Code**.

3.  **Get Refresh Token**:
    Run the included helper script:
    ```bash
    python3 scripts/get_zoho_token.py YOUR_CLIENT_ID YOUR_CLIENT_SECRET YOUR_GRANT_CODE http://localhost:3000/callback
    ```
    Copy the **Refresh Token** from the output.

#### Greenhouse
Go to `Configure (Gear Icon) -> Dev Center -> API Credential Management` and click "Create New API Key".

#### Workable
Navigate to `Settings -> Integrations -> Access Tokens` and generate a new token.

---

## 2. Local Development

### Prerequisites
- Python 3.10+
- Node.js & NPM
- Active ATS credentials

### Local Setup
1.  **Clone the repository and enter the directory**:
    ```bash
    cd banao_assessment_task_2
    ```
2.  **Set up a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    npm install
    ```

### Configuration (.env)
Create a `.env` file in the root directory.

**For Zoho:**
```env
ATS_PROVIDER=zoho
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
ZOHO_BASE_URL=https://recruit.zoho.com/recruit/v2
ZOHO_TOKEN_URL=https://accounts.zoho.com/oauth/v2/token
```

**For Greenhouse/Workable:**
```env
ATS_PROVIDER=greenhouse  # or workable
ATS_API_KEY=your_api_key
ATS_BASE_URL=https://api.greenhouse.io/v1
```

### Running the Service
```bash
npx serverless offline start
```
The service will be available at `http://localhost:3000/dev`.

---

## 3. API Documentation & Examples

### [GET] `/jobs`
Fetches a normalized list of all available job openings.

**Curl Command:**
```bash
curl http://localhost:3000/dev/jobs
```

**Response Screenshot:**
*(Place screenshot here)*

---

### [POST] `/candidates`
Submits a candidate application for a specific job.

**Curl Command:**
```bash
curl -X POST http://localhost:3000/dev/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe453@example.com",
    "phone": "555-0199998",
    "job_id": "210805000000354811"
  }'
```

**Response Screenshot:**
*(Place screenshot here)*

---

### [GET] `/applications?job_id=ID`
Retrieves all applications associated with a specific job ID.

**Curl Command:**
```bash
curl "http://localhost:3000/dev/applications?job_id=210805000000354811"
```

**Response Screenshot:**
*(Place screenshot here)*

---

## 4. Error Handling & Pagination Implementation

For a technical deep dive, see [doc.md](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/doc.md).

### Error Handling Flow
The microservice catches ATS-specific failures and wraps them into a **Clean JSON Error**.
- Provider raises `ATSError`.
- `handler.py` catches the error.
- Client receives a structured JSON with `error: true`, a message, and a status code.

### Pagination Implementation
Implemented in `utils/pagination.py`:
- **Sequential Fetching**: Fetches all pages one by one to respect rate limits.
- **Safety Break**: Hard limit of **100 pages** per request to prevent infinite loops.
- **Aggregation**: Combines all results into a single list before returning to the client.
