from app.db.models import Transcricoes
from app.db.repository import TranscricoesRepository
import openai
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment
import whisperx
import tempfile
import os
from faster_whisper import WhisperModel
import torch
import transformers
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

class Transcricao():
    def __init__(self,db):
        self.db=db
        self.resposta = OpenAI()
        self.model=WhisperModel("large-v2")
        self.llm = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            temperature=0.5,
            return_full_text=True
    )
        self.question="Gostaria de um relatorio com dados sobre as possiveis causas, possiveis agente envolvidos e tambem sobre as emoções envolvidas no seguinte texto:"
        self.prompt=''
    async def transcrever(self,arquivo):
       
       audio = await arquivo.read()
       buffer=BytesIO(audio)
       buffer.name=arquivo.filename
    
       texto=self.resposta.audio.transcriptions.create(
            model="whisper-1",file=buffer
            )
       return texto
    

    async def transcrever2(self, arquivo):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
            temp_file.write(await arquivo.read())  # Ler o conteúdo do arquivo e salvar
            temp_path = temp_file.name
        print(f"Arquivo temporário criado em: {temp_path}")

        # Verifique se o arquivo temporário existe
        if not os.path.exists(temp_path):
            raise FileNotFoundError(f"Arquivo temporário não encontrado: {temp_path}")
       
        try:
            audio = whisperx.load_audio(temp_path)
        except FileNotFoundError as e:
            raise FileNotFoundError("Certifique-se de que o FFmpeg está instalado e no PATH do sistema.") from e

        result = self.model.transcribe(audio)
        updated_first_element = [item.__dict__ for item in result[0]]
        result = (updated_first_element, *result[1:])
        model_a, metadata = whisperx.load_align_model(language_code=result[1].language, device="cuda")
        result = whisperx.align(list(result[0]), model_a, metadata, audio, "cuda", return_char_alignments=False)
        result = await self.resume(result)
        return result
        
    


    async def resume(self,result):
        text=[]
        for item in result["segments"]:
            text.append(item["text"])
        string=" ".join(text)
        self.question= self.question + string
        self.prompt = PromptTemplate.from_template(self.question)
        chain = self.prompt | self.llm | StrOutputParser()
        response=chain.invoke({"question":self.question, "language": "pt","chat_history":[]})
        transcricao=Transcricoes(description=string,resume=response,segments=len(result["segments"]))
        transcricaoRepository=TranscricoesRepository(self.db)
        transcription=transcricaoRepository.create(transcricao)
        return transcription
        



