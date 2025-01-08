import openai
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment


load_dotenv()

class Transcricao():
    def __init__(self):
        self.resposta = OpenAI()

    async def transcrever(self,arquivo):
       
       audio = await arquivo.read()
       buffer=BytesIO(audio)
       buffer.name=arquivo.filename
    
       texto=self.resposta.audio.transcriptions.create(
            model="whisper-1",file=buffer
            )
       
       return texto