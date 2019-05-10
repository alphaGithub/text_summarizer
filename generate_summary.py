import time 
import numpy as np  
import tensorflow as tf 
import pickle 
import re 
from nltk.corpus import stopwords
import os 

epochs =  20 # use 50
batch_size = 64
rnn_size = 256
num_layers = 3
learning_rate = 0.008
keep_probability = 0.75
pwd = os.getcwd()
checkpoint = pwd+"/model/best_model.ckpt"

contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}



def clean_text(text, remove_stopwords):
    text = text.lower()
    if True:
        text = text.split()
        new_text = []
        for word in text:
            if word in contractions:
                new_text.append(contractions[word])
            else:
                new_text.append(word)
        text = " ".join(new_text)

    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\<a href', ' ', text)
    text = re.sub(r'&amp;', '', text) 
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
    text = re.sub(r'<br />', ' ', text)
    text = re.sub(r'\'', ' ', text)
    if remove_stopwords:
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)
    return text

fp = open(pwd+"/data/vocab_to_int","rb")
vocab_to_int = pickle.load(fp)
fp = open(pwd+"/data/clean_texts","rb")
clean_texts=pickle.load(fp)
fp = open(pwd+"/data/reviews" , "rb")
reviews = pickle.load(fp)
fp = open(pwd+"/data/int_to_vocab","rb")
int_to_vocab = pickle.load(fp)

def text_to_seq(text):
    text = clean_text(text, remove_stopwords=True)
    return [vocab_to_int.get(word, vocab_to_int['<UNK>']) for word in text.split()]



def summary(input_sentence):

    input_sentence = clean_text(str(input_sentence),remove_stopwords=True)
    input_sentences = [input_sentence]
    output_summary = ""
    #Sample_sentences=["The coffee tasted great and was at such a good price! I highly recommend this to everyone!"]
    #Sample_sentences=["love individual oatmeal cups found years ago sam quit selling sound big lots quit selling found target expensive buy individually trilled get entire case time go anywhere need water microwave spoon know quaker flavor packets"]
    generagte_summary_length =  [3]

    texts = [text_to_seq(input_sentence) for input_sentence in input_sentences]
    if type(generagte_summary_length) is list:
        if len(input_sentences)!=len(generagte_summary_length):
            raise Exception("[Error] makeSummaries parameter generagte_summary_length must be same length as input_sentences or an integer")
        generagte_summary_length_list = generagte_summary_length
    else:
        generagte_summary_length_list = [generagte_summary_length] * len(texts)


    loaded_graph = tf.Graph()
    with tf.Session(graph=loaded_graph) as sess:
        loader = tf.train.import_meta_graph(checkpoint + '.meta')
        loader.restore(sess, checkpoint)
        input_data = loaded_graph.get_tensor_by_name('input:0')
        logits = loaded_graph.get_tensor_by_name('predictions:0')
        text_length = loaded_graph.get_tensor_by_name('text_length:0')
        summary_length = loaded_graph.get_tensor_by_name('summary_length:0')
        keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')
        for i, text in enumerate(texts):
            generagte_summary_length = generagte_summary_length_list[i]
        
            answer_logits = sess.run(logits, {input_data: [text]*batch_size, 
                                          summary_length: [generagte_summary_length],
                                          text_length: [len(text)]*batch_size,
                                          keep_prob: 1.0})[0] 
            pad = vocab_to_int["<PAD>"] 
            l=len(int_to_vocab)
            print(answer_logits)
            output_summary =' {}\n\r\n\r'.format("  ".join([int_to_vocab[j] for j in answer_logits if (j!=pad and j<l) ]))
    return output_summary

