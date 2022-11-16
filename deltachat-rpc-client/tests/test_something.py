import pytest
import pytest_asyncio

import deltachat_rpc_client
from deltachat_rpc_client import Deltachat


@pytest_asyncio.fixture
async def rpc():
    return await deltachat_rpc_client.start_rpc_server()


@pytest.mark.asyncio
async def test_system_info(rpc):
    system_info = await rpc.get_system_info()
    assert "arch" in system_info
    assert "deltachat_core_version" in system_info


@pytest.mark.asyncio
async def test_email_address_validity(rpc):
    valid_addresses = [
        "email@example.com",
        "36aa165ae3406424e0c61af17700f397cad3fe8ab83d682d0bddf3338a5dd52e@yggmail@yggmail",
    ]
    invalid_addresses = ["email@", "example.com", "emai221"]

    for addr in valid_addresses:
        assert await rpc.check_email_validity(addr)
    for addr in invalid_addresses:
        assert not await rpc.check_email_validity(addr)

@pytest.mark.asyncio
async def test_online_account(rpc):
    account_json = await deltachat_rpc_client.new_online_account()

    account_id = await rpc.add_account()
    await rpc.set_config(account_id, "addr", account_json["email"])
    await rpc.set_config(account_id, "mail_pw", account_json["password"])

    await rpc.configure(account_id)
    while True:
        event = await rpc.get_next_event()
        if event["type"] == "ConfigureProgress":
            # Progress 0 indicates error.
            assert event["progress"] != 0

            if event["progress"] == 1000:
                # Success.
                break
        else:
            print(event)
    print("Successful configuration")


@pytest.mark.asyncio
async def test_online_account(rpc):
    deltachat = Deltachat(rpc)
    account = await deltachat.add_account()
    assert not await account.is_configured()
    info = await account.get_info()
    print(info)
