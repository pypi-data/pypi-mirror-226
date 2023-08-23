""" shil.__main__
"""

from pathlib import Path

from fleks import app, cli
from fleks.util import lme

from . import fmt

LOGGER = lme.get_logger(__name__)


@cli.click.group(name=Path(__file__).parents[0].name)
def entry():
    """CLI tool for `shil` library"""


DEFAULT_INPUT_FILE = "/dev/stdin"


# @cli.click.argument("filename", default=DEFAULT_INPUT_FILE)
@cli.click.flag("--rich", help="use rich output")
@entry.command
def invoke(
    rich: bool = False,
) -> None:
    """Invocation tool for (line-oriented) bash"""


def report(output, rich=False) -> None:
    if rich:
        lme.CONSOLE.print(
            app.Syntax(
                output,
                "bash",
                word_wrap=True,
            )
        )
    else:
        print(output)


@entry.command(name="fmt")
@cli.click.argument("filename", default=DEFAULT_INPUT_FILE)
@cli.click.flag("--rich", help="use rich output")
def _fmt(
    filename: str = DEFAULT_INPUT_FILE,
    rich: bool = False,
) -> None:
    """
    Pretty-printer for (line-oriented) bash
    """
    if filename == "-":
        filename = DEFAULT_INPUT_FILE
    try:
        with open(filename) as fhandle:
            text = fhandle.read()
    except FileNotFoundError:
        LOGGER.warning(f"input @ {filename} is not a file; parsing as string")
        text = filename
    return report(fmt(text), rich=rich)


if __name__ == "__main__":
    entry()
