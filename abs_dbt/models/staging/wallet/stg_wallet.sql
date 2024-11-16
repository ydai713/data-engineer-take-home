with raw_wallets as (
    select * from {{ ref('base_wallet') }}
)

select
    lower(address) as wallet_address
    , total_networth_usd
    , native_balance
    , native_balance_usd
    , token_balance_usd
from raw_wallets
