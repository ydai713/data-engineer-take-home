{{ 
  config(
    materialized="table"
  ) 
}}

{% set whale_threshold = var('whale_threshold', 0.01) %}
{% set nft_min_count_threshold = var('nft_threshold', 2) %}
{% set net_worth_threshold = var('net_worth_threshold', 5000) %}

with wallet_holdings as (
  select
    h.wallet_address,
    count(distinct h.token_id) as wallet_tokens_held,
    count(distinct h.token_id) * 100.0 / (
      select count(distinct token_id) 
      from {{ ref('int_nft_holders') }}
    ) as percent_of_supply
  from {{ ref('int_nft_holders') }} h
  group by h.wallet_address
)

, wallet_classifications as (
  select
    h.wallet_address,
    h.wallet_tokens_held,
    w.total_networth_usd,
    h.percent_of_supply,
    case
      when h.percent_of_supply > {{ whale_threshold * 100 }} then 'Whale'
      when h.wallet_tokens_held >= {{ nft_min_count_threshold }} and w.total_networth_usd > {{ net_worth_threshold }} then 'High-Value Holder'
      else 'Regular Trader'
    end AS trader_classification
  from wallet_holdings h
  left join {{ ref('stg_wallet') }} w
    on h.wallet_address = w.wallet_address
)

select
  wallet_address,
  wallet_tokens_held,
  total_networth_usd,
  percent_of_supply,
  trader_classification
from wallet_classifications
order by wallet_address
