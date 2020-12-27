@naruto.on_message(filters.command(filters.user(AdminSettings) & ("ping", Command))
async def _(_, messages)
   await ping(_, messages)
