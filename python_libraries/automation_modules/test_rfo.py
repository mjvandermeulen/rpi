import subprocess


def test_CLI_rfo_call():
    return_code = subprocess.call([
        '/home/pi/Programming/Automation/executables/rfoutlets_switch_group.py',
        '1000',
        'on'
    ])
    return_code = subprocess.call([
        '/home/pi/Programming/Automation/executables/rfoutlets_switch_group.py',
        '1000',
        'off'
    ])
    assert return_code == 0
