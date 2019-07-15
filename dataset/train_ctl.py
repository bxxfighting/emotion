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

from dataset.data_ctl import list_comment_for_train
from dataset.data_ctl import list_stopword_for_train
from dataset.models import CommentModel


def cut_words(text):
    return ' '.join(jieba.cut(text))


def train():
    comments = list_comment_for_train()
    df = pd.DataFrame(comments, columns=['comment', 'label'])

    x = df[['comment']]
    y = df[['label']]

    x['cut_comment'] = x.comment.apply(cut_words)

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)

    def get_stopwords(path):
        with open(path) as f:
            stopwords = f.read()
        stopwords_list = stopwords.split('\n')
        return stopwords_list

    stopwords = list_stopword_for_train()

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

    emotion_dict = dict(CommentModel.LABEL_CHOICES)

    for x, y in list(zip(x_test.cut_comment.values, y_test.label.values))[:50]:
        r = pipe.predict([x])
        if y == r[0]:
            result = 'O'
        else:
            result = 'X'
        print(result, ' : ', x, ' 真实值：', emotion_dict[y], ' 预测值: ', emotion_dict[r[0]])
