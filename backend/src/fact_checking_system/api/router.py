from fastapi import APIRouter

from fact_checking_system.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])


@api_router.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {"name": "fact-checking-system", "status": "ready-for-specification"}
