import pytest
import pytest_asyncio

import deltachat_rpc_client


@pytest_asyncio.fixture
async def rpc_server():
    return await deltachat_rpc_client.start_rpc_server()


@pytest.mark.asyncio
async def test_system_info(rpc_server):
    system_info = await rpc_server.get_system_info()
    assert "arch" in system_info
    assert "deltachat_core_version" in system_info


@pytest.mark.asyncio
async def test_email_address_validity(rpc_server):
    valid_addresses = [
        "email@example.com",
        "36aa165ae3406424e0c61af17700f397cad3fe8ab83d682d0bddf3338a5dd52e@yggmail@yggmail",
    ]
    invalid_addresses = ["email@", "example.com", "emai221"]

    for addr in valid_addresses:
        assert await rpc_server.check_email_validity(addr)
    for addr in invalid_addresses:
        assert not await rpc_server.check_email_validity(addr)
