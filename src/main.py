from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.transactions.router import router as transactions_router
from src.database import Base
from src.database import get_engine, close_db_connections
from src import init_platform

engine = get_engine()

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database and admin user
    get_engine()
    init_platform.create_admin_user()
        
    yield
    
    # Cleanup db connection
    close_db_connections()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(transactions_router)

@app.get('/')
def welcome():
    return {'detail':'Welcome to finapi'}