#!/usr/bin/env python3
import asyncio
import logging
import sys

import deltachat_rpc_client as dc


async def main():
    rpc = await dc.start_rpc_server()
    deltachat = dc.Deltachat(rpc)
    system_info = await deltachat.get_system_info()
    logging.info("Running deltachat core %s", system_info["deltachat_core_version"])

    accounts = await deltachat.get_all_accounts()
    if not accounts:
        account = await deltachat.add_account()
    else:
        account = accounts[0]

    print(account)
    account_info = await account.get_info()
    print(account_info)

    await account.set_config("bot", "1")
    if not await account.is_configured():
        logging.info("Account is not configured, configuring")
        await account.set_config("addr", sys.argv[1])
        await account.set_config("mail_pw", sys.argv[2])
        await account.configure()
        logging.info("Configured")
    else:
        await deltachat.start_io()

    while True:
        event = await account.get_next_event()
        if event["type"] == "Info":
            logging.info(event["msg"])
        elif event["type"] == "IncomingMsg":
            print("Got a message")
            message = await rpc.get_message(account.account_id, event["msgId"])
            await rpc.markseen_msgs(account.account_id, [event["msgId"]])
            await rpc.misc_send_text_message(
                account.account_id, event["chatId"], message["text"]
            )

    await event_loop_task


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
