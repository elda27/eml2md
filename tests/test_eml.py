from pathlib import Path
from typing import Any, List, Union, get_origin, get_args
import pytest
from eml2md.eml import parse_eml, EMail

example_dir = Path(__file__).parent / "example"


@pytest.mark.parametrize("eml_path", list(example_dir.glob("*.eml")))
def test_parse_eml(eml_path: Path):
    contents = parse_eml(eml_path)

    def check_annotations(values: Any, t: type, key: str = None) -> None:
        if isinstance(values, list):
            assert get_origin(t) is list
            for v in values:
                check_annotations(v, get_args(t)[0], key=key)
        elif isinstance(values, dict):
            assert get_origin(t) is None or get_origin(t) is dict
            if get_origin(t) is None:
                for k, v in values.items():
                    assert k in t.__annotations__
                    check_annotations(v, t.__annotations__[k], key=k)
        else:
            assert isinstance(values, t)
        return True

    assert check_annotations(contents, EMail)
