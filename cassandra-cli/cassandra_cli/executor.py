import subprocess
import os


class NodetoolExecutor:
    def __init__(self, namespace: str, pod_name: str):
        self.namespace = namespace
        self.pod_name = pod_name
        self.user = os.getenv("NODETOOL_USER")
        if not self.user:
            raise RuntimeError("NODETOOL_USER environment variable not set")
        self.password = os.getenv("NODETOOL_PASSWORD")
        if not self.password:
            raise RuntimeError("NODETOOL_PASSWORD environment variable not set")

    def build_command(self, nodetool_args: list[str]) -> list[str]:
        return [
            "kubectl",
            "exec",
            "-n",
            self.namespace,
            self.pod_name,
            "-c",
            "cassandra",
            "--",
            "nodetool",
            "-Dcom.sun.jndi.rmiURLParsing=legacy", # depends on cassandra version, but generally needed for nodetool to work properly
            "-u",
            self.user,
            "-pw",
            self.password,
            *nodetool_args,
        ]

    def run(self, nodetool_args: list[str]) -> str:
        command = self.build_command(nodetool_args)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout
