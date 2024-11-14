from dagster import AssetExecutionContext, asset, job
from dagster_dbt import DbtCliResource, load_assets_from_dbt_manifest

@asset
def create_dbt_manifest(context: AssetExecutionContext, dbt: DbtCliResource):
    """Run dbt commands to create manifest file"""
    # First run dbt deps to install dependencies
    dbt.cli(["deps"], context=context).wait()
    
    # Then run dbt compile to generate manifest
    dbt.cli(["compile"], context=context).wait()
    
    return "Manifest created successfully"

@job
def create_manifest_job():
    create_dbt_manifest()

dbt_assets = load_assets_from_dbt_manifest(
    manifest="dbt/target/manifest.json",
    # Set this to True to load assets even if manifest doesn't exist yet
    load_from_manifest_only=False
)

@asset
def example_asset():
    """A simple example asset"""
    return {"hello": "world"}