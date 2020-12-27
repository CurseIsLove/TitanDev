from . import ping
@naruto.on_message(filters.command(filters.user(AdminSettings) & ("ping", Command))
async def _(_, message)
   await ping(_, message)
