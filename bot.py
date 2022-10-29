from aiogram.utils import executor
from create_bot import dp, bot
from handlers import bot_handlers, bot_commands

# bot_commands.register_handlers_bot_commands(dp)
bot_handlers.register_handlers_bot_handlers(dp)

if __name__ == '__main__':
    print('run')
    executor.start_polling(dp, skip_updates=True)
