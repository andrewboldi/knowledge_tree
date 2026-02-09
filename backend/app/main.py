"""FastAPI application for Knowledge Tree."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import concepts, graph, mvg, user_contributions
from .db.neo4j_client import get_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize and cleanup resources."""
    # Initialize Neo4j connection on startup
    client = get_client()
    client.init_schema()
    yield
    # Cleanup on shutdown
    client.close()


app = FastAPI(
    title="Knowledge Tree API",
    description="Interactive knowledge tree visualization with formal definitions",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(concepts.router, prefix="/api")
app.include_router(graph.router, prefix="/api")
app.include_router(mvg.router, prefix="/api")
app.include_router(user_contributions.router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
