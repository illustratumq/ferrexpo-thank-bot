from aiogram import Dispatcher
from app.handlers.private import start, authorization, send, rating, menu, nonstate, myhistory
from app.handlers.admin import users, statistic


def setup(dp: Dispatcher):
    statistic.setup(dp)
    start.setup(dp)
    authorization.setup(dp)
    menu.setup(dp)
    rating.setup(dp)
    send.setup(dp)
    users.setup(dp)
    myhistory.setup(dp)
    # last setup
    nonstate.setup(dp)



