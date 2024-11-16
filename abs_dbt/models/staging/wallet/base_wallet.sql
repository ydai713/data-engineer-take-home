SELECT 
    address,
    total_networth_usd,
    native_balance,
    native_balance_usd,
    token_balance_usd
FROM {{ source('public', 'wallet_networth') }}
