#!/usr/bin/env python3
import argparse
import asyncio

from src.connector import ConnectToServer
from src.version_checker import compare_versions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='The tunnel client command.')

    parser.add_argument('port', type=int, help='The port to use.')
    parser.add_argument('project', type=str, help='The project to use.')
    # Options
    parser.add_argument('--local', type=bool, default=False, help='Whether to use the local server.')

    return parser.parse_args()

async def run(local_port: int, project_name: str, is_local: bool):
    await compare_versions()
    await ConnectToServer.create(local_port, project_name, is_local)

def main(local_port: int = None, project_name: str = None, is_local: bool = None):
    # When running on the command line, parse the arguments
    if local_port is None or project_name is None:
        args = parse_args()
        project_name = args.project
        local_port = args.port
        is_local = args.local
    # Otherwise, use the parameters passed in from test scripts

    try:
        asyncio.run(run(local_port, project_name, is_local))
    except KeyboardInterrupt:
        print("\nUR Tunnel stopped. Goodbye!")
    except Exception as e:
        print(f'\nError: {e}')


if __name__ == "__main__":
    main()
