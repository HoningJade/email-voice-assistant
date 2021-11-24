'''
API for text summarization

https://deepai.org/machine-learning-model/summarization


'''

import requests
import io
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import string

class Summarize():

    def __init__(self, api_key='061c9c38-576a-458b-b0dd-5b94e6bbcfca'):
        self.api_key = api_key
        self.stop_words = ENGLISH_STOP_WORDS.union(set(string.punctuation))

    def _tokenize(self, text):
        '''returns tokenized text'''
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)
        words = []
        for (word, tag) in tagged:
            if word in self.stop_words:
                continue
            if word.startswith('\''):
                continue
            if tag.startswith('N'):
                words.append(word)
        return words

    def _get_keywords(self, text, k=5, meta=None):
        '''extract top k keywords from email content'''
        vectorizer = TfidfVectorizer(tokenizer=self._tokenize, lowercase=True, )#stop_words=set(ENGLISH_STOP_WORDS)
        X = vectorizer.fit_transform([text]).toarray().squeeze()
        words = np.array(vectorizer.get_feature_names())
        topk_words = words[(np.argsort(X)[::-1])[:k]]
        topk_words.sort()
        filtered_words = [topk_words[0]]
        for i in range(1, len(topk_words)):
            if str(PorterStemmer().stem(topk_words[i])) == str(PorterStemmer().stem(topk_words[i-1])):
                continue
            filtered_words.append(topk_words[i])
        filtered_words = set(filtered_words)

        if meta is not None:
            title_tokens = set(self._tokenize(meta['title'])) if 'title' in meta else set()
            author_tokens = set(self._tokenize(meta['author'])) if 'author' in meta else set()

        return (
            list(filtered_words & title_tokens - author_tokens),
            list((filtered_words | title_tokens) - author_tokens - (filtered_words & title_tokens))
        )
        
    def summarize(self, text: str, mode='tfidf', k=5, meta=None) -> str:
        '''
        text:       text string containing the fattened email
        mode:       whether to use 'tfidf' or to use 'api' directly, api is not recommended
        k:          #keywords to extract, used only if mode is 'tfidf'
        meta:       meta information of the email in dict format
        returns:    a string containing the summary
        '''
        if mode == 'tfidf':
            if meta is not None and 'author' in meta:
                ret_str = str(meta['author']) + " emails you "
            else:
                ret_str = "The email is "
            # matched keywords appear in both the title and contents
            matched, others = self._get_keywords(text, k, meta)
            if len(matched) > 0:
                ret_str += "mainly about "
                if len(matched) > 1:
                    for word in matched[:-1]:
                        ret_str += word + ", "
                    ret_str += "and " + matched[-1] + '. '
                if len(others) > 1:
                    ret_str += "It also talks about "
                    for word in others[:-1]:
                        ret_str += word + ", "
                    ret_str += "and " + others[-1] + '.'
            else:
                ret_str += " about "
                for word in others[:-1]:
                    ret_str += word + ", "
                ret_str += "and " + others[-1] + '.'
            return ret_str
            
        elif mode == 'api':
            raise DeprecationWarning # "The api version of summary is not recommended"
            response = requests.post(
                "https://api.deepai.org/api/summarization",
                data={'text': text,},
                headers={'api-key': self.api_key})
            summary = response.json()['output']
            return "Here is a quick summary of the email. " + summary
        
        else:
            raise NotImplementedError

if __name__ == '__main__':
    '''
    The main function here provides a simple demo
    '''
    summarizer = Summarize()
    # email text to be summarized
    text = """Peter, application deadlines are rapidly approaching! If you're ready to apply, head to gradapply.rice.edu. Deadlines vary by program, so be sure to verify the deadlines that pertain to your application.
        Have lingering questions about grad school life or the application process? Join us Thursday, Nov. 18, to chat with our Graduate Student Ambassadors at one of our Coffee Chats - sign up for the time that works for you here!
        To help you decide your plan of action, we've listed some commonly asked questions below, and more are on our website. Not seeing your question? Let us know! Refer to your program of interest for additional application requirements.
        How can I take a campus tour?
        We're happy to share our virtual tour with you! Click on the image below to watch a video about Rice's beautiful, green campus, set in the heart of Houston. You can also virtually visit Rice at one of our upcoming Coffee Chats! Register here.
        Where should my official transcripts be sent?
        Send official transcripts directly to the program to which you intend to apply. You may also upload an unofficial transcript directly within your online application.
        How do I report my GRE or TOEFL scores?
        A reminder that this year the GRE is optional at Rice, excluding programs in the Jones School of Business, though many programs will suggest you submit scores. To officially report your scores, visit the ETS website to order score reports if you did not do so on your test day. The ETS institutional reporting code for Rice University is 6609. Please allow 2-4 weeks for scores to reach Rice.
        I sent my GRE/TOEFL scores, but the application system shows my scores as pending.
        If your scores are not yet showing in your application, you can check with ETS to make sure you sent the scores using the correct code. You can also contact the program you are applying to and make them aware of this. They can open your application and match the scores.
        How are letters of recommendation submitted?
        Letters can be submitted within the application itself using a valid email address for your recommenders. More on this here.
        My recommender didn't get the request. What do I do?
        Please note that it is possible that the email generated by our application system was filtered as spam. You can log back into the application and resend your letter of recommendation.
        Can I edit my application after I submit it?
        Some programs will permit important minor edits to your application; please contact them directly with requests."""
    # optional email meta information
    meta = {
        'author':   'Rice University Graduate and Postdoctoral Studies',
        'datatime': 'Nov 16, 2021, 3:22 PM',
        'title':    'Rice University application deadlines are approaching!'
    }
    # get the summary by calling the summary function
    summary = summarizer.summarize(text, meta=meta, k=10)
    print(summary)


''' documentation

# Example posting a text URL:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example posting a local text file:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    files={
        'text': open('/path/to/your/file.txt', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example directly sending a text string:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_HERE',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


###############################################################################

import base64

# Let's use deepAI developed API
# https://docs.deepaffects.com/docs/text-summary-api.html

url = "https://proxy.api.deepaffects.com/text/generic/api/v1/async/summary"

querystring = {"apikey":"<API_KEY>", "webhook":"<WEBHOOK_URL>"}

payload = {"summaryType": "abstractive", "model": "iamus", "summaryData": [{"speakerId":"spk", "text":"text blob for speaker"}]}

headers = {
    'Content-Type': "application/json",
}

response = requests.post(url, json=payload, headers=headers, params=querystring)


'''