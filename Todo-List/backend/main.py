from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks , categories
from app.core.database import Base
from app.core.database import engine
import uvicorn
import logging


# Create the database tables 
Base.metadata.create_all(bind=engine)


# Create the FastAPI app instance with metadata
app = FastAPI(
    title="Todo App",
    description="description",
    summary="Todo App with FastAPI and React",
    version="0.0.1",
)


# Define the root route
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Include routers from other files in the app
app.include_router(tasks.router, prefix="/v1", tags=["tasks"])
app.include_router(categories.router, prefix="/v1", tags=["categories"])


# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin",
                    "Access-Control-Allow-Headers"]
)

# Configure logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'watchfiles.main': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
