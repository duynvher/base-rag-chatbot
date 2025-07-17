import chainlit
from demo.client import Client

client = Client()


@chainlit.on_message
async def main(message: chainlit.Message):
    msg = await chainlit.Message(content="").send()

    user = chainlit.user_session.get("user")
    thread_id = chainlit.context.session.thread_id

    async for token in client.call(
            query=message.content,
            user_id=user,
            thread_id=thread_id,

    ):
        await msg.stream_token(token["content"])

    await msg.update()
