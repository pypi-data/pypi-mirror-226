"""
Manager writing to either StringIO or to a CSV file.
  - Trc20Txns are written as CSVs
  - TronEvents are written as JSON
"""
import csv
import json
from abc import abstractmethod
from typing import Any, List, Type

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import *
from trongrid_extractoor.models.trc20_txn import CSV_FIELDS, Trc20Txn
from trongrid_extractoor.models.tron_event import TronEvent

LOG_INTERVAL = 4000


class OutputWriter:
    def __init__(self, output_cls: Type) -> None:
        self.output_cls = output_cls
        self.lines_written = 0

    def write_rows(self, rows: List[Any]) -> None:
        """Write json or CSV."""
        if len(rows) == 0:
            logging.warning(f"Nothing to write (0 rows)...")
            return

        log.info(f"Writing {len(rows)} rows...")

        if self.output_cls == Trc20Txn:
            self.write_txns(rows)
        else:
            self.write_json(rows)

        self.lines_written += len(rows)

        if self.lines_written % LOG_INTERVAL == 0:
            log.info(f"  Timestamp: {rows[0].datetime}")

    @abstractmethod
    def write_txns(self, rows: List[Trc20Txn]) -> None:
        pass

    @abstractmethod
    def write_json(self, rows: List[TronEvent]) -> None:
        pass

    def _write_txns(self, rows: List[Trc20Txn], writeable_io) -> None:
        """Txns are written to a CSV with particular columns."""
        csv_writer = csv.DictWriter(writeable_io, CSV_FIELDS, lineterminator='\n')

        if self.file_mode == 'w':
            csv_writer.writeheader()

        csv_writer.writerows([row.as_dict(CSV_FIELDS) for row in rows])
        self.file_mode = 'a'

    def _write_json(self, rows: List[TronEvent], writeable_io) -> None:
        json.dump([row.raw_event for row in rows], writeable_io, indent=3)
