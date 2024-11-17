SELECT 
    chain_id,
    block_number,
    block_timestamp,
    "from",
    "to",
    transaction_hash,
    value
FROM {{ source('dagster', 'transactions') }}
