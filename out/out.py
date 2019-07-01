import logging
import json
import os


def put(result):
    logging.getLogger().setLevel(logging.INFO)

    doc = result['doc']
    line = result['line']

    logging.info('Write %s line %s', doc, line)

    outdir = os.getenv("OUTPUT_DIR")

    f = open(outdir + doc + '_' + line, "w+")
    f.write(json.dumps(result))
    f.close()
