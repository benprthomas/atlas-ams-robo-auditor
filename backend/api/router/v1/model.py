import logging
import traceback

from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import (
    APIRouter,
    File,
    UploadFile,
    HTTPException,
    Depends,
    Request,
    status,
    Query,
)

from app.core import get_db_session
from app.services import (
    curService,
    ScoreImprovementService,
    curNotFoundError,
    curParsingError,
    modelNotFoundError,
)
from app.schemas.pydantic import curImprovementRequest

cur_router = APIRouter()
logger = logging.getLogger(__name__)


@cur_router.post(
    "/upload",
    summary="Upload a cur in PDF or DOCX format and store it into DB in HTML/Markdown format",
)
async def upload_cur(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Accepts a PDF or DOCX file, converts it to HTML/Markdown, and stores it in the database.

    Raises:
        HTTPException: If the file type is not supported or if the file is empty.
    """
    print("cur uploading start ...")
    request_id = getattr(request.state, "request_id", str(uuid4()))

    allowed_content_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    print("Allowed content types : ")
    print(allowed_content_types)

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF and DOCX files are allowed.",
        )

    file_bytes = await file.read()
    print("File bytes : ")
    print(file_bytes)
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file. Please upload a valid file.",
        )

    print("cur service running ...")
    try:
        cur_service = curService(db)
        cur_id = await cur_service.convert_and_store_cur(
            file_bytes=file_bytes,
            file_type=file.content_type,
            filename=file.filename,
            content_type="md",
        )
    except Exception as e:
        logger.error(
            f"Error processing file: {str(e)} - traceback: {traceback.format_exc()}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}",
        )

    return {
        "message": f"File {file.filename} successfully processed as MD and stored in the DB",
        "request_id": request_id,
        "cur_id": cur_id,
    }


@cur_router.post(
    "/improve"
)
async def score_and_improve(
    request: Request,
    payload: curImprovementRequest,
    db: AsyncSession = Depends(get_db_session),
    stream: bool = Query(
        False, description="Enable streaming response using Server-Sent Events"
    ),
):
    """
    Scores and improves a cur against a model description.

    Raises:
        HTTPException: If the cur or model is not found.
    """
    request_id = getattr(request.state, "request_id", str(uuid4()))
    headers = {"X-Request-ID": request_id}

    request_payload = payload.model_dump()

    try:
        cur_id = str(request_payload.get("cur_id", ""))
        if not cur_id:
            raise curNotFoundError(
                message="invalid value passed in `cur_id` field, please try again with valid cur_id."
            )
        model_id = str(request_payload.get("model_id", ""))
        if not model_id:
            raise modelNotFoundError(
                message="invalid value passed in `model_id` field, please try again with valid model_id."
            )
        score_improvement_service = ScoreImprovementService(db=db)

        if stream:
            return StreamingResponse(
                content=score_improvement_service.run_and_stream(
                    cur_id=cur_id,
                    model_id=model_id,
                ),
                media_type="text/event-stream",
                headers=headers,
            )
        else:
            improvements = await score_improvement_service.run(
                cur_id=cur_id,
                model_id=model_id,
            )
            return JSONResponse(
                content={
                    "request_id": request_id,
                    "data": improvements,
                },
                headers=headers,
            )
    except curNotFoundError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except modelNotFoundError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except curParsingError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error: {str(e)} - traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="sorry, something went wrong!",
        )


@cur_router.get(
    "",
    summary="Get cur data from both cur and processed_cur models",
)
async def get_cur(
    request: Request,
    cur_id: str = Query(..., description="cur ID to fetch data for"),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Retrieves cur data from both cur_model and processed_cur model by cur_id.

    Args:
        cur_id: The ID of the cur to retrieve

    Returns:
        Combined data from both cur and processed_cur models

    Raises:
        HTTPException: If the cur is not found or if there's an error fetching data.
    """
    request_id = getattr(request.state, "request_id", str(uuid4()))
    headers = {"X-Request-ID": request_id}

    try:
        if not cur_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="cur_id is required",
            )

        cur_service = curService(db)
        cur_data = await cur_service.get_cur_with_processed_data(
            cur_id=cur_id
        )
        
        if not cur_data:
            raise curNotFoundError(
                message=f"cur with id {cur_id} not found"
            )

        return JSONResponse(
            content={
                "request_id": request_id,
                "data": cur_data,
            },
            headers=headers,
        )
    
    except curNotFoundError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error fetching cur: {str(e)} - traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching cur data",
        )