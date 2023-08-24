import click
from docsdb.mongodb import mongodb


@click.group(help="DocsDB CLI")
def cli():
    pass


@click.group()
def generate():
    pass


generate.add_command(mongodb)

cli.add_command(generate)


if __name__ == "__main__":
    cli()
