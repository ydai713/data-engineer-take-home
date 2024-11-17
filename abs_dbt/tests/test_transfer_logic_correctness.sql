with valid_transfers as (
  select 
    transaction_hash
    , to_address
    , token_id
  from {{ ref('stg_logs') }}
  where 
    1 = 1
    and to_address is not null
    and token_id is not null
)

select *
from valid_transfers
where
  to_address not like '0x%'
  or length(to_address) != 42
