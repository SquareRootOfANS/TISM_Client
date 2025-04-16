import requests
import json
import os
from datetime import datetime
from urllib.parse import quote

CACHE_FILE = "data/last_successful_fetch.json"

ESTIMATED_SELL_PRICES = {

}

def fetch_enriched_uex_data():
    print("[DEBUG] Fetching prices from UEX...")

    try:
        response = requests.get("https://api.uexcorp.space/2.0/commodities", timeout=10)
        response.raise_for_status()
        price_data = response.json().get("data", [])
        print("[DEBUG] Raw UEX entry sample:", price_data[0] if price_data else "Empty")
        print(f"[DEBUG] UEX returned {len(price_data)} entries.")
    except Exception as e:
        print(f"[API ERROR] UEX fetch failed: {e}")
        return []

    print("[DEBUG] Fetching locations from SC Trade Tools...")
    try:
        loc_response = requests.get("https://sc-trade.tools/api/locations")
        loc_response.raise_for_status()
        sc_locations = loc_response.json()
    except Exception as e:
        print(f"[API ERROR] Location fetch failed: {e}")
        sc_locations = []

    location_lookup = {}
    for loc in sc_locations:
        full_path = " > ".join(filter(None, [
            loc.get("system"), loc.get("jurisdiction"), loc.get("planet"), loc.get("name")
        ]))
        location_lookup[loc["name"].strip().lower()] = full_path
    print("[DEBUG] Location lookup keys (sample):", list(location_lookup.keys())[:10])

    enriched_data = []
    for entry in price_data:
        location = entry.get("location", "").strip().lower()
        print(f"[DEBUG] Enriching '{location}' →", location_lookup.get(location, "NOT FOUND"))
        entry["path"] = location_lookup.get(location, "Unknown")
        enriched_data.append(entry)

    print("[DEBUG] Enriched entry sample:", enriched_data[0] if enriched_data else "No data")
    return enriched_data

def fetch_all_locations():
    url = "https://sc-trade.tools/api/locations"
    headers = { "User-Agent": "Mozilla/5.0" }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        locations = [entry["name"] for entry in data if " > " in entry["name"]]
        print(f"[DEBUG] Fetched {len(locations)} locations.")
        return locations

    except Exception as e:
        print(f"[API ERROR] Failed to fetch locations: {e}")
        return []

def fetch_commodity_prices():
    print("[DEBUG] Loading commodity data from UEX new API...")

    try:
        url = "https://api.uexcorp.space/2.0/commodities_prices_all"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        all_data = response.json().get("data", [])

        print(f"[DEBUG] UEX returned {len(all_data)} entries.")

        grouped = {}
        for entry in all_data:
            name = entry.get("commodity_name")
            location = entry.get("terminal_name")
            price_buy = entry.get("price_buy")
            price_sell = entry.get("price_sell")

            if not name:
                continue

            if name not in grouped:
                grouped[name] = []

            if price_buy:
                grouped[name].append({
                    "location": location,
                    "path": location,
                    "type": "buy",
                    "price": price_buy
                })

            if price_sell:
                grouped[name].append({
                    "location": location,
                    "path": location,
                    "type": "sell",
                    "price": price_sell
                })

        enriched = [{"name": name, "locations": locs} for name, locs in grouped.items()]

        # Save to cache
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"timestamp": datetime.utcnow().isoformat(), "commodities": enriched}, f)

        return enriched, None

    except Exception as e:
        print(f"[API ERROR] UEX fetch failed: {e}")

        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                print("[DEBUG] Using fallback cached data.")
                return cached.get("commodities", []), cached.get("timestamp")

        print("[DEBUG] Using hardcoded fallback data.")
        return [
            {
                "name": "Laranite",
                "locations": [
                    {"location": "Lorville", "path": "Stanton > Hurston > Lorville", "type": "buy", "price": 2022},
                    {"location": "Area18", "path": "Stanton > ArcCorp > Area18", "type": "sell", "price": 2375}
                ]
            }
        ], "mock"