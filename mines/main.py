"""
Entry point of the game.
"""

from minesweeper import Minesweeper
import asyncio

async def main():
    game = Minesweeper()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
