import json

from flask import Blueprint, request, Response

from app.mimetype import correct_format, mimetype_map
from lib import semantics

semantic_adapter = Blueprint('semantic_adapter', __name__, template_folder='../templates')

@semantic_adapter.route('/<ethNetwork>/accounts/<id>')
def accounts(ethNetwork, id):
    output_format = correct_format(request.args.get('format'))
   
    return Response(semantics.semantic_accounts(id, request.url, ethNetwork, output_format ),
                    mimetype=mimetype_map[output_format])

@semantic_adapter.route('/<ethNetwork>/contracts/<id>')
def contracts(ethNetwork, id):
    output_format = correct_format(request.args.get('format'))
   
    return Response(semantics.semantic_contracts(id, request.url, ethNetwork, output_format ),
                    mimetype=mimetype_map[output_format])

@semantic_adapter.route('/<ethNetwork>/blocks/<id>')
def blocks(ethNetwork,id):
    output_format = correct_format(request.args.get('format'))
   
    return Response(semantics.semantic_block(id, request.url, ethNetwork, output_format ),
                    mimetype=mimetype_map[output_format])

@semantic_adapter.route('/<ethNetwork>/blocks/<id>/uncles/<uncle_id>')
def uncles(ethNetwork,id,uncle_id):
    output_format = correct_format(request.args.get('format'))
   
    return Response(semantics.semantic_uncle(id, uncle_id,request.url,  ethNetwork, output_format),
                    mimetype=mimetype_map[output_format])

@semantic_adapter.route('/<ethNetwork>/transactions/<id>')
def transactions(ethNetwork,id):
    output_format = correct_format(request.args.get('format'))
   
    return Response(semantics.semantic_transaction(id, request.url,  ethNetwork, output_format),
                    mimetype=mimetype_map[output_format])

@semantic_adapter.route('/<ethNetwork>/receipts/<transaction>')
def receipts(ethNetwork,transaction):
    output_format = correct_format(request.args.get('format'))
   
    return Response(semantics.semantic_receipt(transaction, request.url,  ethNetwork, output_format),
                    mimetype=mimetype_map[output_format])
