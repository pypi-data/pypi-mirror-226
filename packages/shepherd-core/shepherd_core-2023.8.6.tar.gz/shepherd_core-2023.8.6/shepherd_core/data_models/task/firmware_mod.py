import copy
from pathlib import Path
from typing import Optional
from typing import Union

from pydantic import conint
from pydantic import constr
from pydantic import root_validator
from pydantic import validate_arguments

from ...logger import logger
from ..base.content import IdInt
from ..base.shepherd import ShpModel
from ..content.firmware import Firmware
from ..content.firmware import FirmwareDType
from ..experiment.experiment import Experiment
from ..testbed import Testbed
from ..testbed.target import IdInt16
from ..testbed.target import MCUPort


class FirmwareModTask(ShpModel):
    """Config for Task that adds the custom ID to the firmware & stores it into a file"""

    data: Union[constr(min_length=3, max_length=8_000_000), Path]
    data_type: FirmwareDType
    custom_id: Optional[IdInt16]
    firmware_file: Path

    verbose: conint(ge=0, le=4) = 2
    # ⤷ 0=Errors, 1=Warnings, 2=Info, 3=Debug

    @root_validator(pre=False)
    def post_validation(cls, values: dict) -> dict:
        if values.get("data_type") in [
            FirmwareDType.base64_hex,
            FirmwareDType.path_hex,
        ]:
            logger.warning(
                "Firmware is scheduled to get custom-ID but is not in elf-format"
            )
        return values

    @classmethod
    @validate_arguments
    def from_xp(
        cls,
        xp: Experiment,
        tb: Testbed,
        tgt_id: IdInt,
        mcu_port: MCUPort,
        fw_path: Path,
    ):
        tgt_cfg = xp.get_target_config(tgt_id)

        fw = tgt_cfg.firmware1 if mcu_port == 1 else tgt_cfg.firmware2
        if fw is None:
            return None

        fw_id = tgt_cfg.get_custom_id(tgt_id)
        if fw_id is None:
            obs = tb.get_observer(tgt_id)
            fw_id = obs.get_target(tgt_id).fw_id

        return cls(
            data=fw.data,
            data_type=fw.data_type,
            custom_id=fw_id,
            firmware_file=copy.copy(fw_path),
        )

    @classmethod
    @validate_arguments
    def from_firmware(cls, fw: Firmware, **kwargs):
        kwargs["data"] = fw.data
        kwargs["data_type"] = fw.data_type
        fw.compare_hash()
        path = kwargs.get("firmware_file")
        if path is not None and path.is_dir():
            path_new: Path = path / fw.name
            kwargs["firmware_file"] = path_new.with_suffix(".hex")
        return cls(**kwargs)
