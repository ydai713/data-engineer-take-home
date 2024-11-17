create table if not exists dagster.transactions
(
    chain_id         integer not null,
    block_number     integer,
    block_timestamp  timestamp with time zone,
    "from"           text,
    "to"             text,
    transaction_hash text    not null,
    value            numeric,
    PRIMARY KEY (transaction_hash, chain_id)
);
