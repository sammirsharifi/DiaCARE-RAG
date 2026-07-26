from tqdm.auto import tqdm


def progress(
    iterable,
    desc: str,
    total=None,
    unit="item",
):
    """
    Shared project progress bar.
    """

    return tqdm(
        iterable,
        desc=desc,
        total=total,
        unit=unit,
        leave=True,
        dynamic_ncols=True,
    )