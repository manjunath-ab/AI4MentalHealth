from dagster import Definitions, load_assets_from_modules, ScheduleDefinition, AssetSelection, define_asset_job

from . import assets,python_to_snowflake

all_assets = load_assets_from_modules([assets,python_to_snowflake])

blurt_pipeline = define_asset_job("blurt_pipeline", selection=AssetSelection.all())

basic_schedule = ScheduleDefinition(job=blurt_pipeline, cron_schedule="11 2 * * *")

defs = Definitions(
    assets=all_assets,
    jobs=[blurt_pipeline],
    schedules=[basic_schedule]
)