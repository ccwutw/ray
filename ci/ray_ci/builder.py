import click

from ci.ray_ci.build_container import PYTHON_VERSIONS, BuildContainer
from ci.ray_ci.utils import logger


@click.command()
@click.argument(
    "artifact_type",
    required=True,
    type=click.Choice(["wheel", "jar"]),
)
@click.option(
    "--python-version",
    default="py38",
    type=click.Choice(list(PYTHON_VERSIONS.keys())),
    help=("Python version to build the wheel with"),
)
def main(
    artifact_type: str,
    python_version: str,
) -> None:
    """
    Build a wheel or jar artifact
    """
    if artifact_type == "wheel":
        logger.info(f"Building wheel for Python {python_version}")
        container = BuildContainer(python_version)
        container.run()
        logger.info("Successfully built wheel. Artifacts are in ray/.whl")
    elif artifact_type == "jar":
        raise NotImplementedError("Jar build not implemented yet")
    else:
        raise ValueError(f"Invalid artifact type {artifact_type}")
