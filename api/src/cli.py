import typer
from fastapi_cli.cli import app as FastAPICLIApp

from application import setup_app

app = typer.Typer(no_args_is_help=True)

app.callback()(setup_app)

app.add_typer(FastAPICLIApp, name='api')

def run():
    app()


__all__ = ['run']
