import argparse
from cassandra_cli.executor import NodetoolExecutor
import sys
import logging


def parse_args():
    parser = argparse.ArgumentParser(description="Cassandra Nodetool CLI")

    parser.add_argument("--namespace", default="cassandra")
    parser.add_argument("--pod", default="a-cassandra-0")

    # Parse known args first
    args, remaining = parser.parse_known_args()

    if not remaining:
        parser.error("You must provide a nodetool command")

    return args.namespace, args.pod, remaining


def main():
    namespace, pod, nodetool_args = parse_args()

    try:
        executor = NodetoolExecutor(namespace, pod)
        output = executor.run(nodetool_args)
        logging.info(output)
    except RuntimeError as e:
        logging.info(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
