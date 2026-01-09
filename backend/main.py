"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.core.config import settings
from app.api.rest.endpoints import router as rest_router
from app.api.graphql.schema import schema


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include REST API routes
    app.include_router(
        rest_router,
        prefix="/api/v1",
        tags=["REST API"]
    )
    
    # Include GraphQL routes
    graphql_app = GraphQLRouter(schema)
    app.include_router(
        graphql_app,
        prefix="/graphql",
        tags=["GraphQL"]
    )
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "LangChain App Boilerplate API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "graphql": "/graphql"
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
