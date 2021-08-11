# Based on the code of the 'ehonlia' author of the semantic-adapter 
# of project https://github.com/EricssonResearch/iot-framework-engine

import inspect
from flask import Flask, url_for, render_template, request

from app.semantic_adapter import semantic_adapter
from app.semantic_adapter_ethon import semantic_adapter_ethon
#from rdflib_web.endpoint import endpoint

app = Flask(__name__,
            static_folder='static')
app.register_blueprint(semantic_adapter)
#app.config['graph'] = "sampleEthon.turtle"
#app.register_blueprint(semantic_adapter_ethon, url_prefix='/ethon')
#app.register_blueprint(endpoint)

@app.route('/')
def site_map():
    links = ["/mainnet/blocks/1?format=turtle", 
             "/ropsten/blocks/4900105/uncles/0?format=n3",
             "/mainnet/blocks/1?format=xml",
             "/ropsten/blocks/4900105?format=json-ld",
             "/ropsten/blocks/4900105/transactions/0" ,
             "/ropsten/contracts/CC958703EBB101A652F790299d4D46E85785bCA1?format=n3",
             "/ropsten/receipts/e05eb7bd055e4d5c6ed507f4169523c1d848b570cc3ca83cdd45df0d5abd2705?format=n3"]
   
    return render_template('index.html', url=request.url, links=links)

@app.route('/ethextras.owl')
def ontology():
    return app.send_static_file('ethextras.owl')