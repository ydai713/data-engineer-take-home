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

# Approach

Transformation is handled entirely by DBT. Data ingestion and transformation
are orchestrated by dagster. The pipeline is designed with the following
principles:

1. Modular Data Models:

    **Base Layer**: Raw data ingested from logs and transactions.

    **Staging Layer**: Cleaned and standardized data, ready for analysis.

    **Intermediate Layer**: Aggregations and transformations to calculate
    incremental updates.

    **Mart Layer**: Final business-ready tables for analysis and reporting,
    including: Snapshot of all NFT holders. Trader classifications (e.g.,
    whales, high-value holders).

2. Incremental Processing:

    Intermediate models are configured to process only new data, reducing
    processing time and enabling faster updates.

3. Trader Classification:

    Parameterized logic to classify traders as:

        * Whales: Holders of >1% of supply.
        * High-Value Holders: Holders of ≥2 NFTs a net worth >$5k.
        * Regular Traders: All other holders.

4. Validation:

    Basic dbt tests ensure data quality: Correctness of transfer logic.
    Validation of holdings calculations. Handling edge cases such as mints and
    burns.

5. Automation:

    A Dagster job refreshes the current holder snapshot and trader
    classification every 5 minutes. Includes logging and error handling for
    debugging and monitoring.

# Snapshot

1. table `mart_nft_holders` shows current snapshot of all NFT holders including
   total tokens held per wallet.
```
               wallet_address               | total_tokens_held |  first_transfer_time   |   last_transfer_time
--------------------------------------------+-------------------+------------------------+------------------------
 0x0000000000000000000000000000000000000000 |               960 | 2022-01-07 15:26:58-08 | 2023-09-21 11:53:11-07
 0x000000000000feA5F4B241F9E77B4D43B76798a9 |                 1 | 2024-11-08 23:29:23-08 | 2024-11-08 23:29:23-08
 0x00000060Bb1e57E3f1aF1102f68Db9fc2ee489bc |                 2 | 2023-06-28 16:06:11-07 | 2023-07-01 06:36:23-07
 0x0000009072063E8accCD96346df848dE0D2E57f4 |                 1 | 2024-04-23 04:20:35-07 | 2024-04-23 04:20:35-07
 0x00001f78189bE22C3498cFF1B8e02272C3220000 |                10 | 2023-06-15 10:09:35-07 | 2023-06-15 10:09:35-07
```

2. table `mart_trader_classification` shows trader classification
```

               wallet_address               | wallet_tokens_held | total_networth_usd |   percent_of_supply    | trader_classification
--------------------------------------------+--------------------+--------------------+------------------------+-----------------------
 0x0000000000000000000000000000000000000000 |                960 |                    |     5.5216841136546647 | Whale
 0x000000000000feA5F4B241F9E77B4D43B76798a9 |                  1 |                    | 0.00575175428505694237 | Regular Trader
 0x00000060Bb1e57E3f1aF1102f68Db9fc2ee489bc |                  2 |                    | 0.01150350857011388473 | Regular Trader
 0x0000009072063E8accCD96346df848dE0D2E57f4 |                  1 |                    | 0.00575175428505694237 | Regular Trader
 0x00001f78189bE22C3498cFF1B8e02272C3220000 |                 10 |                    | 0.05751754285056942367 | Regular Trader
 0x000058d75AB402902838Dbf5Aa9d1894Bb420000 |                  1 |                    | 0.00575175428505694237 | Regular Trader
```

# How to run
1. start the pod by running `podman-compose up --build`.
2. go to `localhost:3000` and go to dbt-pipeline DAG, and launch.
3. the DAG contains the following:
    1. run DDL to create tables to hold raw transaction and log data.
    2. ingest log data and transaction data 
    3. run `dbt deps` and `dbt seed`
    4. start `dbt run`
    5. start `dbt test`

# What is not done
1. While tests are implemented to ensure data quality, they were not
   validated against Etherscan due to time constraints.
2. Due to limited domain knowledge in blockchain, the trader
   classification logic might not be fully accurate. Additionally, the
   `total_networth_usd` column contains only two populated rows, which could
   impact the effectiveness of the classification logic.
3. Limited Experience with Dagster: My primary orchestration tools have
   been Airflow and AWS Step Functions. This was my first experience
   using Dagster, so the implementation might not align with Dagster's best
   practices.
4. Time Constraints:
   With 4 hours allocated to the assignment, the current implementation
   represents the best effort within the time available. There are likely
   areas for improvement in design and execution.
