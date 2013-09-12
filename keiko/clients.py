"""
Provides client classes for Keiko-chan.
"""

import contextlib
import socket
import sys

from keiko.flags import (
    build_lamp_flags, parse_lamp_flags,
    build_buzzer_flags, parse_buzzer_flags,
    build_do_flags, parse_do_flags,
    parse_di_flags,
    build_voice_flags, parse_voice_flags
)


class Client(object):
    """Provides high level APIs to control Keiko-chan."""

    def __init__(self, address, port=60000):
        self.raw = RawClient(address, port)
        self.lamps = LampHolder(self.raw)
        self.buzzer = Buzzer(self.raw)
        self.do = DOHolder(self.raw)
        self.di = DIHolder(self.raw)
        self.voices = VoiceHolder(self.raw)


class LampHolder(object):
    """Holds the lamps."""

    def __init__(self, rawclient):
        self.raw = rawclient
        self.red = Lamp(self.raw, 'red')
        self.yellow = Lamp(self.raw, 'yellow')
        self.green = Lamp(self.raw, 'green')

    @property
    def status(self):
        """Returns all the lamps state."""
        flags = self.raw.acop()
        states = parse_lamp_flags(flags)
        return states['lamps']

    def off(self, wait=0):
        """Turns off all the lamps."""
        flags = build_lamp_flags(
            {'lamps': {'red': 'off', 'yellow': 'off', 'green': 'off'}}
        )
        self.raw.acop(flags, wait=wait)


class Lamp(object):
    """A client to control the lamp."""

    def __init__(self, rawclient, color):
        self.raw = rawclient
        self.color = color

    @property
    def status(self):
        """Returns the lamp state."""
        flags = self.raw.acop()
        states = parse_lamp_flags(flags)
        return states['lamps'][self.color]

    def _set(self, state, wait=0, time=0):
        flags = build_lamp_flags({'lamps': {self.color: state}})
        self.raw.acop(flags, wait=wait, time=time)

    def on(self, wait=0, time=0):
        """Turns on the lamp."""
        self._set('on', wait, time)

    def blink(self, wait=0, time=0):
        """Blinks the lamp on and off."""
        self._set('blink', wait, time)

    def quickblink(self, wait=0, time=0):
        """Blinks the lamp on and off quickly."""
        self._set('quickblink', wait, time)

    def off(self, wait=0):
        """Turns off the lamp."""
        self._set('off', wait)


class Buzzer(object):
    """A client to control the buzzer."""

    def __init__(self, rawclient):
        self.raw = rawclient

    @property
    def status(self):
        """Returns the buzzer state."""
        flags = self.raw.acop()
        states = parse_buzzer_flags(flags)
        return states['buzzer']

    def _set(self, state, wait=0, time=0):
        flags = build_buzzer_flags({'buzzer': state})
        self.raw.acop(flags, wait=wait, time=time)

    def on(self, wait=0, time=0):
        """Turns on the buzzer to beep continuously."""
        self.continuous(wait, time)

    def continuous(self, wait=0, time=0):
        """Turns on the buzzer to beep continuously."""
        self._set('continuous', wait, time)

    def intermittent(self, wait=0, time=0):
        """Turns on the buzzer to beep intermittently."""
        self._set('intermittent', wait, time)

    def off(self, wait=0):
        """Turns off the buzzer."""
        self._set('off', wait)


class DOHolder(object):
    """Holds the DOs."""

    def __init__(self, rawclient):
        self.raw = rawclient

    def __call__(self, term):
        return DO(self.raw, term)

    @property
    def status(self):
        """Returns all the DOs state."""
        flags = self.raw.acop(unit=2)
        states = parse_do_flags(flags)
        return states['do']


class DO(object):
    """A client to control the direct output."""

    def __init__(self, rawclient, term):
        self.raw = rawclient
        self.term = term

    @property
    def status(self):
        """Returns the DO state."""
        flags = self.raw.acop(unit=2)
        states = parse_do_flags(flags)
        return states['do'][self.term]

    def _set(self, state, wait=0, time=0):
        flags = build_do_flags({'do': {self.term: state}})
        self.raw.acop(flags, unit=2, wait=wait, time=time)

    def on(self, wait=0, time=0):
        """Turns on the DO."""
        self._set('on', wait, time)

    def off(self, wait=0):
        """Turns off the DO."""
        self._set('off', wait)


class DIHolder(object):
    """Holds the DIs."""

    def __init__(self, rawclient):
        self.raw = rawclient

    def __call__(self, term):
        return DI(self.raw, term)

    @property
    def status(self):
        """Returns all the DIs state."""
        flags = self.raw.rops()
        states = parse_di_flags(flags)
        return states['di']


class DI(object):
    """A client to control the direct input."""

    def __init__(self, rawclient, term):
        self.raw = rawclient
        self.term = term

    @property
    def status(self):
        """Returns the DI state."""
        flags = self.raw.rops()
        states = parse_di_flags(flags)
        return states['di'][self.term]


class VoiceHolder(object):
    """Holds the voices."""

    def __init__(self, rawclient):
        self.raw = rawclient

    def __call__(self, number):
        return Voice(self.raw, number)

    @property
    def status(self):
        """Returns the voices state."""
        flags = self.raw.spop()
        states = parse_voice_flags(flags)
        return states['voice']

    def stop(self):
        """Stops playing any voice."""
        flags = build_voice_flags({'voice': 'stop'})
        self.raw.spop(flags)


