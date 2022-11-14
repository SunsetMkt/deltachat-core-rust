from typing import Optional


class Account:
    def __init__(self, rpc, id):
        self.id = id
        self.rpc = rpc

    async def remove(self) -> None:
        await self.rpc.remove_account(self.id)

    async def start_io(self) -> None:
        await self.rpc.start_io(self.id)

    async def stop_io(self) -> None:
        await self.rpc.stop_io(self.id)

    async def get_info(self):
        return await self.rpc.get_info(self.id)

    async def get_file_size(self):
        return await self.rpc.get_account_file_size(self.id)

    async def is_configured(self) -> bool:
        return await self.rpc.is_configured(self.id)

    async def set_config(key: str, value: Optional[str]):
        await self.rpc.set_config(self.id, key, value)

    async def get_config(key: str) -> Optional[str]:
        return await self.rpc.get_config(self.id, key)
