from .message import Message


class Chat:
    def __init__(self, rpc, account_id, chat_id):
        self.rpc = rpc
        self.account_id = account_id
        self.chat_id = chat_id

    async def block(self):
        await self.rpc.block_chat(self.account_id, self.chat_id)

    async def accept(self):
        await self.rpc.accept_chat(self.account_id, self.chat_id)

    async def delete(self):
        await self.rpc.delete_chat(self.account_id, self.chat_id)

    async def get_encryption_info(self):
        await self.rpc.get_chat_encryption_info(self.account_id, self.chat_id)

    async def send_text(self, text: str):
        msg_id = await self.rpc.misc_send_text_message(
            self.account_id, self.chat_id, text
        )
        return Message(self.rpc, self.account_id, msg_id)
