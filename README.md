### Data Engineering Take-Home Assignment

**Context:**  
We have a simple dataset of NFT transfers (ERC721) between wallets. Each transfer has: timestamp, from_address, to_address, token_id, and collection_address.

**Task:**  
Build a small data pipeline that:

1. Processes raw transfer events to calculate:
   - Current NFT ownership per wallet
   - Total number of unique collections a wallet has interacted with
   - "Power users" (wallets with > X transfers)

2. Implements these requirements:
   - Use dbt for transformations
   - Create appropriate table schemas
   - Include incremental processing logic
   - Add basic data quality tests
   - Write efficient SQL queries
   - Include basic documentation

**Provided:**
- Sample PostgreSQL database with raw transfer events
- Basic dagster setup
- Simple explanation of NFT transfers
- Example expected outputs

**Bonus Points:**
- Query optimization suggestions
- Error handling considerations
- Monitoring recommendations
- Testing strategy
- Performance considerations for scale

We are looking for:
- SQL expertise
- Data modeling
- Incremental processing
- Testing approach
- Documentation skills
- Performance optimization thinking
- Basic blockchain data understanding
