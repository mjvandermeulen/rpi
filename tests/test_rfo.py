import subprocess


def test_CLI_rfo_call():
    return_code = subprocess.call([
        '/home/pi/Programming/Automation/executables/rfoutlets_switch_group.py',
        '1000',
        'on',  # ommited 'blink', but should blink
        '--attempts 1',
        '--delay 5',  # useless when attempts is one
        '--blinks 2',
        '--blinkon 1',
        '--blinkoff 2'
    ])
    # return_code = subprocess.call([
    #     '/home/pi/Programming/Automation/executables/rfoutlets_switch_group.py',
    #     '1000',
    #     'off'
    # ])
    assert return_code == 0
