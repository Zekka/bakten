try:
    import addrefs
    import bot
    bot.main()
except Exception, e:
    import traceback
    traceback.print_exc()

