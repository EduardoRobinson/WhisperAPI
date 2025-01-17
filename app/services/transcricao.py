import openai
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
from pydub import AudioSegment
import whisperx
import tempfile
import os
from faster_whisper import WhisperModel


load_dotenv()

class Transcricao():
    def __init__(self):
        self.resposta = OpenAI()
        self.model=WhisperModel("large-v2")

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
        return result
