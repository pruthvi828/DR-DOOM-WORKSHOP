from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import (
    LocalActionExecuteRequest,
    LocalActionExecuteResponse,
    LocalActionPlanRequest,
    LocalActionPlanResponse,
    LocalActionStatusResponse,
)
from app.services.local_actions import execute_local_action, local_action_bridge_available, make_local_action_plan

router = APIRouter(prefix="/api/local-actions", tags=["local-actions"])


def require_local_origin(request: Request) -> None:
    origin = request.headers.get("origin")
    if not origin:
        return
    hostname = urlparse(origin).hostname
    if hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Local actions accept requests only from a local browser origin.")


@router.get("/status", response_model=LocalActionStatusResponse)
async def local_action_status(request: Request) -> LocalActionStatusResponse:
    require_local_origin(request)
    return LocalActionStatusResponse(enabled=local_action_bridge_available())


@router.post("/plan", response_model=LocalActionPlanResponse)
async def plan_local_action(request: Request, body: LocalActionPlanRequest) -> LocalActionPlanResponse:
    require_local_origin(request)
    if not local_action_bridge_available():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Local actions are disabled or unavailable.")
    plan = make_local_action_plan(body.text)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="That local application is not allowlisted.")
    return LocalActionPlanResponse(
        kind=plan["kind"],
        appId=plan["app_id"],
        label=plan["label"],
        requiresConfirmation=True,
    )


@router.post("/execute", response_model=LocalActionExecuteResponse)
async def execute_planned_local_action(request: Request, body: LocalActionExecuteRequest) -> LocalActionExecuteResponse:
    require_local_origin(request)
    try:
        app = execute_local_action(body.app_id)
    except RuntimeError as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except OSError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Windows could not open {request.app_id}.") from error
    return LocalActionExecuteResponse(ok=True, message=f"Opening {app.label}.")
