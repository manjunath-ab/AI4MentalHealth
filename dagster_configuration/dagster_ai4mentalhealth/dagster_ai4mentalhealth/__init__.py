from dagster import Definitions, load_assets_from_modules, ScheduleDefinition, AssetSelection, define_asset_job
from . import blurt


blurt_assets = load_assets_from_modules([blurt])
blurt_pipeline = define_asset_job("blurt_pipeline", selection=blurt_assets)
blurt_schedule = ScheduleDefinition(job=blurt_pipeline, cron_schedule="11 2 * * *")

defs = Definitions(
    assets=blurt_assets,
    jobs=[blurt_pipeline],
    schedules=[blurt_schedule]
)