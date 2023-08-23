"""Grelinfo Electric Meter Models."""


from pydantic import BaseModel


class ElectricMeterReadDTO(BaseModel):
    """Electric Meter Read DTO."""

    consum_energy_peak: float
    consum_energy_offpeak: float
    return_energy: float
    power_phase_1: float
    power_phase_2: float
    power_phase_3: float

    @property
    def power(self) -> float:
        """Get the total instantaneous power.

        The sum of the instantaneous power of all phases.
        """
        return self.power_phase_1 + self.power_phase_2 + self.power_phase_3
