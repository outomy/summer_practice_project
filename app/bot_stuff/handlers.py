import os
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.types import ContentType

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS

from const import START, HELP

from bot_stuff.tg_bot_keyboard import main_keyboard
from bot_stuff.embed import txt_and_embedding 
from bot_stuff.llm_funcs import chatting
from bot_stuff.bot_memory import (dialog_history_get,
                                dialog_history_write,
                                dialog_history_clear)

router = Router()

# check vector store and load it
if not os.path.exists('D:/coding/!/tg_gigachat_rag/app/faiss_index'):
    txt_and_embedding()

model_name    = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model_kwargs  = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embedding = HuggingFaceEmbeddings(model_name=model_name,
                                model_kwargs=model_kwargs,
                                encode_kwargs=encode_kwargs)

vector_store = FAISS.load_local('app/faiss_index', embeddings=embedding, allow_dangerous_deserialization=True)


# /start and /help
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(START, reply_markup=main_keyboard)

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(HELP)


# bot reboot
@router.message(F.text == 'Перезапустить бота')
async def bot_reboot(message = Message):
    await dialog_history_clear()
    await message.answer('🗑️ История диалога очищена.')


# keyboard things
@router.message(F.text == 'Скачать документы')
async def download_doc(message = Message):

    await message.answer('Вот доступные для скачивания документы:')
    await message.answer_document(document=FSInputFile(
        path='D:/coding/!/tg_gigachat_rag/app/documents/Документация_к_графическому_планшету_Wacom_Intuos_Pro_Paper_Edition.pdf',
        filename='Документация_к_графическому_планшету_Wacom_Intuos_Pro_Paper_Edition.pdf'
    ))
    await message.answer_document(document=FSInputFile(
        path='D:/coding/!/tg_gigachat_rag/app/documents/Каталог_товаров_Elden_Ring.pdf',
        filename='Каталог_товаров_Elden_Ring.pdf'
    ))


# sticker, gif and so on answers
@router.message(F.content_type == ContentType.STICKER)
async def sticker_answer(message: Message):
    await message.answer_sticker(message.sticker.file_id)

@router.message(F.content_type == ContentType.ANIMATION)
async def gif_answer(message: Message):
    await message.answer_sticker(message.animation.file_id)

@router.message(F.content_type == ContentType.PHOTO)
async def gif_answer(message: Message):
    await message.answer('Можешь это распечатать и засунуть себе в зад 😘')

@router.message(F.content_type == ContentType.VOICE)
async def gif_answer(message: Message):
    await message.answer('Я ничего не слышу, сосед сверлит!')

@router.message(F.content_type == ContentType.AUDIO)
async def gif_answer(message: Message):
    await message.answer('Я ничего не слышу, сосед сверлит!')

@router.message(F.content_type == ContentType.DOCUMENT)
async def gif_answer(message: Message):
    await message.answer('Я не буду это окрывать!')


# main dialog
@router.message(F.content_type == ContentType.TEXT)
async def dialog(message: Message):    
    query         = message.text    
    past_requests = await dialog_history_get()
    answer        = await chatting(query, vector_store, past_requests)
    await dialog_history_write(query)
    await message.answer(answer)