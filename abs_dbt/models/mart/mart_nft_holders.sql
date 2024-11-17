with snapshot as (
  select * from {{ ref('int_nft_holders') }}
)

select
  wallet_address
  , count(distinct token_id) as total_tokens_held
  , min(first_transfer_time) as first_transfer_time
  , max(last_transfer_time) as last_transfer_time
from snapshot
group by wallet_address
