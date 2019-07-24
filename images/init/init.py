from redis import StrictRedis, Redis
from rq import Queue
from settings import REDIS_HOST, REDIS_PORT
import os
import logging
import datetime
import glob


def get_docs(dir):
    return list(glob.glob(dir + "*.sent"))


def put_sents(docs, queue, init_time, in_dir):
    for doc in docs:
        sents = [line.rstrip('\n') for line in open(doc)]
        line = 0
        for sent in sents:
            if sent != '':
                queue.enqueue("parsing.parse", {"sent": sent.strip(),
                                                "doc": doc.split('/')[-1],
                                                "line_num": str(line),
                                                "init_time": init_time,
                                                "dir": in_dir})
                line = line + 1
        logging.info('Enqueue %s sentences from %s', line, doc)


if __name__ == '__main__':

    init_time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")

    logging.getLogger().setLevel(logging.INFO)

    logging.info('Connecting to redis server...')

    redis_server_ready = False

    while not redis_server_ready:
        try:
            Redis(REDIS_HOST, REDIS_PORT).ping()
            redis_server_ready = True
        except:
            pass

    logging.info('Sucefful connected!')

    q = Queue('parse', connection=StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT), default_timeout=600)

    docs = get_docs(os.getenv('INPUT_DIR', 'test'))

    logging.info('%s documents found in %s dir', len(
        docs), os.getenv('INPUT_DIR', 'test'))

    put_sents(docs, q, init_time, os.getenv('INPUT_DIR'))
