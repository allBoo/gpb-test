import typer

from application import setup_app
from application.ports.cli import importer

app = typer.Typer(no_args_is_help=True)

app.callback()(setup_app)
importer.register(app)

def run():
    app()


__all__ = ['run']
