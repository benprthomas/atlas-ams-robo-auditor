import logging
import traceback

from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, Request, status, Query
from fastapi.responses import JSONResponse

from app.core import get_db_session
from app.services import modelService, modelNotFoundError
from app.schemas.pydantic.model import modelUploadRequest

model_router = APIRouter()
logger = logging.getLogger(__name__)


@model_router.post(
    "/upload",
    summary="stores the model posting in the database by parsing the JD into a structured format JSON",
)
async def upload_model(
    payload: modelUploadRequest,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Accepts a model description as a MarkDown text and stores it in the database.
    """
    request_id = getattr(request.state, "request_id", str(uuid4()))

    allowed_content_types = [
        "application/json",
    ]

    content_type = request.headers.get("content-type")
    if not content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content-Type header is missing",
        )

    if content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Content-Type. Only {', '.join(allowed_content_types)} is/are allowed.",
        )

    try:
        model_service = modelService(db)
        model_ids = await model_service.create_and_store_model(payload.model_dump())

    except AssertionError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}",
        )

    return {
        "message": "data successfully processed",
        "model_id": model_ids,
        "request": {
            "request_id": request_id,
            "payload": payload,
        },
    }


@model_router.get(
    "",
    summary="Get model data from both model and processed_model models",
)
async def get_model(
    request: Request,
    model_id: str = Query(..., description="model ID to fetch data for"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Retrieves model data from both model_model and processed_model model by model_id.

    Args:
        model_id: The ID of the model to retrieve

    Returns:
        Combined data from both model and processed_model models

    Raises:
        HTTPException: If the model is not found or if there's an error fetching data.
    """
    request_id = getattr(request.state, "request_id", str(uuid4()))
    headers = {"X-Request-ID": request_id}

    try:
        if not model_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="model_id is required",
            )

        model_service = modelService(db)
        model_data = await model_service.get_model_with_processed_data(
            model_id=model_id
        )
        
        if not model_data:
            raise modelNotFoundError(
                message=f"model with id {model_id} not found"
            )

        return JSONResponse(
            content={
                "request_id": request_id,
                "data": model_data,
            },
            headers=headers,
        )
    
    except modelNotFoundError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error fetching model: {str(e)} - traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching model data",
        )
