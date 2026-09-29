import asyncio, httpx

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as c:
        for _ in range(20):
            r = await c.get("/health")
            print(r.status_code, r.json())
if __name__ == "__main__":
    asyncio.run(main())
