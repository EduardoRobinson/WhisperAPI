from app.db.models import Transcricoes
from fastapi import APIRouter,Request,File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db
from app.services.transcricao import Transcricao
router = APIRouter()

@router.get("/")
def get_answer(request:Request):
    templates=Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("index.html",{"request":request})


@router.post("/transcricao")
async def get_transcricao(file:UploadFile=File(...),db: Session = Depends(get_db)):
    transcricao=Transcricao()
    texto=await transcricao.transcrever(file)
    transcricao = Transcricoes(description=texto.text)
    db.add(transcricao)
    db.commit()
    db.refresh(transcricao)
    return texto
