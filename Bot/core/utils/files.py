import os

async def download_voice(message, bot):
    file_id = message.voice.file_id  
    file = await bot.get_file(file_id)  
    file_path = file.file_path
    file_name = f"core/media/audio{file_id}.mp3"
    await bot.download_file(file_path, file_name)
    return file_name

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)
    