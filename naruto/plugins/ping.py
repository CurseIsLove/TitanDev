@naruto.on_message(filters.command(filters.user(AdminSettings) & ("ping", Command))
async def_(_, messages)
   await ping(_, messages)
