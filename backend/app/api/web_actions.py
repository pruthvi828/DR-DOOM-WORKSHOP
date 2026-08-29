from fastapi import APIRouter

from app.schemas import WebActionPlanRequest, WebActionPlanResponse
from app.services.web_action_planner import make_web_action_plan

router = APIRouter(prefix="/api/web-actions", tags=["web-actions"])


@router.post("/plan", response_model=WebActionPlanResponse)
async def plan_web_action(request: WebActionPlanRequest) -> WebActionPlanResponse:
    return WebActionPlanResponse(**make_web_action_plan(request.text.strip()))
