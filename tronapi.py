from flask import (
    Flask, jsonify, abort, make_response, request
)
from trx_utils import (
    from_sun, to_sun, is_address
)

from config.cfg import cttAddr, network
from tronpy import Tron
from tronpy.keys import PrivateKey

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def hello_world():
    abort(404)
    return 'Hello World!'


@app.route('/api/generateAddress', methods=["GET"])
def generateAddress():
    client = Tron(network=network)
    account = client.generate_address()

    return jsonify({
        "data": account,
        "code": 200,
        "msg": "地址生成成功"
    })


@app.route('/api/balance/<string:address>', methods=["GET"])
def balance(address):
    try:
        if not is_address(address):
            raise Exception('地址格式不正确')

        client = Tron()
        response = client.get_account(address)
        _balance = 0
        if 'balance' in response:
            _balance = response['balance']

        # if is_float:
        #     return self.tron.fromSun(response['balance'])
        #
        balance_raw = _balance

        balance_sun = str(from_sun(_balance))

    except Exception as e:
        return jsonify({
            "data": None,
            "code": 500,
            "msg": str(e)
        })

    return jsonify({
        "data": {
            'cttAddr': cttAddr,
            # 'token': symbol,
            'balance': {
                'to_sun': balance_sun,
                'raw': balance_raw
            }
        },
        "code": 200,
        "msg": "查询TRX余额成功"
    })


@app.route('/api/balanceOf/<string:address>', methods=["GET"])
def balanceOf(address):
    try:
        if not is_address(address):
            raise Exception('地址格式不正确')

        client = Tron()
        contract = client.get_contract(cttAddr)
        # symbol = contract.functions.symbol()

        balance_raw = contract.functions.balanceOf(address)

        balance_sun = str(from_sun(balance_raw))

    except Exception as e:
        return jsonify({
            "data": None,
            "code": 500,
            "msg": str(e)
        })

    return jsonify({
        "data": {
            'cttAddr': cttAddr,
            # 'token': symbol,
            'balance': {
                'to_sun': balance_sun,
                'raw': balance_raw
            }
        },
        "code": 200,
        "msg": "查询成功"
    })


@app.route('/api/transferToken', methods=["POST"])
def transferToken():
    # cttAddr = ''

    _from = request.form.get('from_address')
    _to = request.form.get('to_address')
    _privKey = request.form.get('private_key')
    _amount = request.form.get('amount')
    _fee_limit = request.form.get('fee_limit', 20)

    try:
        _amount = to_sun(_amount)
        _fee_limit = to_sun(_fee_limit)

        if _amount <= 0:
            raise Exception('转账金额需大于0')
        if not is_address(_from):
            raise Exception('from 地址格式不正确')
        if not is_address(_to):
            raise Exception('to 地址格式不正确')

        client = Tron()
        priv_key = PrivateKey(bytes.fromhex(_privKey))
        contract = client.get_contract(cttAddr)
        # print('Balance', contract.functions.balanceOf(_from))
        txn = (
            contract.functions.transfer(_to, _amount)
                .with_owner(_from)
                .fee_limit(_fee_limit)
                .build()
                .sign(priv_key)
                # .inspect()
                .broadcast()
        )
        return jsonify({
            "data": txn,
            "code": 200,
            "msg": "TOKEN交易成功"
        })
    except Exception as e:
        return jsonify({
            "data": None,
            "code": 500,
            "msg": str(e)
        })


@app.route('/api/transferTrx', methods=["POST"])
def transferTrx():
    _from = request.form.get('from_address')
    _to = request.form.get('to_address')
    _privKey = request.form.get('private_key')
    _amount = request.form.get('amount')

    try:
        _amount = to_sun(_amount)

        if _amount <= 0:
            raise Exception('转账金额需大于0')
        if not is_address(_from):
            raise Exception('from 地址格式不正确')
        if not is_address(_to):
            raise Exception('to 地址格式不正确')

        client = Tron()

        priv_key = PrivateKey(bytes.fromhex(_privKey))

        txn = (
            client.trx.transfer(_from, _to, _amount)
                .memo("psex")
                .build()
                # .inspect()
                .sign(priv_key)
                .broadcast()
        )
        return jsonify({
            "data": txn,
            "code": 200,
            "msg": "TRX交易成功"
        })
    except Exception as e:
        return jsonify({
            "data": None,
            "code": 500,
            "msg": str(e)
        })


@app.route('/api/getTransaction/<string:txn_id>', methods=["GET"])
def getTransaction(txn_id):
    try:
        client = Tron()
        txn = client.get_transaction(txn_id)
        return jsonify({
            "data": txn,
            "code": 200,
            "msg": "交易查询成功"
        })
    except Exception as e:
        return jsonify({
            "data": None,
            "code": 500,
            "msg": str(e)
        })


if __name__ == "__main__":
    app.run()
    # app.run(debug=app_debug, port=app_port, host=app_host)
