from dotenv import load_dotenv
import os


#загрузка конфига
dotenv_path = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    ),
    'run',
    'config.env'
)
load_dotenv(dotenv_path)


def start(message):
    user_id = int(os.getenv('you_telegram_id'))

    res = []

    text = "Добрый день!\n\n"

    if user_id == message.from_user.id:
        text += "Я — создатель этого виртуального ассистента для вашего ПК и умного дома!\n"
        text += "Если этого бота настраивали не вы,\n"
        text += "то вот ссылка на ассистента и бота с инструкцией: \n*GitHub:* [`GosMan270`](https://github.com/GosMan270/J.A.R.V.I.S)\n\n"
        text += "В этом боте реализована лишь малая часть функций моего ассистента.\n"
        text += "Важное уточнение: *без установленного самого ассистента этот бот не будет работать и станет просто пустышкой*.\n"
        text += "Бот нужен скорее для более детального управления и настройки внутренних подсистем.\n\n"
        text += "Удачного использования! ;)"
        access = True

    elif user_id is None:
        text += ("У вас нет доступа к боту! Загляните сюда: \n"
                 "GitHub: https://github.com/GosMan270/J.A.R.V.I.S\n"
                 "и настройте своего J.A.R.V.I.S.\n"
                 "Кстати, там есть подробная инструкция по настройке, архитектуре и т.д.\n"
                 "По вопросам: @GosMan01")
        access = False

    else:
        text += ("У вас нет доступа к боту! Загляните сюда: \n"
                 "GitHub: https://github.com/GosMan270/J.A.R.V.I.S\n"
                 "и настройте своего J.A.R.V.I.S.\n"
                 "Кстати, там есть подробная инструкция по настройке, архитектуре и т.д.\n"
                 "По вопросам: @GosMan01")
        access = False

    res.append(text)
    res.append(access)

    return res