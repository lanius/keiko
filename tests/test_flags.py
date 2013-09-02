import keiko.flags


class TestFlags(object):

    def test_build_lamp_flags(self):
        flags = keiko.flags.build_lamp_flags(
            {'lamps': {'red': 'on', 'yellow': 'off'}})
        assert flags == '10XXXXXX'
        flags = keiko.flags.build_lamp_flags(
            {'lamps': {'yellow': 'blink', 'green': 'quickblink'}}
        )
        assert flags == 'X23XXXXX'

    def test_parse_lamp_flags(self):
        states = keiko.flags.parse_lamp_flags('10000000')
        assert states == {
            'lamps': {'red': 'on', 'yellow': 'off', 'green': 'off'}
        }
        states = keiko.flags.parse_lamp_flags('02300000')
        assert states == {
            'lamps': {'red': 'off', 'yellow': 'blink', 'green': 'quickblink'}
        }

    def test_lamp_state_interconversion(self):
        org = '12300000'
        state = keiko.flags.parse_lamp_flags(org)
        flags = keiko.flags.build_lamp_flags(state)
        assert flags == org.replace('0', 'X')

    def test_build_buzzer_flags(self):
        flags = keiko.flags.build_buzzer_flags({'buzzer': 'continuous'})
        assert flags == 'XXX1XXXX'

    def test_parse_buzzer_flags(self):
        states = keiko.flags.parse_buzzer_flags('00001000')
        assert states == {
            'buzzer': 'intermittent'
        }

    def test_buzzer_state_interconversion(self):
        org = '00010000'
        state = keiko.flags.parse_buzzer_flags(org)
        flags = keiko.flags.build_buzzer_flags(state)
        assert flags == org.replace('0', 'X')

    def test_build_do_flags(self):
        flags = keiko.flags.build_do_flags({'do': {1: 'on', 3: 'off'}})
        assert flags == '1X0XXXXX'

    def test_parse_do_flags(self):
        states = keiko.flags.parse_do_flags('10100000')
        assert states == {'do': {1: 'on', 2: 'off', 3: 'on', 4: 'off'}}

    def test_do_state_interconversion(self):
        org = '11110000'
        state = keiko.flags.parse_do_flags(org)
        flags = keiko.flags.build_do_flags(state)
        assert flags == org.replace('0', 'X')

    def test_parse_di_flags(self):
        states = keiko.flags.parse_di_flags('0101')
        assert states == {'di': {1: 'off', 2: 'on', 3: 'off', 4: 'on'}}

    def test_build_voice_flags(self):
        flags = keiko.flags.build_voice_flags(
            {'voice': {'number': 15, 'repeat': 8}}
        )
        assert flags == '11510800'
        flags = keiko.flags.build_voice_flags(
            {'voice': {'number': 2, 'repeat': 0}}
        )
        assert flags == '10200000'
        flags = keiko.flags.build_voice_flags({'voice': 'stop'})
        assert flags == '00000000'

    def test_parse_voice_flags(self):
        states = keiko.flags.parse_voice_flags('00000000')
        assert states == {'voice': 'stop'}
        states = keiko.flags.parse_voice_flags('10911000')
        assert states == {
            'voice': {'number': 9, 'repeat': 10}
        }

    def test_voice_state_interconversion(self):
        org = '11510800'
        state = keiko.flags.parse_voice_flags(org)
        flags = keiko.flags.build_voice_flags(state)
        assert flags == org
