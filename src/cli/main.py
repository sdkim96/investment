import argparse
import os
import yaml

import src.app as app
from src.client import (
    UpbitClient,
    AlternativeClient,
)


def load_yaml(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    """The Main entry point for the CLI application.
    
    Example execution:
    `python -m src.cli.main --config src/config.yaml`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to config yaml"
    )
    args = parser.parse_args()

    raw_config = load_yaml(args.config)
    config = app.AppConfig(**raw_config)

    upbit_client = UpbitClient(
        access_key=os.environ.get("UPBIT_ACCESS_KEY", None),
        secret_key=os.environ.get("UPBIT_SECRET_KEY", None),
    )
    alternative_client = AlternativeClient()

    runner = app.Runner(
        config=config,
        upbit_client=upbit_client,
        alternative_client=alternative_client,
    )

    for event in runner.run():
        print(event)


if __name__ == "__main__":
    main()