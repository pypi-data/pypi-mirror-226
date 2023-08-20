from pydantic import BaseModel


class BaseData(BaseModel):
    identifier: str | None


class SolarData(BaseData):
    """This model represents data from solar panels"""
    ...


class SolarPanelInverterData(BaseData):
    ...


class P1Data(BaseData):
    """This model represents the data from a P1 DSMR meter"""
    # Meter info
    meter_model: str | None

    # Totals
    total_power_import_kwh: float
    total_power_import_t1_kwh: float | None
    total_power_import_t2_kwh: float | None
    total_power_export_kwh: float
    total_power_export_t1_kwh: float | None
    total_power_export_t2_kwh: float | None

    # Active power
    active_power_w: float
    active_power_l1_w: float | None
    active_power_l2_w: float | None
    active_power_l3_w: float | None


__all__ = (
    "BaseData",
    "SolarData",
    "P1Data",
)
