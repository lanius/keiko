import sys

import mock
import pytest

import keiko.clients


class TestClient(object):

    def setup(self):
        self.client = keiko.clients.Client('127.0.0.1')  # dummy address
        self.client.raw._execute = mock.MagicMock()

    def teardown(self):
        del self.client

    def get_sent_command(self):
        args, kwargs = self.client.raw._execute.call_args
        return args[0]

    def set_received_message(self, message):
        self.client.raw._execute.return_value = message

    def test_get_lamps(self):
        self.set_received_message('00000000')
        self.client.lamps.status
        assert self.get_sent_command() == 'ACOP -u 1'

    def test_get_lamps_with_state(self):
        self.set_received_message('10100000')
        assert self.client.lamps.status == {
            'red': 'on', 'yellow': 'off', 'green': 'on'
        }

    def test_get_lamp(self):
        self.set_received_message('00000000')
        self.client.lamps.red.status
        assert self.get_sent_command() == 'ACOP -u 1'

    def test_get_lamp_with_state(self):
        self.set_received_message('10100000')
        assert self.client.lamps.red.status == 'on'
        assert self.client.lamps.yellow.status == 'off'
        assert self.client.lamps.green.status == 'on'

    def test_get_lamp_with_mode(self):
        self.set_received_message('02300000')
        assert self.client.lamps.red.status == 'off'
        assert self.client.lamps.yellow.status == 'blink'
        assert self.client.lamps.green.status == 'quickblink'

    def test_turn_on_lamp(self):
        self.client.lamps.red.on()
        assert self.get_sent_command() == 'ACOP -u 1 1XXXXXXX -w 0 -t 0'

    def test_turn_on_lamp_with_mode(self):
        self.client.lamps.yellow.blink()
        assert self.get_sent_command() == 'ACOP -u 1 X2XXXXXX -w 0 -t 0'

    def test_turn_on_lamp_with_wait_and_time(self):
        self.client.lamps.green.on(wait=2, time=3)
        assert self.get_sent_command() == 'ACOP -u 1 XX1XXXXX -w 2 -t 3'

    def test_turn_off_lamp(self):
        self.client.lamps.red.off()
        assert self.get_sent_command() == 'ACOP -u 1 0XXXXXXX -w 0 -t 0'

    def test_turn_off_lamp_with_wait(self):
        self.client.lamps.yellow.off(wait=2)
        assert self.get_sent_command() == 'ACOP -u 1 X0XXXXXX -w 2 -t 0'

    def test_get_buzzer(self):
        self.set_received_message('00000000')
        self.client.buzzer.status
        assert self.get_sent_command() == 'ACOP -u 1'

    def test_get_buzzer_with_state(self):
        self.set_received_message('00000000')
        assert self.client.buzzer.status == 'off'

    def test_get_buzzer_with_mode(self):
        self.set_received_message('00010000')
        assert self.client.buzzer.status == 'continuous'
        self.set_received_message('00001000')
        assert self.client.buzzer.status == 'intermittent'

    def test_turn_on_buzzer(self):
        self.client.buzzer.on()
        assert self.get_sent_command() == 'ACOP -u 1 XXX1XXXX -w 0 -t 0'

    def test_turn_on_buzzer_with_mode(self):
        self.client.buzzer.intermittent()
        assert self.get_sent_command() == 'ACOP -u 1 XXXX1XXX -w 0 -t 0'

    def test_turn_on_buzzer_with_wait_and_time(self):
        self.client.buzzer.on(wait=2, time=3)
        assert self.get_sent_command() == 'ACOP -u 1 XXX1XXXX -w 2 -t 3'

    def test_turn_off_buzzer(self):
        self.client.buzzer.off()
        assert self.get_sent_command() == 'ACOP -u 1 XXX00XXX -w 0 -t 0'

    def test_turn_off_buzzer_with_wait(self):
        self.client.buzzer.off(wait=2)
        assert self.get_sent_command() == 'ACOP -u 1 XXX00XXX -w 2 -t 0'

    def test_get_dos(self):
        self.set_received_message('10100000')
        self.client.do.status
        assert self.get_sent_command() == 'ACOP -u 2'

    def test_get_dos_with_state(self):
        self.set_received_message('10100000')
        assert self.client.do.status == {
            1: 'on', 2: 'off', 3: 'on', 4: 'off'
        }

    def test_get_do(self):
        self.set_received_message('10100000')
        self.client.do(1).status
        assert self.get_sent_command() == 'ACOP -u 2'

    def test_get_do_with_state(self):
        self.set_received_message('10100000')
        assert self.client.do(1).status == 'on'
        assert self.client.do(2).status == 'off'
        assert self.client.do(3).status == 'on'
        assert self.client.do(4).status == 'off'

    def test_turn_on_do(self):
        self.client.do(1).on()
        assert self.get_sent_command() == 'ACOP -u 2 1XXXXXXX -w 0 -t 0'

    def test_turn_on_do_with_wait_and_time(self):
        self.client.do(2).on(wait=3, time=4)
        assert self.get_sent_command() == 'ACOP -u 2 X1XXXXXX -w 3 -t 4'

    def test_turn_off_do(self):
        self.client.do(3).off()
        assert self.get_sent_command() == 'ACOP -u 2 XX0XXXXX -w 0 -t 0'

    def test_turn_off_do_with_wait(self):
        self.client.do(4).off(wait=5)
        assert self.get_sent_command() == 'ACOP -u 2 XXX0XXXX -w 5 -t 0'

    def test_get_dis(self):
        self.set_received_message('0101')
        self.client.di.status
        assert self.get_sent_command() == 'ROPS'

    def test_get_dis_with_state(self):
        self.set_received_message('0101')
        assert self.client.di.status == {
            1: 'off', 2: 'on', 3: 'off', 4: 'on'
        }

    def test_get_di(self):
        self.set_received_message('0101')
        self.client.di(1).status
        assert self.get_sent_command() == 'ROPS'

    def test_get_di_with_state(self):
        self.set_received_message('0101')
        assert self.client.di(1).status == 'off'
        assert self.client.di(2).status == 'on'
        assert self.client.di(3).status == 'off'
        assert self.client.di(4).status == 'on'

    def test_get_voices(self):
        self.set_received_message('00911010')
        self.client.voices.status
        assert self.get_sent_command() == 'SPOP'

    def test_get_voices_with_state(self):
        self.set_received_message('00911010')
        assert self.client.voices.status == 'stop'
        self.set_received_message('10911010')
        assert self.client.voices.status == {'number': 9, 'repeat': 10}

    def test_get_voice(self):
        self.set_received_message('00911010')
        self.client.voices(9).status
        assert self.get_sent_command() == 'SPOP'

    def test_get_voice_with_state(self):
        self.set_received_message('00911010')
        assert self.client.voices(9).status == 'stop'
        self.set_received_message('10911010')
        assert self.client.voices(9).status == 'play'

    def test_play_voice(self):
        self.client.voices(1).play()
        assert self.get_sent_command() == 'SPOP 10110100'

    def test_play_voice_with_times(self):
        self.client.voices(10).play(times=20)
        assert self.get_sent_command() == 'SPOP 11012000'

    def test_repeat_voice(self):
        self.client.voices(1).repeat()
        assert self.get_sent_command() == 'SPOP 10100000'

    def test_stop_voices(self):
        self.client.voices.stop()
        assert self.get_sent_command() == 'SPOP 00000000'

    def test_stop_voice(self):
        self.client.voices(20).stop()
        assert self.get_sent_command() == 'SPOP 00000000'


