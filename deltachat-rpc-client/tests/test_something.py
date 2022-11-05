import pytest

import deltachat_rpc_client

@pytest.mark.asyncio
async def test_system_info():
    rpc_server = await deltachat_rpc_client.start_rpc_server()
    assert rpc_server

    system_info = await rpc_server.get_system_info()
    assert "arch" in system_info
    assert "deltachat_core_version" in system_info
