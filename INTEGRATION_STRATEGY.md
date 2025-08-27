# Julius Service Bus Integration Strategy

This document outlines the integration strategy for connecting the existing systems (`CritterCraftUniverse`, `Prometheus Protocol`, `V-Architect`) to the Julius Service Bus. The goal is to modify each system to act as a client of the service bus, sending standardized `Message` payloads to the central queue.

---

## 1. CritterCraftUniverse Integration

The `CritterCraftUniverse` is a Python-based application with a Flask API. The integration will focus on capturing key events from the user management and game logic and publishing them to the Julius Service Bus.

### 1.1. Go Client Library

A small Go client library will be developed in the `pkg/` directory of the `julius_service_bus` project. This library will provide a simple function to send a `Message` to a specified Julius instance. This library will then be compiled to a shared library (`.so` or `.dll`) and wrapped in a Python module using `ctypes` or `cgo`.

Alternatively, and more simply for this phase, the Python application can make a direct HTTP POST request to the Julius Service Bus API endpoint. This avoids the complexity of a shared library. **This is the recommended approach for the initial implementation.**

### 1.2. Python Integration Module

A new Python module, `julius_client.py`, will be created in `BlockChain/critter-craft/src/services/`. This module will be responsible for:
- Defining the `Message` structure (as a Python dictionary or class).
- A `publish_event` function that takes a `source`, `event_type`, and `payload`, constructs a `Message`, and sends it to the Julius Service Bus API endpoint via an HTTP POST request.

### 1.3. Integration Points

The `publish_event` function will be called from the following key locations in the `CritterCraftUniverse` codebase:

- **`user_manager.py`**:
    - `register()`: After a new user is successfully registered, publish a `UserRegistered` event.
    - `login()`: After a successful login, publish a `UserLoggedIn` event.
    - `update_user_profile()`: The existing placeholder `print` statement will be replaced with a call to `publish_event` to send a `UserProfileUpdated` event.

- **Game Logic (Future)**:
    - When new game-related services are added (e.g., `pet_manager.py`), events like `PetCreated`, `PetEvolved`, `TransactionCompleted` will be published.

### 1.4. Example Event Payload (`UserProfileUpdated`)

```json
{
  "source": "CritterCraftUniverse",
  "event_type": "UserProfileUpdated",
  "payload": {
    "user_id": "...",
    "updated_fields": ["username"],
    "timestamp": "..."
  }
}
```

---

## 2. Prometheus Protocol Integration (Proposed)

**Assumption:** The `Prometheus Protocol` is a monitoring and alerting system.

### 2.1. Integration Point: Alert Manager

The integration will likely happen at the "Alert Manager" level of the Prometheus stack. A custom webhook receiver will be configured in the Alert Manager.

### 2.2. Webhook Handler

A small web service (which could be part of the Julius Service Bus itself, or a separate microservice) will be created to act as the webhook receiver. This service will:
- Receive alerts from the Prometheus Alert Manager.
- Transform the alert data into the standard `Message` format.
- Publish the `Message` to the Julius Service Bus.

### 2.3. Example Event Payload (`HighCpuUsageAlert`)

```json
{
  "source": "PrometheusProtocol",
  "event_type": "HighCpuUsageAlert",
  "payload": {
    "instance": "prod-web-server-01",
    "severity": "critical",
    "value": "95%",
    "summary": "High CPU usage detected on prod-web-server-01"
  }
}
```

---

## 3. V-Architect Integration (Proposed)

**Assumption:** `V-Architect` is an infrastructure-as-code or deployment automation tool.

### 3.1. Integration Point: Command Execution Wrapper

The core command execution logic of `V-Architect` will be wrapped in a new module. This wrapper will be responsible for publishing events after a command is executed.

### 3.2. Event Publishing

After each `V-Architect` command (e.g., `deploy-service`, `run-migration`) is executed, the wrapper will:
- Determine if the command was successful or failed.
- Construct a `Message` with the relevant details.
- Publish the `Message` to the Julius Service Bus.

### 3.3. Example Event Payload (`DeploymentSucceeded`)

```json
{
  "source": "VArchitect",
  "event_type": "DeploymentSucceeded",
  "payload": {
    "service_name": "crittercraft-api",
    "version": "v1.2.3",
    "environment": "production",
    "duration_seconds": 125
  }
}
```
