import os
import sys

import click

import seaplane.config
import seaplane.api


def api_config():
    if not seaplane.config.exists():
        click.echo(
            click.style("Configuration doesn't exist, run config init first.", fg="red")
        )
        sys.exit(1)
    config = seaplane.config.read()
    configuration = seaplane.api.Configuration()
    if config.current_context.options.get("carrier-api-url"):
        configuration.host = config.current_context.options["carrier-api-url"]
    if config.current_context.options.get("jwt") is not None:
        configuration.access_token = config.current_context.options.get("jwt")  # type: ignore
    else:
        click.echo(
            click.style("Missing JWT, try ", fg="yellow") + click.style("auth refresh")
        )
        sys.exit(2)
    return configuration


def read_or_return_string(string_or_file):
    if string_or_file.startswith("@"):
        # File
        file_obj = sys.stdin
        if string_or_file[1:] != "-":
            file_obj = open(os.path.expanduser(string_or_file[1:]), "r")
        string_or_file = file_obj.read()
    return string_or_file


def map_nested_dicts(ob):
    if hasattr(ob, "items") and callable(ob.items):
        return {k: map_nested_dicts(v) for k, v in ob.items()}
    else:
        return ob
