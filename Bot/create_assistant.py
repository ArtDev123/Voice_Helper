from core.services.openai import OpenaiService
import asyncio

async def create():
    assistant = await OpenaiService.create_assistant()
    print(assistant)

asyncio.run(create())