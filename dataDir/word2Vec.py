import logging
import os.path
import sys
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# word2vec训练
# 参考: https://www.jianshu.com/p/6d542ff65b1e

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logging.info("running %s" % ' '.join(sys.argv))

    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
# pylint: disable=unbalanced-tuple-unpacking
    inputFile, modelFile = sys.argv[1:3]

    model = Word2Vec(LineSentence(inputFile), size=100, window=5,
        min_count=5, workers=multiprocessing.cpu_count())
    model.save(modelFile)
