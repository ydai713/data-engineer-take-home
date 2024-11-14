{{
    config(
        materialized='table',
        schema='public'
    )
}}

select 1 as id, 'test' as name