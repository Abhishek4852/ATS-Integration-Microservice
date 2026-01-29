# Project Setup and Zoho OAuth Guide

This document explains how to set up the project and obtain the necessary Zoho OAuth credentials.

## 1. Project Setup

### Prerequisites
* Python 3.10+
* Node.js & NPM (for Serverless Framework)

### Installation
1.  **Clone the repository and enter the directory**:
    ```bash
    cd "banao_assessment task_2"
    ```

2.  **Set up a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Serverless Plugins**:
    ```bash
    npm install
    ```

5.  **Run Locally**:
    ```bash
    npx serverless offline
    ```
    The API will be available at `http://localhost:3000/dev`.

---

## 2. Obtaining Zoho OAuth Credentials

### Step A: Register Zoho Client
1.  Go to the [Zoho API Console](https://api-console.zoho.com/).
2.  Click **Add Client** and select **Server-based Applications**.
3.  Fill in the details:
    *   **Client Name**: ATS Integration
    *   **Homepage URL**: `http://localhost:3000` (or any valid URL)
    *   **Authorized Redirect URIs**: `http://localhost:3000/callback` (or any valid URL)
4.  Copy the **Client ID** and **Client Secret**. Add them to your `.env` file.

### Step B: Generate Grant Token (Authorization Code)
To get the refresh token, you first need a temporary Grant Token.

1.  In the Zoho API Console, click on your created client.
2.  Go to the **Generate Code** tab.
3.  Enter the required scopes:
    `ZohoRecruit.modules.ALL,ZohoRecruit.settings.ALL`
4.  Select a **Time Duration** (e.g., 10 minutes) and click **Generate**.
5.  Select your portal and click **Confirm**.
6.  You will get a **Grant Code**. Copy it immediately (it expires quickly).

### Step C: Get Refresh Token
Use the included helper script to exchange your Grant Code for a Refresh Token.

```bash
# Usage: python3 scripts/get_zoho_token.py <CLIENT_ID> <CLIENT_SECRET> <GRANT_CODE> <REDIRECT_URI>
python3 scripts/get_zoho_token.py YOUR_CLIENT_ID YOUR_CLIENT_SECRET YOUR_GRANT_CODE http://localhost:3000/callback
```

7.  Copy the **Refresh Token** from the output and add it to your `.env` file.

---

## 3. Environment Variables (.env)
Your `.env` file should now look like this:

```env
ATS_PROVIDER=zoho
ZOHO_CLIENT_ID=1000.XXXXXXXXXXXXXXXXXXXXXXXX
ZOHO_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ZOHO_REFRESH_TOKEN=1000.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ZOHO_BASE_URL=https://recruit.zoho.com/recruit/v2
ZOHO_TOKEN_URL=https://accounts.zoho.com/oauth/v2/token
```
