from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TbPagination:
    """Thingsboard pagitation data.

    python-instalation/site-packages/tb_rest_client/models/models_ce/page_data_*.py

    from tb_rest_client.models.models_ce.page_data_device import PageDataDevice  # CE-PE
    """
    data: list  # can't be more specific
    total_pages: int
    total_elements: int
    has_next: bool


@dataclass
class TBTelemetry(ABC):
    """Telemetry data used to send to Thingsboard.

    Define only the attributes that will be sent as telemetry.
    So, attributes like id must no be included.

    .. code-block::

        # Has the desired attrs only.

        class MyTelemetry(Telemetry):
            dimmer: float
            light: bool
    """
    ...


@dataclass
class VendorTelemetry(ABC):
    """Vendor data Telemetry.

    Define the vendor telemetry data you wish to use.
    It depends on data returned by the vendor and the
    data you wish to include.

    Attributes:
        vendor_id: Use as ID that vendor handle.
            The type of ID can be many types: int, str, UUIDs, etc.

    .. code-block::

        class MyVendorTelemetry(VendorTelemetry):
            vendor_id: str
            dimmer: float
            light: str = 'ON'
    """
    vendor_id: Any


@dataclass
class TbDevice:
    """Thingsboard Device."""
    device_id: str  # ID genereated by Thingsboard
    dtype: str  # Equivalent to Device Profile
    name: str
    access_token: Optional[str]
    telemetry: Optional[TBTelemetry] = None
    entity_type: str = 'DEVICE'
    vendor_id: str = ''
