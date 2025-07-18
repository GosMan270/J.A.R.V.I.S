"""
Список команд для активации модулей.
"""
class CommandMappings:
    def command_map(self):
        COMMAND_MAPPINGS = [
            {
                "examples": ["доброе утро", "с добрым утром", "просыпайся", "новый день", "начинаем день", "включись", "включайся"],
                "function": "new_day"
            },
            {
                "examples": ["открой сайт", "открой в браузере"],
                "function": "open_site"
            },
            {
                "examples": ["какая погода сегодня в ...", "погода в ...", "прогноз погоды в ..."],
                "function": "give_weather"
            }
        ]

        inst_command = (
            "Тебе даны наборы примеров фраз пользователя и соответствующая функция.\n"
            "По смыслу определи, к какой функции ближе запрос пользователя. "
            "Ответ дай строго в формате {def: <function_name>} (например, {def: open_site}), а если не удалось определить — {def: None}.\n"
            "Вот список команд:\n"
        )

        for cmd in COMMAND_MAPPINGS:
            exmpls = "; ".join(cmd["examples"])
            inst_command += f"Фразы: {exmpls} => функция: {cmd['function']}\n"
        inst_command += "Используй только формат {def: <function_name>} или {def: None}."
        return inst_command


CM = CommandMappings()