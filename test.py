# test_agent.py
import asyncio
from app import agent

async def main():
    response = await agent.run("What does optimizers do")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())