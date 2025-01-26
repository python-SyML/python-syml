import subprocess
from pathlib import Path

import click


@click.group()
def cli():
    pass


@click.command()
def presentation():
    click.echo("""
               Welcome, dear user of SyML !
               SyML is equipped with a Command Line Interface (CLI).

               If you are facing any difficulty at any point, please use the option --help.
               """)


@click.command()
def run():
    """Run the SyML application."""
    path = Path(__file__).resolve()
    if path.match("**/src/**/*.py"):
        main_dir, _ = str(path).split("src")
        path = Path(main_dir) / Path("src/syml/app/streamlit_app.py")
    subprocess.run(["streamlit", "run", path])


cli.add_command(run)
cli.add_command(presentation)

if __name__ == "__main__":
    cli()
