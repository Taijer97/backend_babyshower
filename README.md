# Backend FastAPI

## Ejecutar

1. Crear entorno virtual
   - Windows: `python -m venv venv`
   - Activar: `venv\\Scripts\\activate`
2. Instalar dependencias: `pip install -r backend/requirements.txt`
3. Variables de entorno: copiar `backend/.env.example` a `.env` y ajustar
4. Lanzar servidor: `uvicorn app.main:app --reload --port 8000`

## Base de datos

- Desarrollo: `sqlite+aiosqlite:///./backend.db`
- MySQL: `mysql+aiomysql://usuario:password@host:puerto/base`
