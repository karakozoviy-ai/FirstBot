from BotTel.My_imp import *

Calories = False


router = Router()
# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        "Привет, данный бот сможет выполнять различные функции, "
        "для более подробного описания нажми команду /help"

    )


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        "Пока что он может только рассчитывать калории при нажатии на кнопку calories"
    )


