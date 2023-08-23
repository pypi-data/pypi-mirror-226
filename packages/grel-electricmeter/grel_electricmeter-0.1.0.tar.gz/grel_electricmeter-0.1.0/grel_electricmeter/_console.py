"""Grelinfo Electric Meter Console."""
# pylint: disable=import-outside-toplevel

import sys

try:
    from typer import Typer, echo
except ImportError:
    print("Error: Please install grel-elecricmeter[console] to use the console.")
    sys.exit(1)

app = Typer()


@app.command()
def read(port: str):
    """Read the electric meter."""
    # Import here to only load the reader when needed
    from grel_electricmeter import ElectricMeterReader

    data = ElectricMeterReader(port=port).read()

    echo(data.model_dump_json(indent=4))


@app.callback()
def main():
    """Grelinfo Electric Meter Console."""
