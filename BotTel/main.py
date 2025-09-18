from My_imp import *
from Handler import Calories,CommonComand,Weather

async def main():
    BOT_TOKEN = BT
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    #Здесь подключаем все наши роутеры
    dp.include_router(Weather.router)
    dp.include_router(CommonComand.router)
    dp.include_router(Calories.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