class Voice(object):

    def __init__(self, rawclient, number):
        self.raw = rawclient
        self.number = number

    @property
    def status(self):
        """Returns the voice state."""
        flags = self.raw.spop()
        states = parse_voice_flags(flags)
        state = states['voice']
        if state == 'stop':
            return 'stop'
        if state['number'] == self.number:
            return 'play'
        else:
            return 'stop'

    def _set(self, state):
        flags = build_voice_flags({'voice': state})
        self.raw.spop(flags)

    def play(self, times=1):
        """Plays the voice."""
        self._set({'number': self.number, 'repeat': times})

    def repeat(self):
        """Plays the voice repeatedly."""
        self.play(0)

    def stop(self):
        """Stops playing the voice."""
        self._set('stop')


class RawClient(object):
    """Provides low level APIs to control Keiko-chan."""

    def __init__(self, address, port=60000):
        self.address = address
        self.port = port

    def _send(self, command):
        ret = ''
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with contextlib.closing(self._sock):
            self._sock.connect((self.address, self.port))
            self._sock.sendall(self._build_data(command))
            ret = self._sock.recv(64)  # enough long
        return self._strip_data(ret)

    def _build_data(self, command):
        data = ''.join([command, '\r'])
        if sys.version_info[0] >= 3:  # py3
            return bytes(data, 'ascii')  # str to bytes
        else:  # py2
            return data

    def _strip_data(self, data):
        if sys.version_info[0] >= 3:  # py3
            data = str(data, 'utf-8')  # bytes to str
        return data.rstrip('\r')

    def _execute(self, command):
        result = self._send(command)
        errors = {
            'ER01': 'Invalid command',
            'ER02': 'Wrong EOL code',
            'ER03': 'Wrong arguments',
            'ER04': 'Command failed'
        }
        if result in errors:
            raise Exception(errors[result])
        return result

    def acop(self, flags=None, unit=1, wait=0, time=0):
        # flags: [0123X]{8}
        command = ' '.join(['ACOP', '-u', str(unit)])
        if flags:
            args = ' '.join([flags, '-w', str(wait), '-t', str(time)])
            return self._execute(' '.join([command, args]))
        else:
            return self._execute(command)

    def alof(self):
        return self._execute('ALOF')

    def ckdi(self, flags=None):
        # flags: [EDX]{4}
        command = 'CKDI'
        if flags:
            return self._execute(' '.join([command, flags]))
        else:
            return self._execute(command)

    def ckid(self, param=None):
        # param: Enable|Disable
        command = 'CKID'
        if param:
            return self._execute(' '.join([command, param]))
        else:
            return self._execute(command)

    def ckip(self, flags=None):
        # flags: [EDX]{20}
        command = 'CKIP'
        if flags:
            return self._execute(' '.join([command, flags]))
        else:
            return self._execute(command)

    def ckst(self):
        return self._execute('CKST')

    def help(self):
        return self._execute('HELP')

    def lgpw(self, new_password=None):
        command = 'LGPW'
        if new_password:
            return self._execute(' '.join([command, new_password]))
        else:
            return self._execute(command)

    def pwst(self, param=None):
        # param: Enable|Disable
        command = 'PWST'
        if param:
            return self._execute(' '.join([command, param]))
        else:
            return self._execute(command)

    def rdcd(self):
        return self._execute('RDCD')

    def rdcn(self):
        return self._execute('RDCN')

    def rdmn(self):
        return self._execute('RDMN')

    def rdpd(self):
        return self._execute('RDPD')

    def rdsn(self):
        return self._execute('RDSN')

    def _rly(self, command, param, wait, time):
        # command: RLY[1-8]
        # param: TurnOff|TurnOn|Blink
        if param:
            args = ' '.join([param, '-w', str(wait), '-t', str(time)])
            return self._execute(' '.join([command, args]))
        else:
            return self._execute(command)

    def rly1(self, param=None, wait=0, time=0):
        return self._rly('RLY1', param, wait, time)

    def rly2(self, param=None, wait=0, time=0):
        return self._rly('RLY2', param, wait, time)

    def rly3(self, param=None, wait=0, time=0):
        return self._rly('RLY3', param, wait, time)

    def rly4(self, param=None, wait=0, time=0):
        return self._rly('RLY4', param, wait, time)

    def rly5(self, param=None, wait=0, time=0):
        return self._rly('RLY5', param, wait, time)

    def rly6(self, param=None, wait=0, time=0):
        return self._rly('RLY6', param, wait, time)

    def rly7(self, param=None, wait=0, time=0):
        return self._rly('RLY7', param, wait, time)

    def rly8(self, param=None, wait=0, time=0):
        return self._rly('RLY8', param, wait, time)

    def rops(self):
        return self._execute('ROPS')

    def ryin(self, term):
        # term: [1-4]
        return self._execute(' '.join(['RYIN', '-n', str(term)]))

    def ryof(self, term):
        # term: [1-4]
        return self._execute(' '.join(['RYOF', '-n', str(term)]))

    def ryot(self, term, param=None, wait=0, time=0):
        command = 'RYOT'
        if param:  # TurnOff|TurnOn|Pulse
            args = ' '.join([
                '-n', str(term), param, '-w', str(wait), '-t', str(time)
            ])
            return self._execute(' '.join([command, args]))
        else:
            return self._execute(' '.join([command, '-n', str(term)]))

    def spop(self, flags=None):
        # flags: [0-9]{7}
        command = 'SPOP'
        if flags:
            return self._execute(' '.join([command, flags]))
        else:
            return self._execute(command)

    def utid(self):
        return self._execute('UTID')

    def vern(self):
        return self._execute('VERN')
