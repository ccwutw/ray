import os
import subprocess
import sys

from typing import List

import ci.ray_ci.bazel_sharding as bazel_sharding

_DOCKER_ECR_REPO = os.environ.get(
    "RAYCI_WORK_REPO",
    "029272617770.dkr.ecr.us-west-2.amazonaws.com/rayproject/citemp",
)
_RAYCI_BUILD_ID = os.environ.get("RAYCI_BUILD_ID", "unknown")
_PIPELINE_POSTMERGE = "0189e759-8c96-4302-b6b5-b4274406bf89"
DOCKER_ENV = [
    "BUILDKITE_BUILD_URL",
    "BUILDKITE_BRANCH",
    "BUILDKITE_COMMIT",
    "BUILDKITE_JOB_ID",
    "BUILDKITE_LABEL",
    "BUILDKITE_PIPELINE_ID",
]
DOCKER_CAP_ADD = [
    "SYS_PTRACE",
    "SYS_ADMIN",
    "NET_ADMIN",
]

class Container:
    """
    A wrapper for running commands in ray ci docker container
    """

    def __init__(self, docker_tag: str) -> None:
        self.docker_tag = docker_tag

    def run_script(self, script: str) -> bytes:
        """
        Run a script in container
        """
        return subprocess.check_output(self.get_run_command(script))


    def _get_run_command(self, script: str) -> List[str]:
        command = [
            "docker",
            "run",
            "-i",
            "--rm",
            "--volume",
            "/tmp/artifacts:/artifact-mount"
        ]
        for env in DOCKER_ENV:
            command += ["--env", env]
        for cap in DOCKER_CAP_ADD:
            command += ["--cap-add", cap]
        command += [
            "--workdir",
            "/rayci",
            "--shm-size=2.5gb",
            self._get_docker_image(),
            "/bin/bash", 
            "-ice", 
            script
        ]

    def _get_docker_image(self) -> str:
        """
        Get docker image for a particular commit
        """
        return f"{_DOCKER_ECR_REPO}:{_RAYCI_BUILD_ID}-{self.docker_tag}"
