import json
import os
import pathlib
import subprocess
import sys
from io import StringIO
from typing import Optional

import jinja2
import ruamel.yaml as yaml
import tomli
import typer
from jinja2 import BaseLoader
from pyfzf.pyfzf import FzfPrompt

from struct2args import generate
from struct2args._util import GetFreePort

INTERACTIVE_MODE = os.environ.get("S2A_INTERACTIVE", True)

app = typer.Typer()


@app.command("generate")
def generate_command(
    file: pathlib.Path,
    name: Optional[str] = typer.Option(None),
    cmd: Optional[str] = typer.Option(None),
):
    environment = jinja2.Environment(
        loader=BaseLoader, extensions=["jinja2_git.GitExtension"]
    )
    environment.add_extension(GetFreePort)
    file_text = environment.from_string(file.read_text()).render()

    if file.suffix == ".yml" or file.suffix == ".yaml":
        parsed_file = yaml.safe_load(StringIO(file_text))
    elif file.suffix == ".json":
        parsed_file = json.loads(file_text)
    elif file.suffix == ".toml":
        parsed_file = tomli.loads(open(file, "r").read())
    else:
        typer.echo(
            "File extension not supported. Must be one of: .yml, .yaml, .json, .toml."
        )
        exit(1)

    if INTERACTIVE_MODE and name is None:
        try:
            fzf = FzfPrompt()
        except SystemError as se:
            typer.echo(f"\n{se}")
            exit(1)
        name = fzf.prompt([arg["_name"] for arg in parsed_file["__args__"]])[0]
    elif not INTERACTIVE_MODE and name is None:
        typer.echo("Name must be provided in non-interactive mode.")
        exit(1)

    called_args = [args for args in parsed_file["__args__"] if args["_name"] == name][0]
    args = generate.generate_args(called_args)

    if cmd is None:
        print(" ".join(args))
    else:
        subprocess.Popen(f"{cmd} {' '.join(args)}", shell=True)


@app.command("list")
def list_command(file: pathlib.Path):
    from rich import print

    parsed_yaml = yaml.safe_load(open(file, "r"))

    print(parsed_yaml)


def main():
    if len(sys.argv) == 1:
        typer.echo("No arguments or file_names provided.")
        exit(1)

    if sys.argv[1] not in ("generate", "list"):
        sys.argv.insert(1, "generate")

    app()


if __name__ == "__main__":
    main()
