from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import database, get_db
from routers import did, tokens, user  # Añade esta importación

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
app.include_router(did.router)
app.include_router(user.router)
app.include_router(tokens.router)

# Eventos de inicio/shutdown
@app.on_event("startup")
async def startup():
    database.connect()  # Conectar a la base de datos
    await database.create_tables()  # Crear tablas

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()  # Desconectar correctamente


# Endpoint de prueba de conexión
@app.get("/test-db", tags=["test"])
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "Database connection OK"}
    except Exception as e:
        return {"error": str(e)}

