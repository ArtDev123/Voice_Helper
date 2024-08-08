from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import FSInputFile

from ..utils.files import download_voice, remove_file
from ..create_bot import bot
from ..services.openai import OpenaiService
from ..keyboards.voice_kb import get_voice_kb
from ..keyboards.tts_kb import get_tts_kb
from ..utils.statesform import StepsForm

router = Router()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    thread, run = await OpenaiService.create_thread_and_run("Hello")
    await state.update_data(thread = thread.id)
    await message.answer('Hello! this is a voice GPT bot. \nYou can send voice messages and get voice answers.')

@router.message(Command("newthread"))
async def start(message: Message, state: FSMContext):
    thread, run = await OpenaiService.create_thread_and_run("Hello")
    await state.update_data(thread = thread.id)
    await message.answer('New threade activated')

@router.message(F.voice)
async def voice(message: Message, state: FSMContext):
    try:
        file_path = await download_voice(message, bot)
        text = await OpenaiService.voice_to_text(file_path)
        await state.update_data(text = text)
        await message.answer(text="Choose action:", reply_markup=get_voice_kb())
        await state.set_state(StepsForm.CHOOSE_ACTION)
    finally:
        remove_file(file_path)

@router.callback_query(F.data == "answer", StepsForm.CHOOSE_ACTION)
async def answer(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    text = user_data['text']
    thread_id = user_data['thread']
    #run = user_data.get('run')
    run = await OpenaiService.submit_message(thread_id, text)
    run = await OpenaiService.wait_on_run(run, thread_id)
    answer = await OpenaiService.get_response(thread_id)
    answer_text = answer.data[-1].content[0].text.value
    await state.update_data(answer = answer_text)
    await callback.message.answer(f"{answer_text}", reply_markup=get_tts_kb())

@router.callback_query(F.data == "text", StepsForm.CHOOSE_ACTION)
async def get_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    text = user_data['text']
    await callback.message.answer(f"{text}")

@router.callback_query(F.data == "voice")
async def voice(callback: CallbackQuery, state: FSMContext):
    try:
        user_data = await state.get_data()
        answer = user_data['answer']
        file_path = f'core/media/audio_answer.mp3'
        await OpenaiService.text_to_speech(answer, file_path)
        audio = FSInputFile(file_path)
        await callback.message.answer_voice(voice=audio)
    finally:
        remove_file(file_path)


@router.message()
async def incorrect(message: Message):
    await message.answer("Incorrect Message, only voice")