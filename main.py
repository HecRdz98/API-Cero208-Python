from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession
from database import database, get_db

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)

# Eventos de inicio/shutdown
@app.on_event("startup")
async def startup():
    database.connect()  # Conectar a la base de datos
    await database.create_tables()  # Crear tablas

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # Desconectar correctamente

@app.get("/", tags=["Home"])
async def home():
    return {"message": "Hello World!"}

# Endpoint de prueba de conexión
@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "Database connection OK"}
    except Exception as e:
        return {"error": str(e)}