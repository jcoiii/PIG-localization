from picosdk.ps2000 import ps2000
from picosdk.functions import adc2mV, assert_pico2000_ok
from picosdk.PicoDeviceEnums import picoEnum
with ps2000.open_unit() as device:
    print('Device info: {}'.format(device.info))
    res = ps2000.ps2000_set_sig_gen_built_in(
        device.handle,
            0,
            400_000,
            0,
            25.0,
            25.0,
            0.0,
            0.1,
            0,
            1_000
        )
    assert_pico2000_ok(res)
    res = ps2000.ps2000_set_channel(
    device.handle,
    picoEnum.PICO_CHANNEL['PICO_CHANNEL_A'],
    True,
    picoEnum.PICO_COUPLING['PICO_DC'],
    ps2000.PS2000_VOLTAGE_RANGE['PS2000_500MV'],
    )
    assert_pico2000_ok(res)