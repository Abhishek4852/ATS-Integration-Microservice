# Pagination & Error Handling Documentation

This document explains how pagination and error handling are implemented in the ATS Integration Microservice, how they are triggered, and the flow of data.

---

## Pagination

The pagination logic is centralized in [pagination.py](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/utils/pagination.py). This utility helps fetch large datasets (like jobs or applications) from ATS providers that limit the number of records returned in a single API call.

### The Pagination Utility

The `utils/pagination.py` file provides two generic strategies:

1.  **`paginate_all(fetch_page_func, start_page=1, **kwargs)`**: Used for page-based pagination (e.g., Page 1, Page 2, etc.).
2.  **`paginate_with_cursor(fetch_func, **kwargs)`**: Used for cursor-based pagination (where the API gives a "next page token").

### How it is Triggered

The pagination is triggered within the **Provider Layer** ([providers/](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/providers/)). Each ATS provider implementation decides if it needs to use the pagination helper based on the volume of data it expects.

#### The Trigger Flow
1.  **Client Request**: A user calls an endpoint like `GET /jobs`.
2.  **Handler**: [handler.py](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/handler.py) receives the request and calls the `JobsService`.
3.  **Service Layer**: [services/jobs_service.py](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/services/jobs_service.py) initializes the active provider (e.g., Greenhouse, Zoho) and calls `list_jobs()`.
4.  **Provider Layer**: The provider's `get_jobs()` method imports and calls `paginate_all`.

### Example: Greenhouse Provider Flow

The [GreenhouseProvider](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/providers/greenhouse.py) is a prime example:
```python
from utils.pagination import paginate_all

def get_jobs(self):
    # This call TRIGGERS the pagination loop
    return paginate_all(self._fetch_jobs_page)

def _fetch_jobs_page(self, page):
    # API call to Greenhouse is made here for a specific 'page'
    # Data is normalized and returned to the pagination utility
    return [self.normalize_job(j) for j in raw_jobs]
```

---

## Error Handling

The microservice ensures that all errors (from the ATS or internal validation) are returned as clean, consistent JSON objects.

### The Error Flow
1.  **ATS Error**: A provider (e.g., [ZohoProvider](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/providers/zoho.py)) encounters an API error (401, 404, 500).
2.  **Raise Exception**: The provider raises an `ATSError` (defined in [utils/errors.py](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/utils/errors.py)) with a descriptive message and the appropriate status code.
3.  **Catch Exception**: The Lambda [handler.py](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/handler.py) wraps service calls in `try/except` blocks to catch `ATSError`.
4.  **JSON Response**: The handler calls `error_response` from [utils/response.py](file:///Users/sachinyaduwanshi/Desktop/banao_assessment_task_2/utils/response.py), which formats the error into the standard JSON structure.

### Standard Error Response Format
```json
{
    "error": true,
    "message": "Detailed error message from the ATS or microservice",
    "status_code": 401
}
```

---

## Why use these utilities?
*   **Abstraction**: The Service and Handler layers don't need to know if the data was fetched in one shot or in 10 separate API calls.
*   **Consistency**: All providers can use the same logic for loop handling and error reporting.
*   **Reliability**: Centralized error handling ensures the client ALWAYS receives a valid JSON response, even when things go wrong.