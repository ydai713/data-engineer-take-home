psql -U yang -h localhost -d postgres -f ddl/create_log_table.sql
psql -U yang -h localhost -d postgres -f ddl/create_transaction_table.sql
psql -U yang -h localhost -d postgres -f token_data/*
