from core.services.openai import OpenaiService
import asyncio

async def create():
    assistant = await OpenaiService.create_assistant()
    print(assistant)

if __name__ == "__main__":
    asyncio.run(create())