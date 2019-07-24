from delphin.interfaces import ace
import logging
import json
import os
import re


def save(result):
    logging.getLogger().setLevel(logging.INFO)

    doc = result['doc']
    line = result['line_num']

    logging.info('Write %s line %s', doc, line)

    outdir = os.getenv("OUTPUT_DIR")

    f = open(outdir + doc + '_' + line, "w+")
    f.write(json.dumps(result, default=str))
    f.close()


def parse(datum):
    ace_args = os.getenv('ACE_ARGS')

    if ace_args:
        ace_args = re.split('\s+', ace_args)
    else:
        ace_args = ['--timeout=60', '--max-words=150',
                    '--rooted-derivations', '--udx', '--disable-generalization']

    res = ace.parse(os.getenv('ERG_DAT', '/root/erg-2018-x86-64-0.9.30.dat'),
                    datum['sent'], cmdargs=ace_args + ['-1'])

    res["line_num"] = datum["line_num"]
    res["doc"] = datum["doc"]
    save(res)
    return True
