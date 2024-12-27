from fastapi import APIRouter,Request,File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.transcricao import Transcricao
router = APIRouter()

@router.get("/")
def get_answer(request:Request):
    templates=Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("index.html",{"request":request})


@router.post("/transcricao")
async def get_transcricao(file:UploadFile=File(...)):
    transcricao=Transcricao()
    return await transcricao.transcrever(file)