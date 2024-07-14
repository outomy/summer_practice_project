# https://github.com/ai-forever/gigachain/blob/master/docs/docs/use_cases/question_answering/gigachat_qa.ipynb - Репозиторий с приколами
# https://github.com/trashchenkov/gigachat_tutorials - гайды
# https://github.com/trashchenkov/gigachat_tutorials/blob/main/RAG_%D0%BF%D0%BE_%D1%81%D1%82%D0%B0%D1%82%D1%8C%D1%8F%D0%BC.ipynb

import asyncio

from aiogram import Bot, Dispatcher
from settings import settings

from bot_stuff.handlers import router
from bot_stuff.bot_memory import dialog_history_clear


async def main():
    await dialog_history_clear()

    bot = Bot(token=settings.TG_BOT_TOKEN)
    dp  = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)



try:
    asyncio.run(main())
except:
    print('Ботика убили Х_Х')