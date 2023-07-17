from bot import bot
from handlers import *

Commands.handler()
Menu.handler()
CheckUser.handler()
AdminAndUserLib.handler()
Upload.handler()
CreateDoc.handler()
Messages.handler()

if __name__ == '__main__':
    bot.polling(non_stop=True)
