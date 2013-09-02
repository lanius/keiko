import mock

import keiko.app


class TestApp(object):
    """Smoke test only."""

    def setup(self):
        keiko.app.app.keiko = mock.MagicMock()
        keiko.app.jsonify = mock.MagicMock(return_value='')
        self.app = keiko.app.app.test_client()

    def test_index(self):
        assert self.app.get('/').status_code == 200

    def test_get_all_lamps(self):
        assert self.app.get('/lamps').status_code == 200

    def test_get_lamp(self):
        assert self.app.get('/lamps/red').status_code == 200
        assert self.app.get('/lamps/yellow').status_code == 200
        assert self.app.get('/lamps/green').status_code == 200

    def test_set_lamp(self):
        assert self.app.get('/lamps/red/on').status_code == 200
        assert self.app.get('/lamps/yellow/blink').status_code == 200
        assert self.app.get('/lamps/green/quickblink').status_code == 200
        assert self.app.get('/lamps/red/off').status_code == 200

    def test_set_all_lamps_off(self):
        assert self.app.get('/lamps/off').status_code == 200

    def test_get_buzzer(self):
        assert self.app.get('/buzzer').status_code == 200

    def test_set_buzzer(self):
        assert self.app.get('/buzzer/on').status_code == 200
        assert self.app.get('/buzzer/continuous').status_code == 200
        assert self.app.get('/buzzer/intermittent').status_code == 200
        assert self.app.get('/buzzer/off').status_code == 200

    def test_get_all_dos(self):
        assert self.app.get('/do').status_code == 200

    def test_get_do(self):
        assert self.app.get('/do/1').status_code == 200
        assert self.app.get('/do/2').status_code == 200
        assert self.app.get('/do/3').status_code == 200
        assert self.app.get('/do/4').status_code == 200
        assert self.app.get('/do/0').status_code == 400
        assert self.app.get('/do/5').status_code == 400

    def test_set_do(self):
        assert self.app.get('/do/1/on').status_code == 200
        assert self.app.get('/do/2/off').status_code == 200

    def test_get_all_dis(self):
        assert self.app.get('/di').status_code == 200

    def test_get_di(self):
        assert self.app.get('/di/1').status_code == 200
        assert self.app.get('/di/2').status_code == 200
        assert self.app.get('/di/3').status_code == 200
        assert self.app.get('/di/4').status_code == 200
        assert self.app.get('/di/0').status_code == 400
        assert self.app.get('/di/5').status_code == 400

    def test_get_all_voices(self):
        assert self.app.get('/voices').status_code == 200

    def test_get_voice(self):
        assert self.app.get('/voices/1').status_code == 200
        assert self.app.get('/voices/20').status_code == 200
        assert self.app.get('/voices/0').status_code == 400
        assert self.app.get('/voices/21').status_code == 400

    def test_set_voice(self):
        assert self.app.get('/voices/1/play').status_code == 200
        assert self.app.get('/voices/2/repeat').status_code == 200
        assert self.app.get('/voices/3/stop').status_code == 200

    def test_set_all_voices_stop(self):
        assert self.app.get('/voices/stop').status_code == 200

    def test_get_contract(self):
        assert self.app.get('/contract').status_code == 200

    def test_get_model(self):
        assert self.app.get('/model').status_code == 200

    def test_get_productiondate(self):
        assert self.app.get('/productiondate').status_code == 200

    def test_get_serialnumber(self):
        assert self.app.get('/serialnumber').status_code == 200

    def test_get_unitid(self):
        assert self.app.get('/unitid').status_code == 200

    def test_get_version(self):
        assert self.app.get('/version').status_code == 200
