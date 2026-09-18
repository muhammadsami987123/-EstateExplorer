from fastapi import APIRouter
from app.schemas.ai import ChatRequest, AnalyzeRequest, ExtractRequest, CompareRequest, InsightRequest
from app.services.ai import get_ai_response, analyze_property, extract_search_params, compare_properties, get_market_insight

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    response = await get_ai_response(messages)
    return {"response": response}


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    response = await analyze_property(request.property, request.preferences)
    return {"response": response}


@router.post("/extract")
async def extract(request: ExtractRequest):
    params = await extract_search_params(request.text)
    return {"params": params}


@router.post("/compare")
async def compare(request: CompareRequest):
    response = await compare_properties(request.properties, request.preferences)
    return {"response": response}


@router.post("/insight")
async def insight(request: InsightRequest):
    response = await get_market_insight(request.location_id)
    return {"response": response}
