ROOT = "https://git.geo.tuwien.ac.at/api/v4/projects/1266/repository/files/"


def make_url(
    file: str,
    *,
    lfs: bool = True,
    is_zip: bool = False,
    cache: bool = False,
    verbose: bool = True,
    branch: str = "main",
) -> str:
    """Generate a download URL for a file in the repository."""
    url = f"{ROOT}{file}/raw?ref={branch}&lfs={str(lfs).lower()}"
    if verbose:
        print(url)
    if is_zip:
        url = f"zip::{url}"
    if cache:
        url = f"simplecache::{url}"
    return url
