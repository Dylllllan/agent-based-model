import asyncio

TOTAL_PLAYERS = 50
BATCH_SIZE = 50

BATCHES = TOTAL_PLAYERS // BATCH_SIZE


async def runAgentClient(index):
    # Wait an amount of time to reduce load on the server
    await asyncio.sleep(0.1 * index)

    # Run the Main.py program with the given index
    process = await asyncio.create_subprocess_exec(
        "python", "Main.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    print("Running agent", index)

    # Wait for the program to complete
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=90)
        # If stdout contains "Network error", output that this has occurred, otherwise say it ran successfully
        if "Network error" in stdout.decode():
            print("Network error occurred for agent", index)
        else:
            print("Agent", index, "finished running")
    except asyncio.TimeoutError:
        # If the program takes too long to complete, output that it has timed out
        print("Agent", index, "timed out")
        # Terminate the process
        process.terminate()


async def start():
    for i in range(BATCHES):
        print("Starting batch", i + 1)
        # Run the main program for each agent client
        await asyncio.gather(*[runAgentClient(index) for index in range(BATCH_SIZE)])
        print("Batch", i + 1, "complete")


if __name__ == "__main__":
    # Run the start function using asyncio
    asyncio.run(start())
