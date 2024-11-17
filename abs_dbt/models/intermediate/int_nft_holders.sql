{{
  config(
    materialized='incremental',
    unique_key=['wallet_address', 'token_id'],
    incremental_strategy='merge' 
  )
}}

with transfers as (
  select 
    a.to_address as wallet_address
    , a.token_id
    , min(b.block_timestamp) as first_transfer_time
    , max(b.block_timestamp) as last_transfer_time
  from {{ ref('stg_logs') }} a
  inner join {{ ref('stg_transactions') }} b
    on a.transaction_hash = b.transaction_hash
  where 
    1 = 1
    and a.to_address is not null
  group by a.to_address, a.token_id
)

select 
  wallet_address,
  token_id,
  first_transfer_time,
  last_transfer_time
from transfers

{% if is_incremental() %}
where 
  1 = 1
  and last_transfer_time > ( select max(last_transfer_time) from {{ this }}
)
{% endif %}
