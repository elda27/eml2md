from datetime import datetime
import logging
from pathlib import Path
from re import M
from typing import Dict, List, Literal, Optional, TypedDict, Union
import eml_parser

_logger = logging.getLogger(__name__)

ContentHeader = TypedDict(
    "ContentHeader",
    {
        "content-language": str,
        "content-disposition": List[str],
        "content-transfer-encoding": List[str],
        "content-type": List[str],
        "x-attachment-id": List[str],
        "content-id": List[str],
    },
)

Body = TypedDict(
    "Body",
    {
        "content_header": ContentHeader,
        "html": Optional[str],
        "content_type": str,
        "content": str,
        "uri": List[str],
        "uri_noscheme": List[str],
        "email": List[str],
        "domain": List[str],
        "hash": str,
        "boundary": str,
    },
)

Header = TypedDict(
    "Header",
    {
        "received": List[str],
        "received_src": Optional[str],
        "from": str,
        "to": List[str],
        "cc": List[str],
        "subject": str,
        "received_foremail": List[str],
        "date": datetime,
        "header": Dict[str, str],
        "mime-version": List[str],
        "message-id": List[str],
    },
)

Content = TypedDict(
    "Content", {"with": str, "for": List[str], "by": List[str], "date": str, "src": str}
)

Hash = TypedDict("Hash", {"md5": str, "sha1": str, "sha256": str, "sha512": str})

Attachment = TypedDict(
    "Attachment",
    {
        "filename": str,
        "size": int,
        "extension": str,
        "hash": Hash,
        "content_header": ContentHeader,
        "raw": bytes,
    },
)

EMail = TypedDict(
    "EMail",
    {
        "body": List[Body],
        "header": Header,
        "received_domain": List[str],
        "received": List[Content],
        "attachment": List[Attachment],
    },
)


def parse_eml(eml_path: Path) -> EMail:
    contents = eml_parser.EmlParser(
        include_attachment_data=True, include_raw_body=True
    ).decode_email_bytes(eml_path.read_bytes())
    return contents
