"""
Provides utilities for flags arguments of commands.
"""

# lamps
_LAMP_DIGITS = {
    'red': 0,
    'yellow': 1,
    'green': 2
}
_LAMP_STATES = {
    'off': 0,
    'on': 1,
    'blink': 2,
    'quickblink': 3
}


def build_lamp_flags(states):
    """Returns flags that be used as arguments of lamp control commands.

    The structure of <states> is:

        {'lamps': {<color>: <state>}}

    <color> is red, yellow, or green.
    <state> is on, blink, quickblink, or off.

    Example:

        {'lamps': {'red': 'on', 'green': 'off'}}
    """
    flag_list = list('XXXXXXXX')
    for color, state in states['lamps'].items():
        flag_list[_LAMP_DIGITS[color]] = str(_LAMP_STATES[state])
    return ''.join(flag_list)


def parse_lamp_flags(flags):
    """Parses flags and returns a dict that represents the lamp states."""
    # flags: [0123]{8}
    values = _swap_key_and_value(_LAMP_STATES)  # {value: state}
    states = dict([
        (color, values[flags[digit]]) for color, digit in _LAMP_DIGITS.items()
    ])
    return {'lamps': states}


# buzzer
_BUZZER_DIGITS = {
    'continuous': 3,
    'intermittent': 4
}


def build_buzzer_flags(states):
    """Returns flags that be used as arguments of buzzer control commands.

    The structure of <states> is:

        {'buzzer': <state>}

    <state> is continuous, intermittent, or off.

    Example:

        {'buzzer': 'continuous'}
    """
    flag_list = list('XXXXXXXX')
    state = states['buzzer']
    if state == 'off':
        for digit in _BUZZER_DIGITS.values():
            flag_list[digit] = '0'
    else:
        flag_list[_BUZZER_DIGITS[state]] = '1'
    return ''.join(flag_list)


def parse_buzzer_flags(flags):
    """Parses flags and returns a dict that represents the buzzer states."""
    # flags: [0123]{8}
    for state, digit in _BUZZER_DIGITS.items():
        if flags[digit] == '1':
            return {'buzzer': state}
    return {'buzzer': 'off'}


# DOs
_DO_DIGITS = {  # {term: digit}
    1: 0,
    2: 1,
    3: 2,
    4: 3
}
_DO_STATES = {
    'off': 0,
    'on': 1
}


def build_do_flags(states):
    """Returns flags that be used as arguments of DOs control commands.

    The structure of <states> is:

        {'do': {<term>: <state>}}

    <term> is a terminal number. <state> is on or off.

    Example:

        {'do': {1: 'on', 3: 'off'}}
    """
    flag_list = list('XXXXXXXX')
    for term, state in states['do'].items():
        flag_list[_DO_DIGITS[term]] = str(_DO_STATES[state])
    return ''.join(flag_list)


def parse_do_flags(flags):
    """Parses flags and returns a dict that represents the DOs states."""
    # flags: [01]{8}
    values = _swap_key_and_value(_DO_STATES)  # {value: state}
    states = dict([
        (term, values[flags[digit]]) for term, digit in _DO_DIGITS.items()
    ])
    return {'do': states}


# DIs
_DI_DIGITS = {  # {term: digit}
    1: 0,
    2: 1,
    3: 2,
    4: 3
}
_DI_STATES = {
    'off': 0,
    'on': 1
}


def parse_di_flags(flags):
    """Parses flags and returns a dict that represents the DIs states."""
    # flags: [01]{4}
    values = _swap_key_and_value(_DI_STATES)  # {value: state}
    states = dict([
        (term, values[flags[digit]]) for term, digit in _DI_DIGITS.items()
    ])
    return {'di': states}


# voice
def build_voice_flags(states):
    """Returns flags that be used as arguments of voice control commands.

    The structure of <states> is:

        {'voice': <state>}

    <state> is stop, or {'number': <number>, 'repeat': <repeat>}.
    <number> is voice number to play, 1 - 20.
    <repeat> is total number of plays. You can set 0 to repeat infinitely.

    Example:

        {'voice: {'number': 1, 'repeat': 3}}
    """
    if states['voice'] == 'stop':
        return '00000000'
    number = states['voice']['number']
    repeat = states['voice']['repeat']
    if repeat == 0:
        return '1{0:02}00000'.format(number)  # to repeat infinitely
    else:
        return '1{0:02}1{1:02}00'.format(number, repeat)


def parse_voice_flags(flags):
    """Parses flags and returns a dict that represents voice playing state."""
    # flags: [0-9]{8}
    if flags[0] == '0':
        return {'voice': 'stop'}
    else:
        return {'voice': {
            'number': int(flags[1:3]),
            'repeat': int(flags[4:6])
        }}


# inner utils
def _swap_key_and_value(dictionary):
    return dict((str(v), s) for s, v in dictionary.items())
