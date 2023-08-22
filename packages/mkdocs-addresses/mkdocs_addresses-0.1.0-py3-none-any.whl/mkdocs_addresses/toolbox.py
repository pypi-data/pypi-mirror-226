import re
import json
import math
from typing import Dict

from .exceptions import AddresserError







def fatal_if(truthy, msg:str, exc=AddresserError):
    if truthy:
        raise exc(msg)




def plugin_dump_padder(k:str, pad=25):
    return k.ljust(pad * math.ceil( len(k) / pad ))


def build_other_snippet(name:str, dct:Dict):
    return f'"{name}": { json.dumps(dct, indent=4) }'


def extract_external_links_refs_in_md(markdown:str):
    """ Extract all the identifiers of externals links in the given markdown code:
                [...][identifier]
    """
    return re.findall(r'\[[^\]]*\]\[([^\]]+)\]', markdown)
