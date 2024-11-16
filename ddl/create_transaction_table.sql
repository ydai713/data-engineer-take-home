SET search_path TO dagster, public;

CREATE TABLE transactions
(
    chain_id         integer NOT NULL,
    block_number     integer,
    block_timestamp  timestamp WITH TIME ZONE,
    "from"           text,
    "to"             text,
    transaction_hash text    NOT NULL,
    value            numeric,
    PRIMARY KEY (transaction_hash, chain_id)
);
