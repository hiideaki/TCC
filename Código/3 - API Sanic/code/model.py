from unidecode import unidecode
import re
import pickle as pkl
from lime.lime_text import LimeTextExplainer

class Model():

    def __init__(self, text, verbose=1):
        self.stopwords = pkl.load(open('utils/stopwords.pkl', 'rb'))

        self.pipeline = pkl.load(open('utils/pipe.pkl', 'rb'))
        
        self.verbose = verbose
        self.text = text

    def inference(self):
        clean_text = self.clean_text(self.text)
        y_pred = int(self.pipeline.predict([clean_text])[0])
        y_proba = int(max(self.pipeline.predict_proba([clean_text])[0]) * 100)
        
        explainer = LimeTextExplainer(class_names=[0, 1])
        
        exp = explainer.explain_instance(clean_text, self.pipeline.predict_proba, num_features=10)

        results = {
            'pred': y_pred,
            'proba': y_proba,
            'lime': exp.as_list()
        }

        print(results)

        return results

    def clean_text(self, text):
        # Making sure we're dealing with strings and lowering the characters
        text = str(text).lower()
        
        # Stripping accents
        text = unidecode(text)
        
        # Removing characters that aren't alphanumeric
        text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
        
        # Removing tokens that intercalate between letters and digits
        text = re.sub(r'\w*([a-zA-Z][0-9]|[0-9][a-zA-Z])\w*', ' ', text)
        
        # Removing digits
        text = re.sub(r'\d', ' ', text)
        
        # Removing tokens with letters that appear more than twice in a row
        text = re.sub(r'\w*([a-zA-Z])\1{2,}\w*', ' ', text)
        
        # Removing extra spaces
        text = re.sub('\s+', ' ', text)
        
        # Removing words with length equal or lower than 2 or are in STOPWORDS
        return ' '.join([token for token in text.split() if len(token) > 2 and token not in self.stopwords])