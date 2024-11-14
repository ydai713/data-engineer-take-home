from dagster import AssetExecutionContext, asset, job
from dagster_dbt import DbtCliResource, load_assets_from_dbt_project

@asset
def create_dbt_manifest(context: AssetExecutionContext, dbt: DbtCliResource):
    """Run dbt commands to create manifest file"""
    dbt.cli(["deps"], context=context).wait()
    dbt.cli(["compile"], context=context).wait()
    return "Manifest created successfully"

@job
def create_manifest_job():
    create_dbt_manifest()

# Explicitly specify the dbt_resource_key
dbt_assets = load_assets_from_dbt_project(
    project_dir="/opt/dagster/app/abs_dbt",
    profiles_dir="/root/.dbt",
    dbt_resource_key="dbt"
)

@asset
def example_asset():
    """A simple example asset"""
    return {"hello": "world"}
