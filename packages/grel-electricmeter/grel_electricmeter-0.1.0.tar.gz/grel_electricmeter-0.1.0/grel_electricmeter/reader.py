"""Grelinfo Electric Meter Reader."""

from logging import getLogger
from time import time

import serial
from serial import Serial, SerialException

from grel_electricmeter.models import ElectricMeterData
from grel_electricmeter.obis import electric_meter_data_from_obis

__HELLO_MESSAGE = b"\x2F\x3F\x21\x0D\x0A"
__START_MESSAGE = b"\x02"
__END_MESSAGE = b"\x03"


logger = getLogger(__name__)


class ElectricMeterReader:  # pylint: disable=too-few-public-methods
    """Electric Meter Reader."""

    def __init__(self, port: str):
        """Initialize.

        Args:
            port: The serial port to use.
        """

        self.serial = Serial(
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

        self.serial.port = port

    def read(self) -> ElectricMeterData:
        """Read the electric meter."""

        logger.info("Start reading electric meter")
        start_time = time()
        try:
            self.__open()
            self.__send_hello()
            self.__wait_start()
            message = self.__read_message()
            data = self.__parse_message(message)
            self.__close()
        except SerialException as exc:
            logger.error("Error while reading electric meter: %s", exc)
            raise

        end_time = time()
        duration = int(end_time - start_time)
        logger.info("Finished reading electric meter ( took %ds )", duration)

        return data

    # Private methods --------------------------------------------------------------------------------------------------

    def __open(self):
        """Open the serial connection to the electric meter if not open."""

        logger.info("Open serial port")
        # Don't open the serial port if it is already open
        if self.serial.is_open:
            logger.debug("Serial port already open")
            return

        # Open the serial port
        self.serial.open()
        logger.debug("Serial port opened")

    def __close(self):
        """Close the serial connection to the electric meter if open."""

        logger.info("Close serial port")
        # Don't close the serial port if it is already closed
        if not self.serial.is_open:
            logger.debug("Serial port already closed")
            return

        # Close the serial port
        self.serial.close()
        logger.debug("Serial port closed")

    def __send_hello(self):
        """ "Send the hello message to the electric meter to start the communication."""
        logger.info("Send hello")
        self.serial.write(__HELLO_MESSAGE)
        logger.debug("Hello sent")

    def __wait_start(self):
        """Wait for the start byte of SML message."""

        logger.info("Wait for start message")
        self.serial.read_until(__START_MESSAGE)
        logger.debug("Start message received")

    def __read_message(self) -> bytes:
        """Read the SML message."""

        logger.info("Read SML message")
        message = self.serial.read_until(__END_MESSAGE)
        logger.debug("SML message read")

        return message

    def __parse_message(self, message: bytes) -> ElectricMeterData:
        """Parse the SML message."""

        logger.info("Parse SML message")
        data = electric_meter_data_from_obis(message)
        logger.debug("SML message parsed")

        return data
