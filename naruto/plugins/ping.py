import time
from naruto import naruto

@naruto.on_message(filters.command(filters.user(AdminSettings) & ("ping", Command))
