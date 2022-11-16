import asyncio
import json
import logging
import os

import aiohttp


class JsonRpcError(Exception):
    pass


class Rpc:
    def __init__(self, process):
        self.process = process
        self.event_queues = {}
        self.id = 0
        self.reader_task = asyncio.create_task(self.reader_loop())

        # Map from request ID to `asyncio.Future` returning the response.
        self.request_events = {}

    async def reader_loop(self):
        while True:
            line = await self.process.stdout.readline()
            response = json.loads(line)
            if "id" in response:
                fut = self.request_events.pop(response["id"])
                fut.set_result(response)
            elif response["method"] == "event":
                # An event notification.
                params = response["params"]
                account_id = params["contextId"]
                if account_id not in self.event_queues:
                    self.event_queues[account_id] = asyncio.Queue()
                await self.event_queues[account_id].put(params["event"])
            else:
                print(response)

    async def get_next_event(self, account_id):
        """Returns next event."""
        if account_id in self.event_queues:
            return await self.event_queues[account_id].get()

    def __getattr__(self, attr):
        async def method(*args, **kwargs):
            self.id += 1
            request_id = self.id

            params = args
            if kwargs:
                assert not args
                params = kwargs

            request = {
                "jsonrpc": "2.0",
                "method": attr,
                "params": params,
                "id": self.id,
            }
            data = (json.dumps(request) + "\n").encode()
            self.process.stdin.write(data)
            event = asyncio.Event()
            loop = asyncio.get_running_loop()
            fut = loop.create_future()
            self.request_events[request_id] = fut
            response = await fut
            if "error" in response:
                raise JsonRpcError(response["error"])
            if "result" in response:
                return response["result"]

        return method


async def start_rpc_server(*args, **kwargs):
    proc = await asyncio.create_subprocess_exec(
        "deltachat-rpc-server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        *args,
        **kwargs
    )
    rpc = Rpc(proc)
    return rpc


async def new_online_account():
    url = os.getenv("DCC_NEW_TMP_EMAIL")
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return json.loads(await response.text())
