"""Main entry point for the bot."""

import asyncio


async def main() -> None:
    """Main function to run the bot."""
    print("Running bot...")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
