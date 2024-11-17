from dagster import Definitions, ScheduleDefinition

from .assets import (
    create_table,
    dbt_assets,
    dbt_pipeline,
    dbt_resource,
    ingest_log_data,
    ingest_transaction_data,
    run_dbt,
    test_dbt,
    create_dbt_manifest,
)


defs = Definitions(
    assets=[
        *dbt_assets,
        create_dbt_manifest,
        run_dbt,
        test_dbt,
        create_table,
        ingest_transaction_data,
        ingest_log_data,
    ],
    jobs=[dbt_pipeline],
    resources={"dbt": dbt_resource},
    schedules=[ScheduleDefinition(job=dbt_pipeline, cron_schedule="*/5 * * * *")],
)
