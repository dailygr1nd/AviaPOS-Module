SNAPSHOT_INTERVAL = 500


def should_snapshot(
    version: int
):

    return (
        version > 0
        and version % SNAPSHOT_INTERVAL == 0
    )