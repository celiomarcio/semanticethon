import json

from flask import Blueprint, request, Response

from app.mimetype import correct_format, mimetype_map
from lib import semantics

semantic_adapter_ethon = Blueprint('semantic_adapter_ethon', __name__, template_folder='../templates')

#@semantic_adapter_ethon.route('/<ethNetwork>/blocks/<id>')
#def blocks(ethNetwork,id):
#    output_format = correct_format(request.args.get('format'))
   
#    return Response(semantics.semantic_block(id, request.url, ethNetwork, output_format ),
#                    mimetype=mimetype_map[output_format])

