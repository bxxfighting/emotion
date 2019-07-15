import os
import jieba
import pkuseg
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

# 这是北大的分词工具，跟jieba选哪个都可以，我试了试，各有好坏吧
# seg = pkuseg.pkuseg()
# cut_model = seg
cut_model = jieba

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR, 'data/comment.csv')
stopwords_path = os.path.join(BASE_DIR, 'data/stopwords.txt')

df = pd.read_csv(data_path)
x = df[['comment']]
y = df[['label']]

def cut_words(text):
    return ' '.join(cut_model.cut(text))

x['cut_comment'] = x.comment.apply(cut_words)

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

def get_stopwords(path):
    with open(path) as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    return stopwords_list

stopwords = get_stopwords(stopwords_path)

max_df = 0.8
min_df = 3

# vect = CountVectorizer(max_df=max_df, min_df=min_df,
#         token_pattern='(?u)\\b[^\\d\\W]\\w+\\b',
#         stop_words=frozenset(stopwords))
vect = CountVectorizer(token_pattern='(?u)\\b[^\\d\\W]\\w+\\b',
        stop_words=frozenset(stopwords))

term_matrix = pd.DataFrame(vect.fit_transform(x_train.cut_comment).toarray(),
        columns=vect.get_feature_names())

nb = MultinomialNB()
pipe = make_pipeline(vect, nb)

cross_val_score(pipe, x_train.cut_comment, y_train, cv=5, scoring='accuracy').mean()

pipe.fit(x_train.cut_comment, y_train)

y_pred = pipe.predict(x_test.cut_comment)
# print(y_pred)
print(metrics.accuracy_score(y_test, y_pred))
# print(metrics.confusion_matrix(y_test, y_pred))

emotion_dict = {
    0: '负面评价',
    1: '正面评价',
}

for x, y in list(zip(x_test.cut_comment.values, y_test.label.values))[:50]:
    r = pipe.predict([x])
    if y == r[0]:
        result = 'O'
    else:
        result = 'X'
    print(result, ' : ', x, ' 真实值：', emotion_dict[y], ' 预测值: ', emotion_dict[r[0]])
