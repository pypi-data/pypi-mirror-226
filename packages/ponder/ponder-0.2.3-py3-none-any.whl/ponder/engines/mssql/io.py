from __future__ import annotations

import logging

from modin.core.io.io import BaseIO

client_logger = logging.getLogger("client logger")


class MSSQLIO(BaseIO):
    pass
