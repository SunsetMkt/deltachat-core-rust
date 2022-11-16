from typing import Optional

from .contact import Contact


class Account:
    def __init__(self, rpc, account_id):
        self.rpc = rpc
        self.account_id = account_id

    async def get_next_event(self):
        return await self.rpc.get_next_event(self.account_id)

    async def remove(self) -> None:
        await self.rpc.remove_account(self.account_id)

    async def start_io(self) -> None:
        await self.rpc.start_io(self.account_id)

    async def stop_io(self) -> None:
        await self.rpc.stop_io(self.account_id)

    async def get_info(self):
        return await self.rpc.get_info(self.account_id)

    async def get_file_size(self):
        return await self.rpc.get_account_file_size(self.account_id)

    async def is_configured(self) -> bool:
        return await self.rpc.is_configured(self.account_id)

    async def set_config(self, key: str, value: Optional[str]):
        await self.rpc.set_config(self.account_id, key, value)

    async def get_config(self, key: str) -> Optional[str]:
        return await self.rpc.get_config(self.account_id, key)

    async def configure(self):
        await self.rpc.configure(self.account_id)

    async def create_contact(self, email: str, name: Optional[str]):
        return Contact(
            self.rpc,
            self.account_id,
            await self.rpc.create_contact(self.account_id, email, name),
        )
