from flask import Blueprint, render_template, request, redirect, session, current_app

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range (1, 11):
    offices.append({"number": i, "tenant": ""})

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }