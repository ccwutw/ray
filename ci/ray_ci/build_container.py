import os

from ci.ray_ci.container import Container

PYTHON_VERSIONS = {
    "py37": ("cp37-cp37m", "1.14.5"),
    "py38": ("cp38-cp38", "1.14.5"),
    "py39": ("cp39-cp39", "1.19.3"),
    "py310": ("cp310-cp310", "1.22.0"),
    "py311": ("cp311-cp311", "1.22.0"),
}


class BuildContainer(Container):
    def __init__(self, python_version: str) -> None:
        super().__init__(
            "manylinux",
            volumes=[f"{os.environ.get('RAYCI_TEMP')}:/rayci"],
        )
        self.bin_path, self.numpy_version = PYTHON_VERSIONS[python_version]

    def run(self) -> None:
        self.run_script(
            f"""
            ./ci/build/build-manylinux-ray.sh
            ./ci/build/build-manylinux-wheel.sh {self.bin_path} {self.numpy_version}
            ./ci/build/copy_build_artifacts.sh wheel
            """
        )
