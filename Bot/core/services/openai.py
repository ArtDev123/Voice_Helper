from openai import AsyncOpenAI, AsyncAssistantEventHandler
import asyncio
from ..settings import settings

class OpenaiService:

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    assistant_id = settings.assistant_id

    @classmethod
    async def create_assistant(cls):
        assistant = await cls.client.beta.assistants.create(
            name="Artem",
            instructions="You are a professional lingvist",
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo",
        )
        return assistant.id
    
    @classmethod
    async def voice_to_text(cls, file_path):
        with open(file_path, 'rb') as file:
            transcription = await cls.client.audio.transcriptions.create(
                model="whisper-1", file=file)
        return transcription.text
    
    @classmethod
    async def text_to_speech(cls, text, file_path) -> bytes:
        max_input_len = 4096
        text = text[:max_input_len]
        response = await cls.client.audio.speech.create(
            model="tts-1",voice="alloy", input=text
        )
        response.stream_to_file(file=file_path)
    
    @classmethod
    async def submit_message(cls, thread_id, content):
        await cls.client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=content
    )
        return await cls.client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=cls.assistant_id,
    )
    
    @classmethod
    async def create_thread_and_run(cls,user_input):
        thread = await cls.client.beta.threads.create()
        run = await cls.submit_message(thread.id, user_input)
        return thread, run
    
    @classmethod
    async def wait_on_run(cls, run, thread_id):
        while run.status == "queued" or run.status == "in_progress":
            run = await cls.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            await asyncio.sleep(0.5)
        return run

    @classmethod
    async def get_response(cls,thread_id):
        return await cls.client.beta.threads.messages.list(thread_id=thread_id, order="asc")
    
