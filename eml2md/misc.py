from typing import Dict, TypedDict


ContentType = TypedDict(
    "ContentType",
    {
        "type": str,
        "sub_type": str,
        "parameters": Dict[str, str],
    },
)


def parse_content_type(content_type: str) -> ContentType:
    """Parsing MIME content type.

    Parameters
    ----------
    content_type : str
        Content type of the body.

    Returns
    -------
    ContentType
        List of MIME type.
    """

    parameters = {}
    tokens = [token.strip() for token in content_type.split(";")]
    main_type, sub_type = tokens[0].split("/")
    for token in tokens[1:]:
        key, val = token.split("=")
        parameters[key] = val.strip('"')
    return {"type": main_type, "sub_type": sub_type, "parameters": parameters}
