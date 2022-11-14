import asyncio
import aiohttp
import json
import logging
import os


class JsonRpcError(Exception):
    pass


class Rpc:
    def __init__(self, process):
        self.process = process
        self.event_queue = asyncio.Queue()
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
            else:
                if response["method"] == "event":
                    # An event notification.
                    await self.event_queue.put(response["params"]["event"])

    async def get_next_event(self):
        """Returns next event."""
        return await self.event_queue.get()

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


async def start_rpc_server():
    proc = await asyncio.create_subprocess_exec(
        "deltachat-rpc-server",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    rpc = Rpc(proc)
    return rpc


async def new_online_account():
    url = os.getenv("DCC_NEW_TMP_EMAIL")
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return json.loads(await response.text())
