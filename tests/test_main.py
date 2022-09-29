from pathlib import Path

import pytest
from unittest.mock import patch

from eml2md.markdown import format_markdown
from eml2md.eml import parse_eml
from eml2md._main import main

example_dir = Path(__file__).parent / "example"
eml_files = list(example_dir.glob("*.eml"))


@pytest.mark.parametrize("eml_path", eml_files, ids=[file.name for file in eml_files])
def test_simple_formatter(eml_path: Path):
    test_file = eml_path.with_suffix(".test.md")
    current_file = eml_path.with_suffix(".current.md")

    with patch(
        "sys.argv",
        ["eml2md", "-i", str(eml_path.absolute()), "-o", str(current_file.absolute())],
    ):
        main()

    result = current_file.read_text()
    if not test_file.exists():
        test_file.write_text(result)
    assert test_file.read_text() == current_file.read_text()
