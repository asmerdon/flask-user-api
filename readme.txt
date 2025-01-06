# Simple Flask API

## Endpoints

### GET /status
- **Description:** Check if the server is running.
- **Response:** `{"message": "Server is running"}`

### POST /data
- **Description:** Accepts JSON data.
- **Request Body Example:**
```json
{
    "name": "Alexander",
    "role": "Developer"
}

Response Example:

{
    "received_data": {
        "name": "Alexander",
        "role": "Developer"
    }
}
