
# CreateAgentApiView

## Description
This API view is responsible for creating a new agent user in the system. It accepts the necessary user details, validates them, and creates a user with the role of an agent. If the email is already in use or required fields are missing, it will return an error.

## Endpoint
- **URL**: `/api/create-agent/`
- **Method**: `POST`
- **Content-Type**: `application/json`

## Request Body
The request body must contain the following fields:
- `email`: (string) **Required** - The email address of the agent.
- `password`: (string) **Required** - The password for the agent.
- `first_name`: (string) **Optional** - The first name of the agent.
- `last_name`: (string) **Optional** - The last name of the agent.
- `username`: (string) **Optional** - The username of the agent. If not provided, the full name will be used as fallback.

### Example Request
```json
{
    "email": "agent@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe"
}
```

## Responses

### Success Response
- **Status Code**: `201 Created`
- **Response Body**:
```json
{
    "message": "Agent johndoe (agent@example.com) created successfully."
}
```

### Error Responses

#### 1. Missing Required Fields (Email or Password)
- **Status Code**: `400 Bad Request`
- **Response Body**:
```json
{
    "error": "Email and password are required."
}
```

#### 2. Email Already Exists
- **Status Code**: `400 Bad Request`
- **Response Body**:
```json
{
    "error": "Email already exists for another user."
}
```

## Notes
- **Authentication**: This view doesn't require authentication as it's intended to be used for agent creation.
- **Validation**: It checks if the email is already in use and ensures the email and password fields are provided.
- **User Role**: By default, the user will be created as an agent (`is_agent=True`) and not as a customer (`is_customer=False`).

## Example Flow
1. The client sends a POST request to the endpoint `/api/create-agent/` with the required data (email, password, and optionally first_name, last_name, and username).
2. If the data is valid and the email is not already taken, a new agent is created and a success response is returned.
3. If there is an error (missing fields or email already exists), an error response is returned with a message explaining the issue.
```
