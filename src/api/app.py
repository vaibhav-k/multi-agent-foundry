"""
FastAPI application entry point.

Creates the HTTP API layer for the Enterprise IT Knowledge Assistant.
"""

from fastapi import FastAPI

from src.api.routes import router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """

    app = FastAPI(
        title="Enterprise IT Knowledge Assistant",
        description=(
            "Multi-agent RAG assistant using Azure AI Foundry, "
            "Azure AI Search, and Azure AI Content Safety."
        ),
        version="1.0.0",
    )

    app.include_router(router)

    return app


app = create_app()
