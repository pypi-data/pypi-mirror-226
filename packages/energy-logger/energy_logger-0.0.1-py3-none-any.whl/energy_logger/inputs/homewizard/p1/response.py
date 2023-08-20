from pydantic import BaseModel

from energy_logger.models import P1Data


class HomeWizardP1Response(BaseModel):
    wifi_ssid: str
    wifi_strength: int
    smr_version: int
    meter_model: str
    unique_id: str
    active_tariff: int
    total_power_import_kwh: float
    total_power_import_t1_kwh: float
    total_power_import_t2_kwh: float
    total_power_export_kwh: float
    total_power_export_t1_kwh: float
    total_power_export_t2_kwh: float
    active_power_w: int
    active_power_l1_w: int
    active_power_l2_w: int
    active_power_l3_w: int
    active_voltage_l1_v: float
    active_voltage_l2_v: float
    active_voltage_l3_v: float
    active_current_l1_a: float
    active_current_l2_a: float
    active_current_l3_a: float
    voltage_sag_l1_count: int
    voltage_sag_l2_count: int
    voltage_sag_l3_count: int
    voltage_swell_l1_count: int
    voltage_swell_l2_count: int
    voltage_swell_l3_count: int
    any_power_fail_count: int
    long_power_fail_count: int
    external: list

    def __str__(self) -> str:
        meter_model = self.meter_model
        active_power_w = self.active_power_w
        total_power_import_kwh = self.total_power_import_kwh
        total_power_export_kwh = self.total_power_export_kwh

        return (
          f"HomeWizard P1 API response. "
          f"{meter_model=}, {active_power_w=} "
          f"{total_power_import_kwh=} {total_power_export_kwh=}"
        )

    def to_p1data(self) -> P1Data:
        return P1Data(
            meter_model=self.meter_model,
            identifier=self.unique_id,
            total_power_import_kwh=self.total_power_import_kwh,
            total_power_import_t1_kwh=self.total_power_import_t1_kwh,
            total_power_import_t2_kwh=self.total_power_import_t2_kwh,
            total_power_export_kwh=self.total_power_export_kwh,
            total_power_export_t1_kwh=self.total_power_export_t1_kwh,
            total_power_export_t2_kwh=self.total_power_export_t2_kwh,
            active_power_w=self.active_power_w,
            active_power_l1_w=self.active_power_l1_w,
            active_power_l2_w=self.active_power_l2_w,
            active_power_l3_w=self.active_power_l3_w,
        )
