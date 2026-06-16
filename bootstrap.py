from storage.migrations.migration_runner import (
    MigrationRunner
)


runner = MigrationRunner(

    db_path="aviapos.db",

    migration_dir=
        "storage/migrations"
)

runner.run()

print(
    "Database initialized."
)