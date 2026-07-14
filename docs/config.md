# Configuration Module

## Directory Structure

```text
src/
└── config/
    ├── __init__.py
    ├── client.py
    ├── logger.py
    ├── logging.py
    └── settings.py
```

---

# Overview

The `config` package centralizes all application configuration, environment management, client initialization, and logging setup. By isolating configuration concerns from business logic, the project becomes easier to maintain, test, and deploy across multiple environments.

This module is one of the first components initialized during application startup and provides shared resources that are consumed throughout the application.

The configuration layer is responsible for:

* Loading environment variables.
* Validating required settings.
* Initializing Azure OpenAI clients.
* Configuring application logging.
* Providing reusable configuration objects.

---

# Configuration Architecture

```text
                .env
                  │
                  ▼
          settings.py
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   client.py          logging.py
        │                   │
        ▼                   ▼
 Azure OpenAI          Logger
        │                   │
        └─────────┬─────────┘
                  ▼
            Application
```

---

# File: `src/config/__init__.py`

## Purpose

Marks the `config` directory as a Python package.

It may also expose commonly used configuration objects for simplified imports throughout the project.

---

## Responsibilities

* Package initialization.
* Optional exports.
* Simplify module imports.

---

## Dependencies

None.

---

# File: `src/config/settings.py`

## Purpose

Loads, validates, and exposes application configuration.

This file serves as the central location for reading environment variables and making them available to the rest of the application.

---

## Responsibilities

* Read environment variables.
* Validate required configuration.
* Provide default values where appropriate.
* Create strongly typed configuration objects.
* Prevent application startup when critical configuration is missing.

---

## Typical Configuration Categories

### Azure OpenAI

* Endpoint
* API key
* Deployment name
* Embedding deployment

### Logging

* Log level
* Log format

### Application

* Environment
* Debug mode
* API version

### Retrieval

* Chunk size
* Chunk overlap
* Retrieval limits

---

## Inputs

* `.env`
* Operating system environment variables

---

## Outputs

A validated settings object shared across the application.

---

## Dependencies

* `python-dotenv`
* `pydantic-settings` (or equivalent configuration library)

---

## Workflow

```text
Read .env
    │
    ▼
Load Variables
    │
    ▼
Validate
    │
    ▼
Create Settings Object
    │
    ▼
Application Access
```

---

# File: `src/config/client.py`

## Purpose

Creates and manages external service clients used by the application.

The primary responsibility of this module is initializing Azure OpenAI clients using validated configuration.

Centralizing client creation avoids duplicate initialization logic and ensures consistent configuration across all consumers.

---

## Responsibilities

* Create Azure OpenAI client.
* Configure authentication.
* Configure endpoints.
* Reuse client instances.
* Handle client initialization errors.

---

## Typical Clients

Examples include:

* Azure OpenAI Chat Client
* Azure Embedding Client
* Search Client
* Content Safety Client

---

## Inputs

* Settings object
* API credentials
* Endpoint URLs

---

## Outputs

Configured client instances.

---

## Used By

* Agents
* RAG pipeline
* Evaluation framework
* API dependencies

---

## Workflow

```text
Settings
    │
    ▼
Read Credentials
    │
    ▼
Initialize Client
    │
    ▼
Validate Connection
    │
    ▼
Return Client
```

---

# File: `src/config/logger.py`

## Purpose

Provides helper functions for obtaining application loggers.

Rather than configuring logging repeatedly in each module, this file exposes reusable logging utilities.

---

## Responsibilities

* Create module loggers.
* Standardize logger names.
* Configure logger hierarchy.
* Provide convenience functions.

---

## Benefits

* Consistent logging style.
* Easier debugging.
* Reduced duplicated code.

---

## Typical Usage

Application modules import a configured logger instead of creating one manually.

---

# File: `src/config/logging.py`

## Purpose

Defines the application's logging configuration.

This file determines how logs are formatted, where they are written, and which log levels are enabled.

---

## Responsibilities

* Configure log handlers.
* Configure formatters.
* Configure log levels.
* Configure console output.
* Configure file output (if enabled).

---

## Typical Configuration

Logging may include:

* Timestamp
* Module name
* Log level
* Message
* Exception traceback

---

## Outputs

A fully configured logging system available throughout the application.

---

## Workflow

```text
Read Settings
      │
      ▼
Configure Formatter
      │
      ▼
Configure Handlers
      │
      ▼
Initialize Root Logger
      │
      ▼
Application Logging
```

---

# Configuration Flow

```text
Application Startup
        │
        ▼
Load Environment Variables
        │
        ▼
Validate Settings
        │
        ▼
Initialize Logging
        │
        ▼
Create Service Clients
        │
        ▼
Expose Shared Resources
```

---

# Module Relationships

```text
                 settings.py
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   client.py     logger.py    logging.py
        │             │             │
        └─────────────┼─────────────┘
                      ▼
             Entire Application
```

---

# Best Practices

## Centralize Configuration

Avoid reading environment variables directly in business logic. Access configuration through the shared settings module.

---

## Reuse Clients

Create external service clients once and share them across the application to reduce initialization overhead.

---

## Validate Early

Fail fast during application startup if required configuration is missing or invalid.

---

## Keep Secrets Out of Source Control

Sensitive values such as API keys should be stored in `.env` and excluded from version control.

---

## Standardize Logging

Use the shared logging configuration throughout the application to maintain consistent log formatting and severity levels.

---

# Related Modules

| Module             | Relationship                                                    |
| ------------------ | --------------------------------------------------------------- |
| `src/bootstrap.py` | Initializes configuration during application startup.           |
| `src/api/`         | Uses shared settings and clients through dependency injection.  |
| `src/agents/`      | Consumes configured Azure OpenAI clients and logging utilities. |
| `src/rag/`         | Uses embedding and search clients initialized here.             |
| `src/evaluation/`  | Reuses application configuration during benchmarking.           |
| `src/main.py`      | Loads configuration before starting the application.            |
