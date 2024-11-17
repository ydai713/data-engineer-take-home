with holdings as (
  select
    wallet_address
    , count(distinct token_id) as total_tokens_held
  from {{ ref('int_nft_holders') }}
  group by wallet_address
)

select *
from holdings
where total_tokens_held < 0
