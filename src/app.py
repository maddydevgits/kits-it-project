import json
from web3 import Web3,HTTPProvider
from flask import Flask,request,render_template
import urllib3

app=Flask(__name__)

blockchain='http://127.0.0.1:7545'

def connect():
    web3=Web3(HTTPProvider(blockchain))
    web3.eth.defaultAccount=web3.eth.accounts[0]

    artifact="../build/contracts/demo.json"
    with open(artifact) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    
    contract=web3.eth.contract(
        abi=contract_abi,
        address=contract_address
    )
    return web3,contract


@app.route('/print',methods=['GET','POST'])
def print1():
    web3,contract=connect()
    data=contract.functions.print().call()
    print(data)
    return (data)

@app.route('/scan',methods=['GET','POST'])
def scan1():
    data=request.args.get('data')
    web3,contract=connect()
    tx_hash=contract.functions.scan(data).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return 'transaction success'

@app.route('/sendDataToPython',methods=['GET','POST'])
def sendDataToPython():
    data=request.form['data']
    http=urllib3.PoolManager()
    response=http.request('get','http://127.0.0.1:5002/scan?data='+data)
    response=response.data
    return render_template('index.html',msg=response.decode('utf-8'))

@app.route('/scanDataFromPython',methods=['GET','POST'])
def scanDataFromPython():
    http=urllib3.PoolManager()
    response=http.request('get','http://127.0.0.1:5002/print')
    response=response.data
    return render_template('index.html',name=response.decode('utf-8'))

@app.route('/')
def home():
    return render_template('index.html')

if __name__=="__main__":
    app.run(port=5002)