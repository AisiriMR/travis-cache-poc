import json
import time
import redis

# Connect to Redis on your laptop
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Load the fake products (our "fake Supabase")
with open("products.json") as f:
    products = json.load(f)

ONE_WEEK = 7 * 24 * 60 * 60  # seconds


def search_boots(color, max_price):
    key = f"boots:{color}:under:{max_price}"
    start = time.perf_counter()

    # 1. Check the cache first
    saved = r.get(key)
    if saved:
        results = json.loads(saved)
        took = (time.perf_counter() - start) * 1000
        print(f"\n✅ CACHE HIT  ({took:.2f} ms)  key = {key}")
        return results

    # 2. Not in cache: do the "slow work"
    print(f"\n❌ CACHE MISS  key = {key}")
    print("   Searching products and pretending the AI is thinking...")
    time.sleep(2)  # pretend this is the slow, expensive AI

    results = [
        p for p in products
        if p["color"] == color and p["price"] <= max_price
    ]

    # 3. Save the answer in Redis, auto-delete after one week
    r.set(key, json.dumps(results), ex=ONE_WEEK)
    took = (time.perf_counter() - start) * 1000
    print(f"   Saved to cache ({took:.0f} ms)")
    return results


while True:
    color = input("\nColor (or 'quit'): ").strip().lower()
    if color == "quit":
        break
    max_price = int(input("Max price: $").strip())

    for boot in search_boots(color, max_price):
        print(f"   - {boot['name']}: ${boot['price']}")