from datetime import datetime
import logging
from pathlib import Path
from re import M
from typing import Dict, List, Literal, Optional, Tuple, TypedDict, cast

_logger = logging.getLogger(__name__)

ContentHeader = TypedDict(
    "ContentHeader",
    {
        "content_type": List[str],
        "content_id": Optional[str],
    },
)

Body = TypedDict(
    "Body",
    {
        "content_header": Optional[ContentHeader],
        "content_type": str,
        "content": str,
    },
)

User = Tuple[str, str]
Header = TypedDict(
    "Header",
    {
        "from": User,
        "to": List[User],
        "cc": List[User],
        "subject": str,
        "date": datetime,
        "header": Dict[str, str],
    },
)

Content = TypedDict(
    "Content", {"with": str, "for": List[str], "by": List[str], "date": str, "src": str}
)

Attachment = TypedDict(
    "Attachment",
    {
        "content_header": Optional[ContentHeader],
        "raw": bytes,
    },
)

EMail = TypedDict(
    "EMail",
    {
        "body": List[Body],
        "header": Header,
        "attachment": List[Attachment],
    },
)

import email
from email.message import Message
from email.header import decode_header
from email.utils import getaddresses, parsedate_to_datetime


def _decode_token(token: str) -> str:
    if not token.startswith("=?"):
        return token
    decoded, encoding = decode_header(token)[0]
    return decoded.decode(encoding or "utf-8")


def _parse_payload(part: Message) -> Tuple[List[Body], List[Attachment]]:
    """"""
    bodies = []
    attachments = []
    if part.get_content_maintype() == "multipart":
        for sub_part in part.get_payload():
            sub_bodies, sub_attachments = _parse_payload(sub_part)
            bodies.extend(sub_bodies)
            attachments.extend(sub_attachments)
    elif part.get_content_type() in ("text/plain", "text/html"):
        bodies.append(
            {
                "content": part.get_payload(decode=True).decode("utf-8"),
                "content_type": part.get_content_type(),
                "content_header": {
                    "content_type": [part["Content-Type"]],
                    "content_id": part["content-id"],
                },
            }
        )
    elif part.get_content_disposition() == "attachment":
        attachments.append(
            {
                "raw": part.get_payload(decode=True),
                "content_header": {
                    "content_type": [part["Content-Type"]],
                    "content_id": part["content-id"],
                },
            }
        )
    else:
        raise NotImplementedError(f"Not implemented payload: {str(part)}")
    return bodies, attachments


def parse_eml(eml_path: Path) -> EMail:
    eml = email.message_from_bytes(eml_path.read_bytes())
    if eml.get_content_maintype() != "multipart":
        raise NotImplementedError(
            "Not implemented yet: root mime type {}".format(eml.get_content_type())
        )
    bodies, attachments = _parse_payload(eml)
    header: Header = {}  # type:ignore

    for key in [
        "from",
        "to",
        "cc",
    ]:
        key = cast(
            Literal["from", "to", "cc"], key
        )  # Due to insufficient type recognization of mypy
        data = eml.get(key)
        if data is None:
            header[key] = []
        else:
            users = [
                (_decode_token(token), address)
                for token, address in getaddresses([eml.get(key)])
            ]
            if key != "from":
                header[key] = users
            else:
                header[key] = users[0]

    header["subject"] = _decode_token(eml.get("subject"))
    header["date"] = parsedate_to_datetime(eml.get("date"))

    return {"body": bodies, "header": header, "attachment": attachments}


# def parse_eml(eml_path: Path) -> EMail:
#     contents = eml_parser.EmlParser(
#         include_attachment_data=True, include_raw_body=True
#     ).decode_email_bytes(eml_path.read_bytes())
#     return contents
