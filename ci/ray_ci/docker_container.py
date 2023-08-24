import os

from ci.ray_ci.container import Container
from ci.ray_ci.build_container import PYTHON_VERSIONS


class DockerContainer(Container):
    def __init__(self, python_version: str) -> None:
        super().__init__(
            "forge",
            volumes=[f"{os.environ['RAYCI_TEMP']}:/rayci"],
        )
        self.python_version = python_version

    def run(self) -> None:
        base_image = (
            f"{os.environ['RAYCI_WORK_REPO']}:"
            f"{os.environ['BUILDKITE_COMMIT'][:6]}"
            "-raybase"
        )
        wheel_name = (
            "ray-3.0.0.dev0-"
            f"{PYTHON_VERSIONS[self.python_version][0]}-"
            "manylinux2014_x86_64.whl"
        )
        constraints_file = (
            "requirements_compiled_py37.txt"
            if self.python_version == "py37"
            else "requirements_compiled.txt"
        )
        ray_image = (
            "rayproject/ray:"
            f"{os.environ['BUILDKITE_COMMIT'][:6]}-"
            f"{self.python_version}-cpu"
        )
        self.run_script(
            f"""
            ./ci/build/build-ray-docker.sh \
              {wheel_name} {base_image} {constraints_file} {ray_image}
            """
        )
