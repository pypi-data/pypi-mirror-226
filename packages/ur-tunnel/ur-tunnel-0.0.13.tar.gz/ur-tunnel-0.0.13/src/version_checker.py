import aiohttp
from packaging import version
from src.package_info import __version__, __package_name__

async def _get_pypi_version() -> version.Version:
    """Get the latest version of the package from PyPI."""
    async with ((aiohttp.ClientSession()) as session):
        async with session.get(
                f"https://pypi.org/pypi/{__package_name__}/json",
                ssl=False
        )as response:
            data = await response.json()
            pypi_version = data.get('info',{}).get('version','0.0.0')
            return version.parse(pypi_version)

async def compare_versions() -> None:
    """Compare the client version to the latest version on PyPI."""
    pypi_version = await _get_pypi_version()
    current_version = version.parse(__version__)
    print('Current version:', current_version)
    if pypi_version.major > current_version.major \
            or pypi_version.minor > current_version.minor:
        # Major or minor version mismatch
        raise VersionMismatch(f'Version mismatch: {pypi_version} > {current_version}.'
                              f' Run "pip install {__package_name__} --upgrade" to update.')
    elif pypi_version.micro > current_version.micro:
        # Micro version mismatch
        print(f'V{pypi_version} available.'
              f'Run "pip install {__package_name__} --upgrade" to update.')

class VersionMismatch(Exception):
    """Raised when the client version is not up-to-date."""
    pass
