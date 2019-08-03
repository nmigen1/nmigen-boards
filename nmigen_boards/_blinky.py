import itertools

from nmigen import *
from nmigen.build import ResourceError


class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        clk = platform.request(platform.default_clk)
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)

        leds = []
        for n in itertools.count():
            try:
                leds.append(platform.request("user_led", n))
            except ResourceError:
                break
        leds = Cat(led.o for led in leds)

        clk_freq = platform.default_clk_frequency
        ctr = Signal(max=int(clk_freq//2), reset=int(clk_freq//2) - 1)
        with m.If(ctr == 0):
            m.d.sync += ctr.eq(ctr.reset)
            m.d.sync += leds.eq(~leds)
        with m.Else():
            m.d.sync += ctr.eq(ctr - 1)

        return m


def build_and_program(platform_cls, **kwargs):
    platform_cls().build(Blinky(), do_program=True, **kwargs)
