from typing import List, Optional
from eml2md.eml import Body, EMail, Header


class Formatter:
    def format(self, mail: EMail) -> str:
        return (
            self.format_header(mail["header"])
            + "\n\n"
            + self.format_bodies(mail["body"])
        )

    def format_bodies(self, bodies: List[Body]) -> str:
        return "\n".join(self.format_body(body) for body in bodies)

    def format_header(self, header: Header) -> str:
        raise NotImplementedError()

    def format_body(self, body: Body) -> str:
        raise NotImplementedError()


class SimpleFormatter(Formatter):
    def format_header(self, header: Header) -> str:
        return "\n".join(
            [
                "|||",
                "|---|---|",
                "|From|{}|".format(header["from"]),
                "|To|{}|".format("<br>".join(header["to"])),
                "|CC|{}|".format("<br>".join([])),
                "|Date|{}|".format(header["date"].strftime("%Y-%m-%d %H:%M:%S")),
                "|Subject|{}|".format(header["subject"]),
            ]
        )

    def format_body(self, body: Body) -> str:
        return "{content}".format(**body)


def create_formatter(formatter: Optional[str] = None) -> Formatter:
    return SimpleFormatter()


def format_markdown(mail: EMail, formatter: Optional[str] = None) -> str:
    return create_formatter(formatter).format(mail)
