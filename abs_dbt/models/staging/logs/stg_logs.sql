with raw_logs as (
  select * from {{ ref('base_logs') }}
)

select
  chain_id
  , transaction_hash
  , log_index
  , topics
  , data
  , cast(decoded->>'to' as text) as to_address
  , cast(decoded->>'from' as text) as from_address
  , cast(decoded->>'tokenId' as numeric) as token_id
  , method
  , address as contract_addres
from raw_logs
where 
  1 = 1
  and method = 'Transfer'
