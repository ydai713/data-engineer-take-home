from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import dbt_assets, create_dbt_manifest, create_manifest_job

defs = Definitions(
    assets=[*dbt_assets, create_dbt_manifest],
    jobs=[create_manifest_job],
    resources={
        "dbt": DbtCliResource(
            project_dir="dbt",
            profiles_dir="dbt",
        ),
    },
)