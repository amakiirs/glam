from sys import exit
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from yaml import dump, safe_load

from econfgen import generate_config
from econfgen.models import Config, Environment


def get_parser() -> ArgumentParser:
    parser = ArgumentParser('econfgen', description='Tool to generate netlify configurations compatible with the theme')
    parser.add_argument('-P', '--prod', action='store_true', help='If a production or local configuration should be generated')
    parser.add_argument('-c', '--config', type=Path, default=Path.cwd() / 'econfgen.yml', help='Path to the configuration file')
    return parser


def get_config(path: Path) -> Optional[Config]:
    if path.exists():
        with open(path, 'r') as f:
            yaml_config = safe_load(f.read())
            #print(yaml_config)
            return Config(**yaml_config)
    return None


def main() -> int:
    parser = get_parser()
    args = parser.parse_args()
    #print(args)
    if (config := get_config(args.config)) is None:
        print(f'Configuration file not found: {args.config}')
        return 1
    #print(config.default)

    if args.prod:
        # merge the prod keys over the default keys
        final_config = config.default.dict() | { k:v for k,v in config.prod.dict().items() if v is not None }
    else:
        final_config = config
    # print(final_config)

    config = generate_config(backend=final_config['backend'], local_backend=final_config['local_backend'], jobs=final_config['jobs'])
    print(dump(config.dict()))
    return 0


if __name__ == '__main__':
    exit(main())
