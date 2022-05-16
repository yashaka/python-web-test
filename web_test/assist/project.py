
def abs_path_from_project(relative_path: str):
    import web_test
    from pathlib import Path
    return Path(
        web_test.__file__
    ).parent.parent.joinpath(relative_path).absolute().__str__()
