import asyncio

from src.bot import TgBot


if __name__ == '__main__':
    try:
        BOT = TgBot()
        asyncio.run(BOT.run())
    except KeyboardInterrupt as e:
        print('Closing...')
        print(f'error as {e}')