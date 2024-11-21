from pycoingecko import CoinGeckoAPI

## As we are using a free API key, we need to change Coingecko API to use non-pro API endpoint
## 'https://api.coingecko.com/api/v3/' with demo API key header 'x-cg-demo-api-key'
client = CoinGeckoAPI(api_key=os.getenv("COINGECKO_API_KEY"), retries=1)


def get_coins(*ids, currency: str = "usd"):
    currency = currency.lower()

    res = []
    for coin in client.get_coins_markets(currency, ids=",".join(ids), per_page=20):
        if not coin["market_cap_rank"]:
            coin["market_cap_rank"] = -1

        res.append({
            "id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "rank": coin["market_cap_rank"],
            "img": coin["image"],
            "url": f'https://www.coingecko.com/en/coins/{coin["id"]}',
            "price": coin["current_price"],
            "price_change": coin["price_change_percentage_24h"],
            "atl": coin["atl"],
            "atl_change": coin["atl_change_percentage"],
            "ath": coin["ath"],
            "ath_change": coin["ath_change_percentage"],
        })

    return res


def search(symbols: set = None, currency: str = "usd") -> list:
    ids = []

    for coin in client.get_coins_list():
        if coin["symbol"] in symbols:
            ids.append(coin["id"])

    return get_coins(*ids, currency=currency)
