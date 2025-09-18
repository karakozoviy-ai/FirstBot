from BotTel.My_imp import  *
router = Router()
Calories = False
#Выходим из режима
@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    global Calories
    Calories = False
    await message.answer("Вы вышли из текущего режима подсчета калориев")
   # Этот хэндлер будет срабатывать на команду "/calories"
@router.message(Command(commands='calories'))
async def process_calories_command(message: Message):
    global Calories
    await message.answer("Напиши 4 цифры, через пробел, сначала белки, затем жиры, потом углеводы, потом граммы итогового продукта\n"
    " Я рассчитаю калории на 100 гр продукта\n"
    " Если надо будет выйти из этого режима нажми на кнопку /cancel\n")
    Calories = True

#Подсчет калориев
@router.message()
async def process_answer(message: Message):
    if Calories == True:
        try:
            p,f,c,m = map(float,message.text.split())
            await message.answer(f"Итоговая калорийность: {str(((p * 4 + f * 9 + c * 4) * m) / 100)}\n")
            await message.answer(f"Белков: {(p/100)*m}, Жиров: {(f/100)*m}, Углеводов: {(c/100)*m}")
        except:
            await message.answer('Вы ввели, что то не так, если не получается то из режима можно выйти через команду /cancel')

