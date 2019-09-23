from nmigen.build import *


__all__ = ["UserLEDResource"]


def _SplitResources(*args, pins, invert=False, attrs=None, default_name, dir):
    assert isinstance(pins, (str, list, dict))

    if isinstance(pins, str):
        pins = pins.split()
    if isinstance(pins, list):
        pins = dict(enumerate(pins))

    resources = []
    for number, pin in pins.items():
        ios = [PinsN(pin, dir=dir) if invert else Pins(pin, dir=dir)]
        if attrs is not None:
            ios.append(attrs)
        resources.append(Resource.family(*args, number, default_name=default_name, ios=ios))
    return resources


def LEDResources(*args, **kwargs):
    return _SplitResources(*args, **kwargs, default_name="led", dir="o")


def RGBLEDResource(*args, r, g, b, invert=False, attrs=None):
    ios = []
    ios.append(Subsignal("r", Pins(r, dir="o", assert_width=1)))
    ios.append(Subsignal("g", Pins(g, dir="o", assert_width=1)))
    ios.append(Subsignal("b", Pins(b, dir="o", assert_width=1)))
    if attrs is not None:
        ios.append(attrs)
    return Resource.family(*args, default_name="rgb_led", ios=ios)


def ButtonResources(*args, **kwargs):
    return _SplitResources(*args, **kwargs, default_name="button", dir="i")


def SwitchResources(*args, **kwargs):
    return _SplitResources(*args, **kwargs, default_name="switch", dir="i")
