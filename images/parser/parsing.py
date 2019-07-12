from delphin.interfaces import ace
from delphin.mrs import simplemrs, prolog, eds
import logging
import json
import os
import re


def get_pos(ep):
    if ep.pred.pos:
        return ep.pred.pos
    elif ep.pred.lemma == 'named':
        return 'n'
    else:
        return ep.pred.pos


def get_lemma(ep):
    ''' Get lemma from a pyDelphin elementary predicate '''
    if ep.carg:
        return ep.carg
    elif ep.pred.pos == 'u' and ep.pred.sense == 'unknown' and "/" in ep.pred.lemma:
        cutpoint = ep.pred.lemma.rfind('/')
        return ep.pred.lemma[:cutpoint]
    elif ep.pred.type == 0:
        return None
    else:
        return ep.pred.lemma


def get_pred(ep):
    return dict(cfrom=ep.cfrom,
                cto=ep.cto,
                pos=get_pos(ep),
                sem=ep.pred.sense,
                type=ep.pred.type,
                form=ep.pred.string,
                lemma=get_lemma(ep))


def save(result):
    logging.getLogger().setLevel(logging.INFO)

    doc = result['doc']
    line = result['line']

    logging.info('Write %s line %s', doc, line)

    outdir = os.getenv("OUTPUT_DIR")

    f = open(outdir + doc + '_' + line, "w+")
    f.write(json.dumps(result))
    f.close()


def parse(res):
    data = res.copy()
    sent = res['sent']

    infos = res.get('result_infos', ["preds", "treal", "tcpu", "total", "memory"])
    ace_args = os.getenv('ACE_ARGS')

    if ace_args:
        ace_args = re.split('\s+', ace_args)
    else:
        ace_args = ['--timeout=60', '--max-words=150',
                    '--rooted-derivations', '--udx', '--disable-generalization']

    res = ace.parse(os.getenv('ERG_DAT', '/root/erg-2018-x86-64-0.9.30.dat'),
                    sent, cmdargs=ace_args + ['-1'])

    if len(res['results']) > 0:
        x = res.result(0).mrs()

        data["parsed"] = True

        if "simplemrs" in infos:
            try:
                data["simplemrs"] = simplemrs.dumps([x])
            except:
                data["simplemrs"] = None

        if "prolog" in infos:
            try:
                data["prolog"] = prolog.dumps([x])
            except:
                data["prolog"] = None

        if "eds" in infos:
            try:
                data["eds"] = eds.dumps([x])
            except:
                data["eds"] = None

        if "preds" in infos:
            data["preds"] = [get_pred(ep) for ep in x.eps()]

        if "treal" in infos:
            data["treal"] = res["treal"]
        if "tcpu" in infos:
            data["tcpu"] = res["tcpu"]
        if "total" in infos:
            data["total"] = res["total"]
        if "memory" in infos:
            data["memory"] = res["others"]

    else:
        data["parsed"] = False

    save(data)

    return True
