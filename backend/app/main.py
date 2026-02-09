"""Knowledge Tree FastAPI Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Knowledge Tree API",
    description="Interactive knowledge tree visualization system API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "knowledge-tree"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Knowledge Tree API", "docs": "/docs"}
