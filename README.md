# NFT Analytics Engineering Assignment

## Overview
Build an analytics pipeline that processes NFT transfer events and wallet data using provided dbt and Dagster environment. Expected time: 3-4 hours.

## Data Sources
Run these in the order they're listed below
- `logs_nft1.sql`
- `logs_nft2.sql`
- `txs_nft1.sql`
- `txs_nft2.sql`

`wallet_networth.csv` is a csv file with each holder's wallet native balance on ethereum.

Import this data into your db in another table to then run the analysis pipelines on them.

## Required Analytics Models

### 1. Core NFT Ownership (Primary Focus)
Create models showing:
- Current snapshot of all NFT holders
- Incrementally updates for faster processing
- Includes total tokens held per wallet
- Includes first/last transfer timestamps per wallet

### 2. Trader Classification
- Whales: Wallets holding >1% of supply
- High-Value Holders: Wallets holding ≥2 NFTs AND net worth >$5k
  - We should be able to easily paramterize the NFT and net worth number and rerun the analysis on the new parameters

### 3. Data Quality
Implement basic dbt tests to verify:
- Transfer logic correctness
- Holdings calculations
- Edge cases (mints/burns)

### 4. Simple Refresh Pipeline
Create a Dagster job that:
- Refreshes current holders and trader classifications
- Runs every 5 minutes
- Includes basic logging

## Deliverables
1. DBT Models
   - Analytics models
   - Basic tests

2. Dagster Pipeline
   - Basic scheduled job
   - Error handling

3. README explaining:
   - Approach
   - How to run
   - How to validate

## Validation
Compare against Etherscan:
- https://etherscan.io/token/0xc2e9678a71e50e5aed036e00e9c5caeb1ac5987d
- https://etherscan.io/token/0x1b41d54b3f8de13d58102c50d7431fd6aa1a2c48