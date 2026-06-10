# Changelog

## 2.0.0 - 2026-06-10

### Changed (8)

- Renamed `get_hot_tokens()` to `get_hot_token_list()`
- Renamed `get_price()` to `get_token_price()`
- Renamed `get_price_info()` to `get_token_trading_info()`
- Renamed `search_tokens()` to `search_token()`
- - Modified response for `get_candles()` (`GET /api/v1/dex/market/candles`):
  - `data`.items.items: type `string` → `number`
- Modified response for `get_hot_token_list()` (`GET /api/v1/dex/market/token/hot-token`):
  - `data`.`items`.items: property `riskLevel` deleted
  - `data`.`items`.items: item property `riskLevel` deleted

## 1.0.0 - 2026-06-09

- Initial release
