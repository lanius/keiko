"""
Provides Web API server for Keiko-chan.
"""

from flask import Flask, request, jsonify, abort

from keiko.clients import Client


app = Flask(__name__)


_VALID_COLORS = ['green', 'yellow', 'red']
_VALID_TERMS = ['1', '2', '3', '4']


@app.route('/')
def index():
    return 'keiko.py API server'


@app.route('/lamps')
def get_all_lamps():
    return jsonify(lamps=app.keiko.lamps.status)


@app.route('/lamps/<color>')
def get_lamp(color):
    if color not in _VALID_COLORS:
        abort(400)
    lamp = getattr(app.keiko.lamps, color)
    return jsonify(lamps={color: lamp.status})


@app.route('/lamps/<color>/<state>')
def set_lamp(color, state):
    if color not in _VALID_COLORS:
        abort(400)
    lamp = getattr(app.keiko.lamps, color)
    wait = request.args.get('wait', 0)
    time = request.args.get('time', 0)
    if state in ['on', 'blink', 'quickblink']:
        getattr(lamp, state)(wait, time)
    elif state == 'off':
        lamp.off(wait)
    else:
        abort(400)
    return jsonify(result='success')


@app.route('/lamps/off')
def set_all_lamps_off():
    wait = request.args.get('wait', 0)
    app.keiko.lamps.off(wait)
    return jsonify(result='success')


@app.route('/buzzer')
def get_buzzer():
    return jsonify(buzzer=app.keiko.buzzer.status)


@app.route('/buzzer/<state>')
def set_buzzer(state):
    wait = request.args.get('wait', 0)
    time = request.args.get('time', 0)
    if state in ['on', 'continuous', 'intermittent']:
        getattr(app.keiko.buzzer, state)(wait, time)
    elif state == 'off':
        app.keiko.buzzer.off(wait)
    else:
        abort(400)
    return jsonify(result='success')


@app.route('/do')
def get_all_dos():
    return jsonify(do=app.keiko.do.status)


@app.route('/do/<term>')
def get_do(term):
    if term not in _VALID_TERMS:
        abort(400)
    do = app.keiko.do(int(term))
    return jsonify(do={term: do.status})


@app.route('/do/<term>/<state>')
def set_do(term, state):
    if term not in _VALID_TERMS:
        abort(400)
    do = app.keiko.do(int(term))
    wait = request.args.get('wait', 0)
    time = request.args.get('time', 0)
    if state == 'on':
        do.on(wait, time)
    elif state == 'off':
        do.off(wait)
    else:
        abort(400)
    return jsonify(result='success')


@app.route('/di')
def get_all_dis():
    return jsonify(di=app.keiko.di.status)


@app.route('/di/<term>')
def get_di(term):
    if term not in _VALID_TERMS:
        abort(400)
    di = app.keiko.di(int(term))
    return jsonify(di={term: di.status})


@app.route('/voices')
def get_all_voices():
    return jsonify(voices=app.keiko.voices.status)


@app.route('/voices/<number>')
def get_voice(number):
    if not (number.isdigit() and 1 <= int(number) <= 20):
        abort(400)
    voice = app.keiko.voices(int(number))
    return jsonify(voices={number: voice.status})


@app.route('/voices/<number>/<state>')
def set_voice(number, state):
    if not (number.isdigit() and 1 <= int(number) <= 20):
        abort(400)
    voice = app.keiko.voices(int(number))
    times = request.args.get('times', 1)
    if state == 'play':
        voice.play(times)
    elif state in ['repeat', 'stop']:
        getattr(voice, state)()
    else:
        abort(400)
    return jsonify(result='success')


@app.route('/voices/stop')
def set_all_voices_stop():
    app.keiko.voices.stop()
    return jsonify(result='success')


@app.route('/contract')
def get_contract():
    return jsonify(contract={
        'deadline': app.keiko.raw.rdcd(),
        'number': app.keiko.raw.rdcn()
    })


@app.route('/model')
def get_model():
    return jsonify(model=app.keiko.raw.rdmn())


@app.route('/productiondate')
def get_productiondate():
    return jsonify(productiondate=app.keiko.raw.rdpd())


@app.route('/serialnumber')
def get_serialnumber():
    return jsonify(serialnumber=app.keiko.raw.rdsn())


@app.route('/unitid')
def get_unitid():
    return jsonify(unitid=app.keiko.raw.utid())


@app.route('/version')
def get_version():
    return jsonify(version=app.keiko.raw.vern())


def main():
    import argparse
    import logging
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'address',
        metavar='ADDRESS',
        help='address of Keiko-chan'
    )
    parser.add_argument(
        '--port',
        default=60000,
        help='port of Keiko-chan[60000]'
    )
    parser.add_argument(
        '--server',
        default='127.0.0.1:8080',
        help='address and port of API server[127.0.0.1:8080]'
    )
    parser.add_argument(
        '--debug',
        type=bool,
        default=False,
        help='run API server on debug mode[False]'
    )
    args = parser.parse_args()

    log_handler = logging.FileHandler(
        os.path.join(os.getcwd(), 'error.log')
    )
    log_handler.setLevel(logging.ERROR)
    app.logger.addHandler(log_handler)

    app.keiko = Client(args.address, args.port)
    app.debug = args.debug
    host, port = args.server.split(':')
    app.run(host=host, port=int(port))


if __name__ == '__main__':
    main()
