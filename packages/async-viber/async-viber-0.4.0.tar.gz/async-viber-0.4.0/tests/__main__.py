from viber import dp, Message, run


@dp.message_handler(text="1")
async def _(msg: Message):
    await msg.answer("1")


run()
