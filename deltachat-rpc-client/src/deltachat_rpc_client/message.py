class Message:
    def __init__(self, rpc, account_id, msg_id):
        self.rpc = rpc
        self.account_id = account_id
        self.msg_id = msg_id

    async def send_reaction(self, reactions):
        msg_id = await self.rpc.send_reaction(self.account_id, self.msg_id, reactions)
        return Message(self.rpc, self.account_id, msg_id)
