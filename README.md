# commentClassification
Taobao comments classification project for Data Analysis.

## Comment Classification
You can use module [readData.py](https://github.com/hejm37/commentClassification/blob/master/readData.py) to read the data in [data directory](https://github.com/hejm37/commentClassification/tree/master/dataDir/data).

The data in file *part1.csv, part2.csv, part4.csv, template1.csv, template2.csv* has two labels. The first label indicates if the comment is a template comment. The second label indicates if the comment is helpful. (These data are labeled by one person. It should be consistent.)

Jupyter notebook files *simpleEvaluation.ipynb* shows the result of classifications using different method in sklearn.

## Data Crawling
The code of data crawling and preprocessing is not well organized and managed (sorry for that). But still, these files maybe helpful to you:

*craw_tb.py*: Taobao comments crawling

*craw_corpus.py*: Crawling more data to train word2vec model

*prepareCorpus.py*: Prepare corpus for training word2vec model

*word2Vec.py*: Word2vec model training
