from .rpc import Rpc, start_rpc_server, new_online_account
from .deltachat import Deltachat
from .account import Account


async def main():
    deltachat = start_rpc_server()

    print("System info:", await deltachat.get_system_info())
    account_ids = await deltachat.get_all_account_ids()
    if not account_ids:
        account_id = await deltachat.add_account()
    else:
        account_id = account_ids[0]

    async def event_loop():
        while True:
            notification = await deltachat.get_next_event()
            if not notification:
                break
            account_id = notification["contextId"]
            event = notification["event"]
            if event["type"] == "Info":
                logging.info(event["msg"])
            elif event["type"] == "IncomingMsg":
                await deltachat.accept_chat(account_id, event["chatId"])
                message = await deltachat.message_get_message(
                    account_id, event["msgId"]
                )
                await deltachat.markseen_msgs(account_id, [event["msgId"]])
                await deltachat.misc_send_text_message(
                    account_id, message["text"], event["chatId"]
                )
            else:
                print("Unknown event:", event)
            deltachat.event_queue.task_done()

    event_loop_task = asyncio.create_task(event_loop())

    account_info = await deltachat.get_info(account_id)
    print(account_info)

    if not await deltachat.is_configured(account_id):
        print("Account is not configured, configuring")
        await deltachat.set_config(account_id, "addr", "address")
        await deltachat.set_config(account_id, "mail_pw", "password")
        await deltachat.configure(account_id)
        print("Configured")
    else:
        await deltachat.start_io(account_id)

    await event_loop_task


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
