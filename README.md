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
*   **Zoho Recruit (OAuth 2.0)**: Follow the detailed step-by-step guide in [SETUP.md](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/SETUP.md#2-obtaining-zoho-oauth-credentials) to register a client and generate a refresh token.
*   **Greenhouse**: Go to `Configure (Gear Icon) -> Dev Center -> API Credential Management` and click "Create New API Key".
*   **Workable**: Navigate to `Settings -> Integrations -> Access Tokens` and generate a new token.

---

## 2. Local Development

### Prerequisites
- Python 3.10+
- Node.js & NPM (for Serverless Framework)
- Active ATS credentials (API Key or Refresh Token)

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
4.  **Configure Environment**: Create a `.env` file from the [SETUP.md Template](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/SETUP.md#3-environment-variables-env).

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
    "email": "jane.doe@example.com",
    "phone": "555-0199",
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
When an ATS returns an error (e.g., 401 Unauthorized or 404 Not Found), the microservice catches the exception in the Provider layer and wraps it into a **Clean JSON Error**.

**Internal Logic:**
1.  Provider raises `ATSError(message, status_code)`.
2.  `handler.py` catches the error in a `try/except` block.
3.  Client receives:
    ```json
    {
      "error": true,
      "message": "Friendly error message",
      "status_code": 401
    }
    ```

### Pagination Implementation
The service uses a recursive fetching strategy to ensure all data is retrieved, even if the ATS paginates its responses.

*   **How it works**: The `utils/pagination.py` utility handles the loop. It calls the provider's fetch method repeatedly, incrementing the `page` number each time until no more results are found.
*   **Concurrency & Speed**: Pages are currently fetched **sequentially** (one at a time) to respect ATS rate limits and avoid overwhelming the external API.
*   **Safety Break**: To prevent infinite loops with mock data or misbehaving APIs, there is a hard safety limit of **100 pages** per request.
*   **Data Source**: All pages are aggregated into a single list before being returned to the user, providing a seamless "fetch all" experience.
