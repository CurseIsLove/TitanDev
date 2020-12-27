from . import ping
from naruto import naruto
@naruto.on_message(filters.command(filters.user(AdminSettings) & ("ping", Command))
async def(_, message)
   await ping(_, message)
