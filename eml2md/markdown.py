import typing
from typing import List, Optional, Tuple

from eml2md.eml import Body, EMail, Header
from eml2md.misc import parse_content_type


class Formatter:
    if typing.TYPE_CHECKING:
        mail: EMail

    def format(self, mail: EMail) -> str:
        """Format mail

        Parameters
        ----------
        mail : EMail
            mail to format

        Returns
        -------
        str
            formatted string
        """
        self.mail = mail
        return (
            self.format_header(mail["header"])
            + "\n\n"
            + self.format_bodies(mail["body"])
        )

    def format_bodies(self, bodies: List[Body]) -> str:
        """Format all bodies

        Parameters
        ----------
        bodies : List[Body]
            List of body of email.

        Returns
        -------
        str
            formatted bodies
        """
        return "\n".join(
            self.format_body(body) for body in bodies if self.is_supported_content(body)
        )

    def format_header(self, header: Header) -> str:
        raise NotImplementedError()

    def format_body(self, body: Body) -> str:
        """Format a body

        Parameters
        ----------
        body : Body
            body of email

        Returns
        -------
        str
            formatted body
        """
        raise NotImplementedError()

    def is_supported_content(self, body: Body) -> bool:
        """Check the content type of the body

        Parameters
        ----------
        body : Body
            testing body

        Returns
        -------
        bool
            True if the content type is supported on this formatter.
        """
        return True


class SimpleFormatter(Formatter):
    def format_header(self, header: Header) -> str:
        return "\n".join(
            [
                "|||",
                "|---|---|",
                "|From|{}|".format(self._format_mail_addr(header["from"])),
                "|To|{}|".format(
                    "<br>".join([self._format_mail_addr(addr) for addr in header["to"]])
                ),
                "|CC|{}|".format(
                    "<br>".join([self._format_mail_addr(addr) for addr in header["cc"]])
                ),
                "|Date|{}|".format(header["date"].strftime("%Y-%m-%d %H:%M:%S")),
                "|Subject|{}|".format(header["subject"]),
            ]
        )

    def format_body(self, body: Body) -> str:
        content = body["content"]
        content = self._replace_attachments(content)
        return self._strip_content(content)

    def _format_mail_addr(self, mail_addr: Tuple[str, str]) -> str:
        """Format mail address

        Parameters
        ----------
        mail_addr : str
            mail address

        Returns
        -------
        str
            formatted mail address
        """
        name, addr = mail_addr
        return "{} <{}>".format(name, addr)

    def _replace_attachments(self, content: str) -> str:
        """Replace attachments in the content

        Parameters
        ----------
        content : str
            Content a part of mail bodies

        Returns
        -------
        str
            Content with replaced attachments
        """
        from base64 import b64encode, b64decode

        for attachment in self.mail["attachment"]:
            content_header = attachment["content_header"]
            if content_header is None:
                continue  # Ignore an attachment

            for content_type_str in content_header["content_type"]:
                content_type = parse_content_type(content_type_str)
                if content_type["type"] == "image":
                    name = content_type["parameters"]["name"]
                    content = content.replace(
                        "[image: {}]".format(name),
                        "![{}]({})".format(
                            name,
                            "data:{}/{};base64,".format(
                                content_type["type"], content_type["sub_type"]
                            )
                            + b64encode(attachment["raw"]).decode("utf-8"),
                        ),
                    )
        return content

    def _strip_content(self, content: str) -> str:
        """Strip the \r\n delimiters inserted at the end of each line
        according to the specification of eml files.

        Parameters
        ----------
        content : str
            Content string

        Returns
        -------
        str
            delimiters stripped content string
        """
        return content.replace("\r\n\r\n", "\n").replace("\r\n", "\n")

    def is_supported_content(self, body: Body) -> bool:
        return "text/plain" == body["content_type"]


class SimpleHTMLFormatter(SimpleFormatter):
    def is_supported_content(self, body: Body) -> bool:
        return "text/plain" == body["content_type"]


def create_formatter(formatter: Optional[str] = None) -> Formatter:
    if formatter is None or formatter == "simple":
        return SimpleFormatter()
    elif formatter == "html":
        return SimpleHTMLFormatter()
    else:
        raise NotImplementedError(f"Not implemented formatter: {formatter}")


def format_markdown(mail: EMail, formatter: Optional[str] = None) -> str:
    return create_formatter(formatter).format(mail)
