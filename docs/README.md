# Overview 

This project implements an analytics pipeline that processes NFT transfer
events and wallet data using DBT and Dagster. The pipeline does the following:

* **Ingestion** ingestion: NFT transfer logs and transaction data.
* **Transformation** Build analytics data models to capture current NFT holding
and classify traders.
* **Testing** Implement data quality tests to ensure accuracy.
* **Orchestration** Automates the entire process with a Dagster job scheduled
to run every 5 minutes.

# Assumptions

To simulate a real-world scenario where new data arrives periodically, the
large data ingestion files (`logs_nft1.sql`, `logs_nft2.sql`, `txs_nft1.sql`,
`txs_nft2.sql`) are broken down into smaller chunk files. These chunks mimic
new files being deposited into the filesystem every 5 minutes. This approach
allows the pipeline to process data incrementally, demonstrating its ability to
handle continuous data ingestion without duplicating existing data.

# Local development
1. Created a new folder `ddl` for ddl statements to create `logs` and
   `transactions` tables.
2. run the following commands to create tables and ingest data.
   ```
   psql -U yang -h localhost -d postgres -f ddl/create_log_table.sql
   psql -U yang -h localhost -d postgres -f ddl/create_transaction_table.sql
   psql -U yang -h localhost -d postgres -f token_data/*
   ```