class TestRawClient(object):

    address = '127.0.0.1'
    port = 60000

    def setup(self):
        self.patcher = mock.patch('socket.socket')
        self.patcher.start()
        self.client = keiko.clients.RawClient(self.address, self.port)
        self.client._strip_data = mock.Mock()  # has trouble on py3

    def teardown(self):
        del self.client
        self.patcher.stop()

    def get_sent_data(self):
        args, kwargs = self.client._sock.sendall.call_args
        data = args[0]
        if sys.version_info[0] >= 3:  # py3
            return str(data, 'utf-8')  # bytes to str
        else:  # py2
            return data

    def test_connect(self):
        self.client.help()
        self.client._sock.connect.assert_called_with(
            (self.address, self.port)
        )

    def test_error(self):
        self.client._send = mock.Mock(return_value='ER01')  # error code
        with pytest.raises(Exception):
            self.client.help()

    def test_acop_read(self):
        self.client.acop()
        assert self.get_sent_data() == 'ACOP -u 1\r'

    def test_acop_write_with_default(self):
        self.client.acop('X12XXXXX')
        assert self.get_sent_data() == 'ACOP -u 1 X12XXXXX -w 0 -t 0\r'

    def test_acop_write_with_param(self):
        self.client.acop('101XXXXX', unit=2, wait=3, time=4)
        assert self.get_sent_data() == 'ACOP -u 2 101XXXXX -w 3 -t 4\r'

    def test_alof_write(self):
        self.client.alof()
        assert self.get_sent_data() == 'ALOF\r'

    def test_ckdi_read(self):
        self.client.ckdi()
        assert self.get_sent_data() == 'CKDI\r'

    def test_ckdi_write(self):
        self.client.ckdi('EDEX')
        assert self.get_sent_data() == 'CKDI EDEX\r'

    def test_ckid_read(self):
        self.client.ckid()
        assert self.get_sent_data() == 'CKID\r'

    def test_ckid_write(self):
        self.client.ckid('Enable')
        assert self.get_sent_data() == 'CKID Enable\r'

    def test_ckip_read(self):
        self.client.ckip()
        assert self.get_sent_data() == 'CKIP\r'

    def test_ckip_write(self):
        self.client.ckip('EDEXXXXXXXXXXXXXXXXX')
        assert self.get_sent_data() == 'CKIP EDEXXXXXXXXXXXXXXXXX\r'

    def test_ckst_read(self):
        self.client.ckst()
        assert self.get_sent_data() == 'CKST\r'

    def test_help_read(self):
        self.client.help()
        assert self.get_sent_data() == 'HELP\r'

    def test_lgpw_read(self):
        self.client.lgpw()
        assert self.get_sent_data() == 'LGPW\r'

    def test_lgpw_write(self):
        self.client.lgpw('isa')
        assert self.get_sent_data() == 'LGPW isa\r'

    def test_pwst_read(self):
        self.client.pwst()
        assert self.get_sent_data() == 'PWST\r'

    def test_pwst_write(self):
        self.client.pwst('Enable')
        assert self.get_sent_data() == 'PWST Enable\r'

    def test_rdcd_read(self):
        self.client.rdcd()
        assert self.get_sent_data() == 'RDCD\r'

    def test_rdcn_read(self):
        self.client.rdcn()
        assert self.get_sent_data() == 'RDCN\r'

    def test_rdmn_read(self):
        self.client.rdmn()
        assert self.get_sent_data() == 'RDMN\r'

    def test_rdpd_read(self):
        self.client.rdpd()
        assert self.get_sent_data() == 'RDPD\r'

    def test_rdsn_read(self):
        self.client.rdsn()
        assert self.get_sent_data() == 'RDSN\r'

    def test_rly1_read(self):
        self.client.rly1()
        assert self.get_sent_data() == 'RLY1\r'

    def test_rly2_read(self):
        self.client.rly2()
        assert self.get_sent_data() == 'RLY2\r'

    def test_rly3_read(self):
        self.client.rly3()
        assert self.get_sent_data() == 'RLY3\r'

    def test_rly4_read(self):
        self.client.rly4()
        assert self.get_sent_data() == 'RLY4\r'

    def test_rly5_read(self):
        self.client.rly5()
        assert self.get_sent_data() == 'RLY5\r'

    def test_rly6_read(self):
        self.client.rly6()
        assert self.get_sent_data() == 'RLY6\r'

    def test_rly7_read(self):
        self.client.rly7()
        assert self.get_sent_data() == 'RLY7\r'

    def test_rly8_read(self):
        self.client.rly8()
        assert self.get_sent_data() == 'RLY8\r'

    def test_rly_write_with_default(self):
        self.client.rly1('TurnOn')
        assert self.get_sent_data() == 'RLY1 TurnOn -w 0 -t 0\r'

    def test_rly_write_with_param(self):
        self.client.rly2('Blink', wait=10, time=30)
        assert self.get_sent_data() == 'RLY2 Blink -w 10 -t 30\r'

    def test_rops_read(self):
        self.client.rops()
        assert self.get_sent_data() == 'ROPS\r'

    def test_ryin_read(self):
        self.client.ryin(1)
        assert self.get_sent_data() == 'RYIN -n 1\r'

    def test_ryof_write(self):
        self.client.ryof(2)
        assert self.get_sent_data() == 'RYOF -n 2\r'

    def test_ryot_read(self):
        self.client.ryot(2)
        assert self.get_sent_data() == 'RYOT -n 2\r'

    def test_ryot_write_with_default(self):
        self.client.ryot(1, 'TurnOn')
        assert self.get_sent_data() == 'RYOT -n 1 TurnOn -w 0 -t 0\r'

    def test_ryot_write_with_param(self):
        self.client.ryot(2, 'TurnOn', wait=10, time=20)
        assert self.get_sent_data() == 'RYOT -n 2 TurnOn -w 10 -t 20\r'

    def test_spop_read(self):
        self.client.spop()
        assert self.get_sent_data() == 'SPOP\r'

    def test_spop_write(self):
        self.client.spop('10100000')
        assert self.get_sent_data() == 'SPOP 10100000\r'

    def test_utid_read(self):
        self.client.utid()
        assert self.get_sent_data() == 'UTID\r'

    def test_vern_read(self):
        self.client.vern()
        assert self.get_sent_data() == 'VERN\r'
