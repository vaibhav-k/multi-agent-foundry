"""
FastAPI application entry point.

Creates the HTTP API layer for the Enterprise IT Knowledge Assistant.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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

    app.include_router(router, prefix="/api/v1")

    @app.get(
        "/",
        response_class=HTMLResponse,
        include_in_schema=False,
    )
    def home():
        """
        Landing page showing application health.
        """

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Enterprise IT Knowledge Assistant</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background: #f5f7fa;
                    color: #222;
                }

                .card {
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    max-width: 600px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }

                .healthy {
                    color: green;
                    font-weight: bold;
                }

                a {
                    color: #0066cc;
                    text-decoration: none;
                }
            </style>
        </head>

        <body>
            <div class="card">
                <h1>Enterprise IT Knowledge Assistant</h1>

                <p>
                    Status:
                    <span class="healthy">Healthy</span>
                </p>

                <p>
                    Multi-agent RAG workflow is running.
                </p>

                <hr>

                <p>
                    API Health:
                    <a href="/api/v1/health">
                        /api/v1/health
                    </a>
                </p>

                <p>
                    API Documentation:
                    <a href="/docs">
                        /docs
                    </a>
                </p>

                <p>
                    Chat Endpoint:
                    <code>POST /api/v1/chat</code>
                </p>
            </div>
        </body>
        </html>
        """

    return app


app = create_app()
