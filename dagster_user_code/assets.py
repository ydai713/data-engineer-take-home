from dagster import job, op, AssetExecutionContext, Definitions, ScheduleDefinition
from dagster_dbt import DbtCliResource, load_assets_from_dbt_project

# Load dbt assets
dbt_assets = load_assets_from_dbt_project(
    project_dir="/opt/dagster/app/abs_dbt",
    profiles_dir="/root/.dbt",
    dbt_resource_key="dbt"
)

# Define operations to run dbt commands
@op(required_resource_keys={"dbt"})
def run_dbt(context: AssetExecutionContext):
    """Run all dbt models."""
    dbt = context.resources.dbt
    context.log.info("Starting dbt run...")
    dbt.cli(["run"], context=context).wait()
    context.log.info("dbt run completed.")

@op(required_resource_keys={"dbt"})
def test_dbt(context: AssetExecutionContext):
    """Run all dbt tests."""
    dbt = context.resources.dbt
    context.log.info("Starting dbt test...")
    dbt.cli(["test"], context=context).wait()
    context.log.info("dbt test completed.")

# Define the job combining dbt run and test
@job(resource_defs={"dbt": DbtCliResource})
def dbt_pipeline():
    run_dbt()
    test_dbt()

# Define the dbt CLI resource
dbt_resource = DbtCliResource(
    project_dir="/opt/dagster/app/abs_dbt",
    profiles_dir="/root/.dbt"
)

# Define the schedule and assets
defs = Definitions(
    assets=dbt_assets,
    jobs=[dbt_pipeline],
    resources={"dbt": dbt_resource},
    schedules=[
        ScheduleDefinition(job=dbt_pipeline, cron_schedule="*/5 * * * *")
    ]
)
