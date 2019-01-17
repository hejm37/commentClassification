import logging
import os.path
import sys
import re
import jieba
from utils import remove_noise, q_to_b

# word2vec语料预处理，主要为去噪、分词
# 参考: https://www.jianshu.com/p/6d542ff65b1e

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info('running %s' % ' '.join(sys.argv))

    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
# 下面一行注释为编辑器语法检查的设置，不用管
# pylint: disable=unbalanced-tuple-unpacking
    inp, outp = sys.argv[1:3]
    space = ' '
    i = 0

    finput = open(inp)
    foutput = open(outp, 'w')   # exiting file will be erased.
    finput.readline()
    for line in finput:
        # remove some noise character before segmentation
        line_seg = jieba.cut(remove_noise(line))
        foutput.write(space.join(line_seg))
        i = i + 1
        if (i % 1000 == 0):
            logger.info("Saved " + str(i) + " ")