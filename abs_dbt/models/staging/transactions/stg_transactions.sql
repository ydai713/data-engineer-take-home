with raw_transactions as (
  select * from {{ ref('base_transactions') }}
)

select
  chain_id
  , block_number
  , block_timestamp
  , lower("from") as from_address
  , lower("to") as to_address
  , transaction_hash
  , value
from raw_transactions
