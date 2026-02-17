# Cassandra CLI

A command-line interface for interacting with Cassandra `nodetool` via `kubectl exec`.

## Setup

This project uses Poetry for dependency management.

1.  **Install dependencies:**
    ```bash
    poetry install
    ```

2.  **Set Environment Variables:**

    ```bash
    export NODETOOL_USER=<your_username>
    export NODETOOL_PASSWORD=<your_password>
    ```

## Usage

To run a `nodetool` command, use the following format:

```bash
poetry run python -m cassandra_cli.cli [OPTIONS] <nodetool_command>
```

**Options:**
- `--namespace`: Kubernetes namespace (default: `cassandra`)
- `--pod`: Cassandra pod name (default: `a-cassandra-0`)

**Examples:**

```bash
# Basic command (uses defaults)
poetry run python -m cassandra_cli.cli status

# Specify namespace
poetry run python -m cassandra_cli.cli --namespace cassandra status

# Specify both namespace and pod
poetry run python -m cassandra_cli.cli --namespace cassandra --pod a-cassandra-0 status

# Commands with arguments
poetry run python -m cassandra_cli.cli compactionstats -H
poetry run python -m cassandra_cli.cli ring
poetry run python -m cassandra_cli.cli tablestats keyspace.table
```

## Default Configuration

- **Namespace:** `cassandra`
- **Pod:** `a-cassandra-0`