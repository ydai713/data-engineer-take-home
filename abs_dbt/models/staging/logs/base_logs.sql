SELECT 
    chain_id,
    transaction_hash,
    log_index,
    topics,
    data,
    decoded,
    method,
    address
FROM {{ source('public', 'logs') }}
