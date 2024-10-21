import logging
from datetime import datetime

from maillog.data.models.maillog import MailLog, MessageType

logger = logging.getLogger(__name__)


class ParserException(Exception):
    pass


class MailLogParser:

    @classmethod
    def from_string(cls, string: str) -> MailLog | None:
        parts = string.split(' ')
        if len(parts) < 3:
            raise ParserException("too few parts")

        date_str, time_str, internal_id, flag_str = parts[:4]
        remaining = parts[2:]

        try:
            date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ParserException("invalid date/time")

        flag = MessageType(flag_str) if flag_str in MessageType else MessageType.other

        address = None
        if flag != MessageType.other:
            address = parts[4]
            if address == ':blackhole:':
                address = parts[5]
            address = address.strip('<>')
            if not address:
                address = None

            # TODO validate email address

        str_id = None
        if flag == MessageType.incoming:
            for chunk in parts[4:]:
                if chunk.startswith('id='):
                    str_id = chunk[3:]
                    break

        return MailLog(
            type=flag,
            date=date_time,
            message=' '.join(remaining),
            int_id=internal_id,
            address=address,
            id=str_id,
        )
