from pathlib import Path
import pytest
from eml2md.markdown import format_markdown
from eml2md.eml import parse_eml

example_dir = Path(__file__).parent / "example"


@pytest.mark.parametrize("eml_path", list(example_dir.glob("*.eml")))
def test_simple_formatter(eml_path: Path):
    test_file = eml_path.with_suffix(".test.md")
    current_file = eml_path.with_suffix(".current.md")
    result = format_markdown(parse_eml(eml_path), formatter="simple")
    if not test_file.exists():
        test_file.write_text(result)
    current_file.write_text(result)
    assert test_file.read_text() == result
