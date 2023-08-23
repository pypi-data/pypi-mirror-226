"""Grelinfo Electric Meter Configuration."""

from pydantic import BaseModel


class ElectricMeterConfig(BaseModel, extra="forbid", frozen=True):
    """Electric Meter Configuration.

    Async application, that run serial blocking methods in a thread.
    """

    port: str
