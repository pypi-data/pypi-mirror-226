"""Grelinfo Electric Meter OBIS utilities."""

import re
from enum import Enum

from grel_electricmeter.models import ElectricMeterData


class ObisCode(Enum):
    """Obis Code Enum"""

    CONSUM_ENERGY_PEAK = "1-0:1.8.1*255"
    CONSUM_ENERGY_OFFPEAK = "1-0:1.8.2*255"
    RETURN_ENERGY = "1-0:2.8.0*255"
    POWER_PHASE_1 = "1-0:36.7.0*255"
    POWER_PHASE_2 = "1-0:56.7.0*255"
    POWER_PHASE_3 = "1-0:76.7.0*255"


def electric_meter_data_from_obis(raw: bytes) -> ElectricMeterData:
    """Convert ElectricMeterData from SML OBIS raw data.

    Args:
        raw: The raw SML OBIS text.

    Returns:
        The ElectricMeterData object.
    """
    text = raw.decode("ascii")

    text = text.replace("\r\n", "")
    pattern = re.compile(r"(?P<obis>[^\(]+)\((?P<value>[^\*\)]+)\*?(?P<unit>\w+)?\)")

    iterator = pattern.finditer(text)

    datadict = {}

    for match in iterator:
        groupdict = match.groupdict()
        value = groupdict["value"]
        datadict[groupdict["obis"]] = value

    return ElectricMeterData(
        consum_energy_peak=datadict[ObisCode.CONSUM_ENERGY_PEAK.value],
        consum_energy_offpeak=datadict[ObisCode.CONSUM_ENERGY_OFFPEAK.value],
        return_energy=datadict[ObisCode.RETURN_ENERGY.value],
        power_phase_1=float(datadict[ObisCode.POWER_PHASE_1.value]) * 1000,
        power_phase_2=float(datadict[ObisCode.POWER_PHASE_2.value]) * 1000,
        power_phase_3=float(datadict[ObisCode.POWER_PHASE_3.value]) * 1000,
    )
