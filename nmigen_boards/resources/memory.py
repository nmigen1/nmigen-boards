from nmigen.build import *


__all__ = ["SPIFlashResources", "SDCardResources", "SRAMResource"]


def SPIFlashResources(*args, cs, clk, mosi, miso, wp=None, hold=None, attrs=None):
    resources = []

    io_all = []
    if attrs is not None:
        io_all.append(attrs)
    io_all.append(Subsignal("cs",  PinsN(cs, dir="o")))
    io_all.append(Subsignal("clk", Pins(clk, dir="o", assert_width=1)))

    io_1x = list(io_all)
    io_1x.append(Subsignal("mosi", Pins(mosi, dir="o", assert_width=1)))
    io_1x.append(Subsignal("miso", Pins(miso, dir="i", assert_width=1)))
    if wp is not None and hold is not None:
        io_1x.append(Subsignal("wp",   PinsN(wp,   dir="o", assert_width=1)))
        io_1x.append(Subsignal("hold", PinsN(hold, dir="o", assert_width=1)))
    resources.append(Resource.family(*args, default_name="spi_flash", ios=io_1x,
                                     name_suffix="1x"))

    io_2x = list(io_all)
    io_2x.append(Subsignal("dq", Pins(" ".join([mosi, miso]), dir="io",
                                      assert_width=2)))
    resources.append(Resource.family(*args, default_name="spi_flash", ios=io_2x,
                                     name_suffix="2x"))

    if wp is not None and hold is not None:
        io_4x = list(io_all)
        io_4x.append(Subsignal("dq", Pins(" ".join([mosi, miso, wp, hold]), dir="io",
                                          assert_width=4)))
        resources.append(Resource.family(*args, default_name="spi_flash", ios=io_4x,
                                         name_suffix="4x"))

    return resources


def SDCardResources(*args, clk, cmd, dat0, dat1=None, dat2=None, dat3=None,
                    cd=None, wp=None, attrs=None):
    resources = []

    io_common = []
    if attrs is not None:
        io_common.append(attrs)
    if cd is not None:
        io_common.append(Subsignal("cd", Pins(cd, dir="i", assert_width=1)))
    if wp is not None:
        io_common.append(Subsignal("wp", PinsN(wp, dir="i", assert_width=1)))

    io_native = list(io_common)
    io_native.append(Subsignal("clk", Pins(clk, dir="o", assert_width=1)))
    io_native.append(Subsignal("cmd", Pins(cmd, dir="o", assert_width=1)))

    io_1bit = list(io_native)
    io_1bit.append(Subsignal("dat", Pins(dat0, dir="io", assert_width=1)))
    if dat3 is not None: # works as electronic card detect
        io_1bit.append(Subsignal("ecd", Pins(dat3, dir="i", assert_width=1)))
    resources.append(Resource.family(*args, default_name="sd_card", ios=io_1bit,
                                     name_suffix="1bit"))

    if dat1 is not None and dat2 is not None and dat3 is not None:
        io_4bit = list(io_native)
        io_4bit.append(Subsignal("dat", Pins(" ".join((dat0, dat1, dat2, dat3)), dir="io",
                                             assert_width=4)))
        resources.append(Resource.family(*args, default_name="sd_card", ios=io_4bit,
                                         name_suffix="4bit"))

    if dat3 is not None:
        io_spi = list(io_common)
        io_spi.append(Subsignal("cs", PinsN(dat3, dir="io"))) # doubles as electronic card detect
        io_spi.append(Subsignal("clk", Pins(clk, dir="o", assert_width=1)))
        io_spi.append(Subsignal("mosi", Pins(cmd, dir="o", assert_width=1)))
        io_spi.append(Subsignal("miso", Pins(dat0, dir="i", assert_width=1)))
        resources.append(Resource.family(*args, default_name="sd_card", ios=io_spi,
                                         name_suffix="spi"))

    return resources


def SRAMResource(*args, cs, oe=None, we, a, d, dm=None, attrs=None):
    io = []
    io.append(Subsignal("cs", PinsN(cs, dir="o", assert_width=1)))
    if oe is not None:
        # Asserted WE# deactivates the D output buffers, so WE# can be used to replace OE#.
        io.append(Subsignal("oe", PinsN(oe, dir="o", assert_width=1)))
    io.append(Subsignal("we", PinsN(we, dir="o", assert_width=1)))
    io.append(Subsignal("a", Pins(a, dir="o")))
    io.append(Subsignal("d", Pins(d, dir="io")))
    if dm is not None:
        io.append(Subsignal("dm", PinsN(dm, dir="o"))) # dm="LB# UB#"
    if attrs is not None:
        io.append(attrs)
    return Resource.family(*args, default_name="sram", ios=io)
