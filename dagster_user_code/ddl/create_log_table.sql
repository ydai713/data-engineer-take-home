create table if not exists dagster.logs
(
    chain_id         integer not null,
    transaction_hash text    not null,
    log_index        integer not null,
    topics           text[],
    data             text,
    decoded          jsonb,
    method           text,
    address          text,
    primary key (transaction_hash, log_index, chain_id)
);
