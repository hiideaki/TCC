import pickle as pkl

STOPWORDS = pkl.load(open('utils/stopwords.pkl', 'rb'))

PIPELINE = pkl.load(open('utils/pipe.pkl', 'rb'))