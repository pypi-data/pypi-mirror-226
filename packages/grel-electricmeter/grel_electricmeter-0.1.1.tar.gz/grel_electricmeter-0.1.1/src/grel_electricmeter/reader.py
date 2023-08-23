"""Grelinfo Electric Meter Reader."""

from logging import getLogger
from time import time

import serial
from serial import Serial, SerialException

from grel_electricmeter.models import ElectricMeterReadDTO
from grel_electricmeter.sml import electric_meter_data_from_sml_message

_HELLO_MESSAGE = b"\x2F\x3F\x21\x0D\x0A"
_START_MESSAGE = b"\x02"
_END_MESSAGE = b"\x03"


logger = getLogger(__name__)


class ElectricMeterReader:  # pylint: disable=too-few-public-methods
    """Electric Meter Reader."""

    def __init__(self, port: str):
        """Initialize.

        Args:
            port: The serial port to use.
        """
        self._serial = Serial(
            # Don't open the serial port automatically by setting the port later
            port=None,
            baudrate=300,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )

        self._serial.port = port

    def read(self) -> ElectricMeterReadDTO:
        """Read the electric meter."""
        logger.info("Start reading electric meter")
        start_time = time()
        try:
            self._open()
            self._send_hello()
            self._wait_start()
            message = self._read_message()
            data = self._parse_message(message)
        except SerialException as exc:
            logger.error("Error while reading electric meter: %s", exc)
            raise
        finally:
            self._close()

        end_time = time()
        duration = int(end_time - start_time)
        logger.info("Finished reading electric meter ( took %ds )", duration)

        return data

    # Private methods --------------------------------------------------------------------------------------------------

    def _open(self):
        """Open the serial connection to the electric meter if not open."""
        logger.info("Open serial port")
        # Don't open the serial port if it is already open
        if self._serial.is_open:
            logger.debug("Serial port already open")
            return

        # Open the serial port
        self._serial.open()
        logger.debug("Serial port opened")

    def _close(self):
        """Close the serial connection to the electric meter if open."""
        logger.info("Close serial port")
        # Don't close the serial port if it is already closed
        if not self._serial.is_open:
            logger.debug("Serial port already closed")
            return

        # Close the serial port
        self._serial.close()
        logger.debug("Serial port closed")

    def _send_hello(self):
        """Send the hello message to the electric meter to start the communication."""
        logger.info("Send hello")
        self._serial.write(_HELLO_MESSAGE)
        logger.debug("Hello sent")

    def _wait_start(self):
        """Wait for the start byte of SML message."""
        logger.info("Wait for start message")
        self._serial.read_until(_START_MESSAGE)
        logger.debug("Start message received")

    def _read_message(self) -> bytes:
        """Read the SML message."""
        logger.info("Read SML message")
        message = self._serial.read_until(_END_MESSAGE)
        logger.debug("SML message read")

        return message

    def _parse_message(self, message: bytes) -> ElectricMeterReadDTO:
        """Parse the SML message."""
        logger.info("Parse SML message")
        data = electric_meter_data_from_sml_message(message)
        logger.debug("SML message parsed")

        return data
