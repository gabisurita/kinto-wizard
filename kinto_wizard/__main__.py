import argparse

from ruamel import yaml
from kinto_http import cli_utils

from .logger import logger
from .kinto2yaml import introspect_server


def main():
    parser = argparse.ArgumentParser(description="Wizard to setup Kinto with YAML")
    subparsers = parser.add_subparsers(title='subcommand',
                                       description='Load/Dump',
                                       dest='subcommand',
                                       help="Choose and run with --help")
    subparsers.required = True
    for command in ('load', 'dump'):
        subparser = subparsers.add_parser(command)
        subparser.set_defaults(which=command)

        cli_utils.add_parser_options(subparser,
                                     include_bucket=False,
                                     include_collection=False)

        if command == 'load':
            subparser.add_argument(dest='filepath', help='YAML file')

    args = parser.parse_args()
    cli_utils.setup_logger(logger, args)

    logger.debug("Instantiate Kinto client.")
    client = cli_utils.create_client_from_args(args)

    if args.which == 'dump':
        logger.debug("Start introspection...")
        result = introspect_server(client)
        print(yaml.safe_dump(result, default_flow_style=False))

    elif args.which == 'load':
        logger.debug("Start initialization...")
        initialize_server(client, args.filepath)


if __name__ == "__main__":
    main()
