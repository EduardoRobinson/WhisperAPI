from app.db.models import Transcricoes
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import Depends, HTTPException

class TranscricoesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, transcricao: Transcricoes):
        try:
            self.db.add(transcricao)
            self.db.commit()
            self.db.refresh(transcricao)
            return transcricao
        except Exception as e:
            self.db.rollback() 
            raise HTTPException(status_code=500, detail=f"Erro ao criar a transcrição: {str(e)}")

    def delete(self, transcricao_id: int):
        try:
            transcricao = self.db.query(Transcricoes).get(transcricao_id)
            if not transcricao:
                raise HTTPException(status_code=404, detail="Transcrição não encontrada")
            self.db.delete(transcricao)
            self.db.commit()
            return {"message": "Transcrição deletada com sucesso"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao deletar a transcrição: {str(e)}")

    def update(self, transcricao_id: int, transcricao_data: dict):
        try:
            transcricao = self.db.query(Transcricoes).get(transcricao_id)
            if not transcricao:
                raise HTTPException(status_code=404, detail="Transcrição não encontrada")
            for key, value in transcricao_data.items():
                setattr(transcricao, key, value)
            self.db.commit()
            self.db.refresh(transcricao)
            return transcricao
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar a transcrição: {str(e)}")

    def getAll(self):
        try:
            return self.db.query(Transcricoes).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar transcrições: {str(e)}")

    def getById(self, transcricao_id: int):
        try:
            transcricao = self.db.query(Transcricoes).get(transcricao_id)
            if not transcricao:
                raise HTTPException(status_code=404, detail="Transcrição não encontrada")
            return transcricao
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar a transcrição: {str(e)}")
