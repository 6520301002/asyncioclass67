import asyncio
import httpx
import time

async def fetch_pokemon_names(ability_name, ability_url):
    start_time = time.time()  # เริ่มจับเวลา
    async with httpx.AsyncClient() as client:
        response = await client.get(ability_url)
        data = response.json()
        pokemon_names = [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
    elapsed_time = time.time() - start_time  # คำนวณเวลาที่ใช้
    return ability_name, pokemon_names, elapsed_time

async def main():
    urls = {
        "battle-armor": "https://pokeapi.co/api/v2/ability/battle-armor",
        "speed-boost": "https://pokeapi.co/api/v2/ability/speed-boost"
    }
    
    # สร้าง tasks สำหรับดึงข้อมูลและจับเวลา
    tasks = {ability: fetch_pokemon_names(ability, url) for ability, url in urls.items()}
    
    # รอให้ tasks เสร็จสิ้นและรวบรวมผลลัพธ์
    results = await asyncio.gather(*tasks.values())
    
    # แสดงผลลัพธ์
    for ability_name, pokemon_names, elapsed_time in results:
        print(f"Pokémon with '{ability_name}' ability:")
        for name in pokemon_names:
            print(f"- {name}")
        print(f"Time taken for '{ability_name}': {elapsed_time:.2f} seconds")
        print()  # เพิ่มบรรทัดว่างระหว่างความสามารถ

# เริ่มต้นและรันโปรแกรม
asyncio.run(main())
