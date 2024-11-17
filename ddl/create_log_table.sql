CREATE TABLE logs
(
    chain_id         integer NOT NULL,
    transaction_hash text    NOT NULL,
    log_index        integer NOT NULL,
    topics           text[],
    data             text,
    decoded          jsonb,
    method           text,
    address          text,
    PRIMARY KEY (transaction_hash, log_index, chain_id)
);
