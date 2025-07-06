from fastapi import FastAPI
from backend.routes.hr_extraction import router as hr_extraction_router
from backend.routes.resume_extraction import router as resume_extraction_router
from backend.routes.results import router as filters
import uvicorn

#declaring the app instance
app = FastAPI()

#including routers
app.include_router(hr_extraction_router)
app.include_router(resume_extraction_router)
app.include_router(filters)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
