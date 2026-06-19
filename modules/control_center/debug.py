from core.projections.bootstrap import engine


def rebuild_projections():

    engine.rebuild()

    return {
        "status": "rebuilt"
    }