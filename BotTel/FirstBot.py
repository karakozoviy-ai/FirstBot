from BotToken import  BT


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
#Тест
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = BT

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
Calories = False


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        "Привет, данный бот сможет выполнять различные функции, "
        "для более подробного описания нажми команду /help"
    )



# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        "Пока что он может только рассчитывать калории при нажатии на кнопку calories"
    )





# Этот хэндлер будет срабатывать на команду "/calories"
@dp.message(Command(commands='calories'))
async def process_calories_command(message: Message):
    global Calories
    await message.answer("Напиши 4 цифры, через пробел, сначала белки, затем жиры, потом углеводы, потом граммы итогового продукта\n"
    " Я рассчитаю калории на 100 гр продукта\n"
    " Если надо будет выйти из этого режима нажми на кнопку /cancel\n")
    Calories = True

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    global Calories
    Calories = False
    await message.answer("Вы вышли из текущего режима")



# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message()
async def process_answer(message: Message):
    if Calories == True:
        p,f,c,m = map(int,message.text.split())
        await message.answer(f"Итоговая калорийность: {str(((p * 4 + f * 9 + c * 4) * m) / 100)}\n")
        await message.answer(f"Белков:{(p/100)*m}, Жиров{(f/100)*m}, Углеводов{(c/100)*m}")
    else:
        await message.answer('Мы пока что не находимся в режиме команд, выбери команду')



if __name__ == '__main__':
    dp.run_polling(bot)