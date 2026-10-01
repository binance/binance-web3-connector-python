# Changelog

## 8.0.0 - 2026-10-01

### Changed (220)

#### REST API

- Modified response for `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`):
  - property `status` added
  - property `sub_data` added
  - property `type` added
  - property `code` added
  - property `data` added
  - property `error_data` added
  - property `params` added
  - oneOf removed 2 schema(s)

- Modified response for `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`):
  - property `type` added
  - property `code` added
  - property `data` added
  - property `error_data` added
  - property `params` added
  - property `status` added
  - property `sub_data` added
  - oneOf removed 2 schema(s)

- Modified response for `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`):
  - property `error_data` added
  - property `params` added
  - property `status` added
  - property `sub_data` added
  - property `type` added
  - property `code` added
  - property `data` added
  - oneOf removed 2 schema(s)

- Modified response for `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`):
  - property `code` added
  - property `data` added
  - property `error_data` added
  - property `params` added
  - property `status` added
  - property `sub_data` added
  - property `type` added
  - oneOf removed 2 schema(s)

- Modified response for `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`):
  - property `error_data` added
  - property `params` added
  - property `status` added
  - property `sub_data` added
  - property `type` added
  - property `code` added
  - property `data` added
  - oneOf removed 2 schema(s)

- Added response field `status`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Added response field `sub_data`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Added response field `type`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Added response field `code`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Added response field `data`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Added response field `error_data`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Added response field `params`
  - affected methods:
    - `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
    - `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
    - `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
    - `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
    - `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- Removed response schema `GetBroadcastOrdersResponse401`
- Removed response schema `GetTransactionsByAddressResponse401`
- Removed response schema `GetRfqOrderStatusResponse403`
- Removed response schema `ListDeFiProtocolsResponse403`
- Removed response schema `GetRwaTokenListResponse404`
- Removed response schema `GetCandlesResponse403`
- Removed response schema `GetTokenBalancesByAddressResponse403`
- Removed response schema `GetTopTradersResponse403`
- Removed response schema `GetTokenBalancesByAddressResponse401`
- Removed response schema `GetTokenDevInfoResponse403`
- Removed response schema `BuildDeFiClaimTransactionResponse404`
- Removed response schema `GetAddressPortfolioOverviewResponse403`
- Removed response schema `GetGasPriceResponse403`
- Removed response schema `GetB402SupportedConfigurationsV1Response401`
- Removed response schema `GetHotTokenListResponse404`
- Removed response schema `GetB402SupportedConfigurationsV1Response1`
- Removed response schema `GetAddressRecentPnLResponse404`
- Removed response schema `GetAllTokenBalancesByAddressResponse404`
- Removed response schema `GetB402SupportedConfigurationsV2Response2`
- Removed response schema `GetTokenBasicInfoResponse404`
- Removed response schema `GetRwaTokenIssuancePlatformsResponse404`
- Removed response schema `GetRwaTokenPriceResponse403`
- Removed response schema `GetAddressPnLForSpecificTokenResponse401`
- Removed response schema `GetTransactionDetailByHashResponse401`
- Removed response schema `GetBroadcastOrdersResponse403`
- Removed response schema `GetTrackedTradesResponse401`
- Removed response schema `GetAggregatedQuoteResponse401`
- Removed response schema `QuoteAndBuildSwapTransactionResponse401`
- Removed response schema `ListDeFiProtocolsResponse401`
- Removed response schema `GetAddressRecentPnLResponse401`
- Removed response schema `GetProtocolDetailResponse401`
- Removed response schema `BuildSwapTransactionResponse401`
- Removed response schema `GetErc20ApproveTransactionResponse404`
- Removed response schema `GetTokenBasicInfoResponse401`
- Removed response schema `BuildDeFiClaimTransactionResponse401`
- Removed response schema `GetTokenTradesResponse401`
- Removed response schema `SubmitRfqOrderResponse401`
- Removed response schema `SettleB402PaymentV2Response1`
- Removed response schema `GetRfqOrderStatusResponse404`
- Removed response schema `BuildDeFiDepositTransactionResponse401`
- Removed response schema `BuildDeFiClaimTransactionResponse403`
- Removed response schema `GetPortfolioSupportedChainsResponse401`
- Removed response schema `GetTransactionsByAddressResponse403`
- Removed response schema `GetAggregatorSupportedChainsResponse401`
- Removed response schema `GetAddressPortfolioOverviewResponse404`
- Removed response schema `ListDeFiInvestmentsResponse404`
- Removed response schema `GetTokenTradingInfoResponse401`
- Removed response schema `CalculateLpAddPairedAmountsResponse403`
- Removed response schema `GetTrackedTradesResponse404`
- Removed response schema `GetAggregatorSupportedChainsResponse403`
- Removed response schema `SearchTokenResponse403`
- Removed response schema `CalculateLpAddPairedAmountsResponse401`
- Removed response schema `GetTokenAdvancedInfoResponse404`
- Removed response schema `GetTokenTradesResponse404`
- Removed response schema `GetTokenDevInfoResponse401`
- Removed response schema `GetRwaTokenIssuancePlatformsResponse401`
- Removed response schema `GetRwaUnderlyingMarketDataResponse404`
- Removed response schema `BuildDeFiDepositTransactionResponse403`
- Removed response schema `GetLatestBlockHeightResponse404`
- Removed response schema `GetB402SupportedConfigurationsV2Response1`
- Removed response schema `GetTokenPriceResponse401`
- Removed response schema `GetGasPriceResponse404`
- Removed response schema `GetAggregatorSupportedChainsResponse404`
- Removed response schema `GetHoldersRankingResponse404`
- Removed response schema `GetHoldersRankingResponse401`
- Removed response schema `BuildLpAddTransactionResponse403`
- Removed response schema `GetCandlesResponse401`
- Removed response schema `GetTokenTradingInfoResponse404`
- Removed response schema `GetSupportedChainsResponse401`
- Removed response schema `GetAddressPnLForSpecificTokenResponse404`
- Removed response schema `BuildLpRemoveTransactionResponse404`
- Removed response schema `SettleB402PaymentV1Response403`
- Removed response schema `BuildLpRemoveTransactionResponse403`
- Removed response schema `GetB402SupportedConfigurationsV2Response429`
- Removed response schema `VerifyB402PaymentV2Response2`
- Removed response schema `VerifyB402PaymentV1Response403`
- Removed response schema `QuoteAndBuildSwapTransactionResponse404`
- Removed response schema `BuildLpAddTransactionResponse401`
- Removed response schema `GetDeFiPositionsResponse401`
- Removed response schema `BuildSwapTransactionResponse403`
- Removed response schema `VerifyB402PaymentV2Response403`
- Removed response schema `GetPortfolioSupportedChainsResponse404`
- Removed response schema `GetRwaTokenPriceResponse404`
- Removed response schema `GetTokenBalancesByAddressResponse404`
- Removed response schema `CalculateLpAddPairedAmountsResponse404`
- Removed response schema `GetB402SupportedConfigurationsV2Response401`
- Removed response schema `GetTransactionStatusResponse401`
- Removed response schema `GetAggregatedQuoteResponse403`
- Removed response schema `SearchTokenResponse401`
- Removed response schema `GetTransactionStatusResponse403`
- Removed response schema `SimulateTransactionsResponse403`
- Removed response schema `GetInvestmentDetailResponse403`
- Removed response schema `SearchTokenResponse404`
- Removed response schema `BuildSolanaSwapInstructionsResponse403`
- Removed response schema `SettleB402PaymentV2Response403`
- Removed response schema `BuildSolanaSwapInstructionsResponse404`
- Removed response schema `BuildDeFiRedeemTransactionResponse404`
- Removed response schema `GetHoldersRankingResponse403`
- Removed response schema `GetB402SupportedConfigurationsV1Response503`
- Removed response schema `GetTokenDevInfoResponse404`
- Removed response schema `SimulateTransactionsResponse404`
- Removed response schema `GetRwaUnderlyingInfoResponse401`
- Removed response schema `GetTrackedTradesResponse403`
- Removed response schema `BroadcastTransactionsResponse403`
- Removed response schema `GetTransactionDetailByHashResponse404`
- Removed response schema `GetB402SupportedConfigurationsV1Response429`
- Removed response schema `GetRwaUnderlyingInfoResponse404`
- Removed response schema `GetWalletSupportedChainsResponse403`
- Removed response schema `GetRfqOrderStatusResponse401`
- Removed response schema `GetAddressRecentPnLResponse403`
- Removed response schema `GetRwaUnderlyingMarketDataResponse403`
- Removed response schema `BuildDeFiRedeemTransactionResponse401`
- Removed response schema `BuildLpAddTransactionResponse404`
- Removed response schema `GetAllTokenBalancesByAddressResponse401`
- Removed response schema `GetLatestBlockHeightResponse401`
- Removed response schema `GetProtocolDetailResponse404`
- Removed response schema `GetGasPriceResponse401`
- Removed response schema `GetTransactionStatusResponse404`
- Removed response schema `SettleB402PaymentV1Response2`
- Removed response schema `GetLeaderboardResponse401`
- Removed response schema `VerifyB402PaymentV2Response503`
- Removed response schema `GetB402SupportedConfigurationsV2Response503`
- Removed response schema `SettleB402PaymentV2Response503`
- Removed response schema `GetTokenPriceResponse404`
- Removed response schema `GetBroadcastOrdersResponse404`
- Removed response schema `GetPortfolioSupportedChainsResponse403`
- Removed response schema `GetLatestBlockHeightResponse403`
- Removed response schema `GetTopLiquidityPoolsResponse404`
- Removed response schema `VerifyB402PaymentV1Response503`
- Removed response schema `GetTokenTradesResponse403`
- Removed response schema `BuildSwapTransactionResponse404`
- Removed response schema `GetDexTradeHistoryResponse403`
- Removed response schema `GetTokenBasicInfoResponse403`
- Removed response schema `SubmitRfqOrderResponse404`
- Removed response schema `VerifyB402PaymentV1Response401`
- Removed response schema `GetProtocolDetailResponse403`
- Removed response schema `GetDexTradeHistoryResponse404`
- Removed response schema `GetDeFiPositionsResponse404`
- Removed response schema `BroadcastTransactionsResponse404`
- Removed response schema `SettleB402PaymentV1Response401`
- Removed response schema `GetTransactionDetailByHashResponse403`
- Removed response schema `SettleB402PaymentV1Response503`
- Removed response schema `SubmitRfqOrderResponse403`
- Removed response schema `GetInvestmentDetailResponse404`
- Removed response schema `GetTopTradersResponse404`
- Removed response schema `GetTokenPriceResponse403`
- Removed response schema `GetGasLimitResponse401`
- Removed response schema `SearchRwaTokenResponse404`
- Removed response schema `BuildDeFiRedeemTransactionResponse403`
- Removed response schema `GetGasLimitResponse403`
- Removed response schema `GetRwaUnderlyingInfoResponse403`
- Removed response schema `GetAddressPortfolioOverviewResponse401`
- Removed response schema `GetTokenAdvancedInfoResponse401`
- Removed response schema `GetGasLimitResponse404`
- Removed response schema `GetTransactionSupportedChainsResponse403`
- Removed response schema `GetTransactionsByAddressResponse404`
- Removed response schema `GetRwaUnderlyingMarketDataResponse401`
- Removed response schema `GetB402SupportedConfigurationsV2Response403`
- Removed response schema `BuildDeFiDepositTransactionResponse404`
- Removed response schema `SettleB402PaymentV2Response2`
- Removed response schema `GetCandlesResponse404`
- Removed response schema `ListDeFiInvestmentsResponse403`
- Removed response schema `GetRwaTokenListResponse403`
- Removed response schema `GetRwaTokenPriceResponse401`
- Removed response schema `ListDeFiInvestmentsResponse401`
- Removed response schema `GetLeaderboardResponse404`
- Removed response schema `GetLeaderboardResponse403`
- Removed response schema `GetTokenAdvancedInfoResponse403`
- Removed response schema `QuoteAndBuildSwapTransactionResponse403`
- Removed response schema `BroadcastTransactionsResponse401`
- Removed response schema `GetB402SupportedConfigurationsV1Response2`
- Removed response schema `VerifyB402PaymentV2Response1`
- Removed response schema `GetRwaTokenIssuancePlatformsResponse403`
- Removed response schema `SearchRwaTokenResponse401`
- Removed response schema `SettleB402PaymentV2Response429`
- Removed response schema `GetTopLiquidityPoolsResponse403`
- Removed response schema `GetHotTokenListResponse403`
- Removed response schema `VerifyB402PaymentV1Response429`
- Removed response schema `GetErc20ApproveTransactionResponse401`
- Removed response schema `ListDeFiProtocolsResponse404`
- Removed response schema `SearchRwaTokenResponse403`
- Removed response schema `SimulateTransactionsResponse401`
- Removed response schema `GetTransactionSupportedChainsResponse401`
- Removed response schema `SettleB402PaymentV1Response1`
- Removed response schema `SettleB402PaymentV1Response429`
- Removed response schema `GetSupportedChainsResponse404`
- Removed response schema `VerifyB402PaymentV2Response429`
- Removed response schema `GetTransactionSupportedChainsResponse404`
- Removed response schema `GetRwaTokenListResponse401`
- Removed response schema `GetWalletSupportedChainsResponse404`
- Removed response schema `GetWalletSupportedChainsResponse401`
- Removed response schema `GetAllTokenBalancesByAddressResponse403`
- Removed response schema `GetTopTradersResponse401`
- Removed response schema `BuildLpRemoveTransactionResponse401`
- Removed response schema `GetErc20ApproveTransactionResponse403`
- Removed response schema `GetSupportedChainsResponse403`
- Removed response schema `GetTokenTradingInfoResponse403`
- Removed response schema `GetB402SupportedConfigurationsV1Response403`
- Removed response schema `GetDeFiPositionsResponse403`
- Removed response schema `SettleB402PaymentV2Response401`
- Removed response schema `GetHotTokenListResponse401`
- Removed response schema `GetDexTradeHistoryResponse401`
- Removed response schema `GetTopLiquidityPoolsResponse401`
- Removed response schema `GetInvestmentDetailResponse401`
- Removed response schema `VerifyB402PaymentV2Response401`
- Removed response schema `BuildSolanaSwapInstructionsResponse401`
- Removed response schema `GetAddressPnLForSpecificTokenResponse403`
- Removed response schema `GetAggregatedQuoteResponse404`

## 7.0.0 - 2026-09-18

### Added (1)

- Added `binance-web3-common` library

### Changed ()

- Updated `binance-common` library to version `4.4.0`

## 6.2.0 - 2026-09-10

### Changed (2)

- Added parameter `enableRFQ`
  - affected methods:
    - `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`)
- Added parameter `excludeDexes`
  - affected methods:
    - `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`)

## 6.1.0 - 2026-09-02

### Added (17)

- `get_b402_supported_configurations_v1()` (`POST /api/v1/b402/supported`)
- `get_b402_supported_configurations_v2()` (`POST /api/v2/b402/supported`)
- `verify_b402_payment_v1()` (`POST /api/v1/b402/verify`)
- `verify_b402_payment_v2()` (`POST /api/v2/b402/verify`)
- `settle_b402_payment_v1()` (`POST /api/v1/b402/settle`)
- `settle_b402_payment_v2()` (`POST /api/v2/b402/settle`)
- `get_de_fi_positions()` (`POST /api/v1/defi/data/position/list`)
- `list_de_fi_investments()` (`POST /api/v1/defi/data/investment/list`)
- `get_investment_detail()` (`POST /api/v1/defi/data/investment/detail`)
- `list_de_fi_protocols()` (`POST /api/v1/defi/data/protocol/list`)
- `get_protocol_detail()` (`POST /api/v1/defi/data/protocol/detail`)
- `build_de_fi_deposit_transaction()` (`POST /api/v1/defi/transaction/deposit`)
- `build_de_fi_redeem_transaction()` (`POST /api/v1/defi/transaction/redeem`)
- `build_de_fi_claim_transaction()` (`POST /api/v1/defi/transaction/claim`)
- `build_lp_add_transaction()` (`POST /api/v1/defi/transaction/lp-add`)
- `build_lp_remove_transaction()` (`POST /api/v1/defi/transaction/lp-remove`)
- `calculate_lp_add_paired_amounts()` (`POST /api/v1/defi/transaction/lp-add/calculate`)

### Changed (1)

- Added `B402PaymentsApi`, `DefiDataApi` and `DefiTransactionApi` modules

## 6.0.0 - 2026-08-07

### Added (1)

- `get_latest_block_height()` (`GET /api/v1/dex/pre-transaction/block-height`)

### Changed (3)

- Updated `binance-common` library to version `4.2.0`
- Updated Dependencies
- Added parameter `vendor`
  - affected methods:
    - `get_aggregated_quote()` (`GET /api/v1/dex/aggregator/quote`)

## 5.0.0 - 2026-07-29

### Changed (8)

- Added parameter `fee_percent`
  - affected methods:
    - `get_aggregated_quote()` (`GET /api/v1/dex/aggregator/quote`)
    - `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`)
    - `build_swap_transaction()` (`GET /api/v1/dex/aggregator/swap`)
    - `build_solana_swap_instructions()` (`GET /api/v1/dex/aggregator/swap-instruction`)
- Added parameter `fee_source`
  - affected methods:
    - `get_aggregated_quote()` (`GET /api/v1/dex/aggregator/quote`)
- Added parameter `from_token_referrer_wallet_address`
  - affected methods:
    - `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`)
    - `build_swap_transaction()` (`GET /api/v1/dex/aggregator/swap`)
    - `build_solana_swap_instructions()` (`GET /api/v1/dex/aggregator/swap-instruction`)
- Added parameter `to_token_referrer_wallet_address`
  - affected methods:
    - `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`)
    - `build_swap_transaction()` (`GET /api/v1/dex/aggregator/swap`)
    - `build_solana_swap_instructions()` (`GET /api/v1/dex/aggregator/swap-instruction`)
- Modified response for `get_aggregated_quote()` (`GET /api/v1/dex/aggregator/quote`):
  - `data`.items: property `actual_swap_amount` added
  - `data`.items: property `fee_amount` added
  - `data`.items: property `fee_token` added
  - `data`.items: item property `actual_swap_amount` added
  - `data`.items: item property `fee_amount` added
  - `data`.items: item property `fee_token` added

- Modified response for `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`):
  - `data`.`routerResult`: property `actual_swap_amount` added
  - `data`.`routerResult`: property `fee_amount` added
  - `data`.`routerResult`: property `fee_token` added

- Modified response for `build_swap_transaction()` (`GET /api/v1/dex/aggregator/swap`):
  - `data`.`routerResult`: property `actual_swap_amount` added
  - `data`.`routerResult`: property `fee_amount` added
  - `data`.`routerResult`: property `fee_token` added

- Modified response for `buildSolanaSwapInstructions()` (`GET /api/v1/dex/aggregator/swap-instruction`):
  - `data`.`routerResult`: property `actual_swap_amount` added
  - `data`.`routerResult`: property `fee_amount` added
  - `data`.`routerResult`: property `fee_token` added

## 4.0.0 - 2026-07-28

### Changed (2)

- Added parameter `tron_tx`
  - affected methods:
    - `get_gas_limit()` (`POST /api/v1/dex/pre-transaction/gas-limit`)
    - `simulate_transactions()` (`POST /api/v1/dex/pre-transaction/simulate`)

- Modified response for `getGasLimit()` (`POST /api/v1/dex/pre-transaction/gas-limit`):
  - `data`: property `energyFee` added
  - `data`: property `energyRequired` added
  - `data`: property `freeBandwidth` added
  - `data`: property `freeEnergy` added
  - `data`: property `bandwidthFee` added
  - `data`: property `bandwidthRequired` added

## 3.0.0 - 2026-07-21

### Added (17)

- `get_address_pn_l_for_specific_token()` (`GET /api/v1/dex/market/portfolio/token/latest-pnl`)
- `get_address_portfolio_overview()` (`GET /api/v1/dex/market/portfolio/overview`)
- `get_address_recent_pn_l()` (`GET /api/v1/dex/market/portfolio/recent-pnl`)
- `get_dex_trade_history()` (`GET /api/v1/dex/market/portfolio/dex-history`)
- `get_portfolio_supported_chains()` (`GET /api/v1/dex/market/portfolio/supported/chain`)
- `get_leaderboard()` (`GET /api/v1/dex/market/leaderboard/list`)
- `get_tracked_trades()` (`GET /api/v1/dex/market/address-tracker/trades`)
- `get_rwa_token_issuance_platforms()` (`GET /api/v1/dex/market/rwa/platforms`)
- `get_rwa_token_list()` (`GET /api/v1/dex/market/rwa/tokens`)
- `get_rwa_token_price()` (`GET /api/v1/dex/market/rwa/price`)
- `get_rwa_underlying_info()` (`GET /api/v1/dex/market/rwa/underlying-profile`)
- `get_rwa_underlying_market_data()` (`GET /api/v1/dex/market/rwa/underlying-market`)
- `search_rwa_token()` (`GET /api/v1/dex/market/rwa/search`)
- `build_solana_swap_instructions()` (`GET /api/v1/dex/aggregator/swap-instruction`)
- `get_rfq_order_status()` (`GET /api/v1/dex/aggregator/order/{orderId}`)
- `quote_and_build_swap_transaction()` (`GET /api/v1/dex/aggregator/quote-and-swap`)
- `submit_rfq_order()` (`POST /api/v1/dex/aggregator/order/submit`)

### Changed (6)

- Added parameter `user_wallet_address`
  - affected methods:
    - `get_aggregated_quote()` (`GET /api/v1/dex/aggregator/quote`)
- Added parameter `vendor`
  - affected methods:
    - `get_erc20_approve_transaction()` (`GET /api/v1/dex/aggregator/approve-transaction`)
- Modified response for `get_aggregated_quote()` (`GET /api/v1/dex/aggregator/quote`):
  - `data`.items: property `approve_target` added
  - `data`.items: property `execution_mode` added
  - `data`.items: property `is_best` added
  - `data`.items: item property `approve_target` added
  - `data`.items: item property `execution_mode` added
  - `data`.items: item property `is_best` added
- Modified response for `build_swap_transaction()` (`GET /api/v1/dex/aggregator/swap`):
  - `data`: property `execution_mode` added
  - `data`: property `rfq` added
- Modified parameter `slippage_percent`:
  - required: `true` → `false`
  - affected methods:
    - `build_swap_transaction()` (`GET /api/v1/dex/aggregator/swap`)
- Update dependencies

## 2.0.1 - 2026-06-17

- Updated `binance-common` library to version `4.0.1`

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
