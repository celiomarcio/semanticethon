JSON = 'application/json'

mimetype_map = {
    'xml': 'application/rdf+xml',
    'json-ld': JSON,
    'n3': 'text/n3',
    'turtle': 'application/x-turtle',
   # None: 'text/xml'
}

def correct_format(output_format):
    if output_format is None:
        corrected_output_format = 'xml'
    else:
        corrected_output_format = output_format

    return corrected_output_format