from argparse import ArgumentParser
from pathlib import Path
from secrets import choice
from typing import NamedTuple
from eml2md.markdown import format_markdown
from eml2md.eml import parse_eml


class Args(NamedTuple):
    input: Path
    output: Path
    format: str


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, required=True, help="Input file")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output file")
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["simple", "html"],
        default="simple",
        required=False,
        help="Format of output markdown",
    )
    args: Args = parser.parse_args()

    args.output.write_text(
        format_markdown(parse_eml(args.input), formatter=args.format)
    )


if __name__ == "__main__":
    main()
