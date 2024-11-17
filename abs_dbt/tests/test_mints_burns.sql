with mint_burn_transfers as (
  select 
    token_id
    , to_address
    , from_address
  from {{ ref('stg_logs') }}
  where 
    -- burn address
    to_address = '0x0000000000000000000000000000000000000000'
    -- mint address
    or from_address = '0x0000000000000000000000000000000000000000'
)

select *
from mint_burn_transfers
where token_id is null
