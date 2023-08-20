from datetime import timedelta
from enum import Enum
from typing import Optional

import numpy as np
from pydantic import PositiveFloat
from pydantic import confloat
from pydantic import conint
from pydantic import conlist
from pydantic import root_validator

from ..base.shepherd import ShpModel
from ..testbed.gpio import GPIO


class PowerTracing(ShpModel, title="Config for Power-Tracing"):
    """Configuration for recording the Power-Consumption of the Target Nodes
    TODO: postprocessing not implemented ATM
    """

    intermediate_voltage: bool = False
    # ⤷ for EMU: record buffer capacitor instead of output (good for V_out = const)
    #            this also includes current!

    # time
    delay: timedelta = 0  # seconds
    duration: Optional[timedelta] = None  # till EOF

    # post-processing
    calculate_power: bool = False
    samplerate: conint(ge=10, le=100_000) = 100_000  # down-sample
    discard_current: bool = False
    discard_voltage: bool = False
    # ⤷ reduce file-size by omitting current / voltage

    @root_validator(pre=False)
    def post_validation(cls, values: dict) -> dict:
        if values.get("delay") and values["delay"].total_seconds() < 0:
            raise ValueError("Delay can't be negative.")
        if values.get("duration") and values["duration"].total_seconds() < 0:
            raise ValueError("Duration can't be negative.")

        discard_all = values.get("discard_current") and values.get("discard_voltage")
        if not values.get("calculate_power") and discard_all:
            raise ValueError(
                "Error in config -> tracing enabled, but output gets discarded"
            )
        if values.get("calculate_power"):
            raise ValueError("postprocessing not implemented ATM")
        return values


class GpioTracing(ShpModel, title="Config for GPIO-Tracing"):
    """Configuration for recording the GPIO-Output of the Target Nodes
    TODO: postprocessing not implemented ATM
    """

    # initial recording
    mask: conint(ge=0, lt=2**10) = 0b11_1111_1111  # all
    # ⤷ TODO: custom mask not implemented
    gpios: Optional[conlist(item_type=GPIO, min_items=1, max_items=10)]  # = all
    # ⤷ TODO: list of GPIO to build mask, one of both should be internal

    # time
    delay: timedelta = 0  # seconds
    duration: Optional[timedelta] = None  # till EOF

    # post-processing,
    uart_decode: bool = False  # todo: is currently done online by system-service
    uart_pin: GPIO = GPIO(name="GPIO8")
    uart_baudrate: conint(ge=2_400, le=921_600) = 115_200
    # TODO: add a "discard_gpio" (if only uart is wanted)

    @root_validator(pre=False)
    def post_validation(cls, values: dict) -> dict:
        if values.get("mask") == 0:
            raise ValueError("Error in config -> tracing enabled but mask is 0")
        if values.get("delay") and values["delay"].total_seconds() < 0:
            raise ValueError("Delay can't be negative.")
        if values.get("duration") and values["duration"].total_seconds() < 0:
            raise ValueError("Duration can't be negative.")
        return values


class GpioLevel(str, Enum):
    low = "L"
    high = "H"
    toggle = "X"  # TODO: not the smartest decision for writing a converter


class GpioEvent(ShpModel, title="Config for a GPIO-Event"):
    """Configuration for a single GPIO-Event (Actuation)"""

    delay: PositiveFloat
    # ⤷ from start_time
    # ⤷ resolution 10 us (guaranteed, but finer steps are possible)
    gpio: GPIO
    level: GpioLevel
    period: confloat(ge=10e-6) = 1
    # ⤷ time base of periodicity in s
    count: conint(ge=1, le=4096) = 1

    @root_validator(pre=False)
    def post_validation(cls, values: dict) -> dict:
        if not values.get("gpio").user_controllable():
            raise ValueError(
                f"GPIO '{values.get('gpio').name}' in actuation-event not controllable by user"
            )
        return values

    def get_events(self) -> np.ndarray:
        stop = self.delay + self.count * self.period
        return np.arange(self.delay, stop, self.period)


class GpioActuation(ShpModel, title="Config for GPIO-Actuation"):
    """Configuration for a GPIO-Actuation-Sequence
    TODO: not implemented ATM:
        - decide if pru control sys-gpio or
        - reverses pru-gpio (preferred if possible)
    """

    events: conlist(item_type=GpioEvent, min_items=1, max_items=1024)

    def get_gpios(self) -> set:
        return {_ev.gpio for _ev in self.events}


class SystemLogging(ShpModel, title="Config for System-Logging"):
    """Configuration for recording Debug-Output of the Observers System-Services"""

    dmesg: bool = True
    ptp: bool = True
    shepherd: bool = True


# TODO: some more interaction would be good
#     - execute limited python-scripts
#     - send uart-frames
