from protocol import *

async def main():
    loop = asyncio.get_event_loop()
    proto = Protocol(Earth=True, ports=[5000, 5001,5002,5003])
    cli = ProtocolCLI(loop, proto)

    cli_thread = threading.Thread(target=cli.cmdloop)
    cli_thread.start()

    await proto.run_protocol()

    cli_thread.join()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        logging.info("Cleaning up...")
