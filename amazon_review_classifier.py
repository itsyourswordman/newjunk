import json
from sklearn.model_selection import train_test_split #split
from sklearn.feature_extraction.text import CountVectorizer  #bags of words matrix
from sklearn import svm  #classification
import random

class Review(object):
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.sentiment=self.get_sentiment()

    def get_sentiment(self):
        if self.score<=2:
            return "NEGATIVE"
        elif self.score==3:
            return "NEUTRAL"
        else:
            return "POSITIVE"

class ReivewContainer:
    def __init__(self,reviews):
        self.reviews=reviews

    def evenly_distribute(self):
        negative= filter(lambda x:x.sentiment=='NEGATIVE', self.reviews)
        positive=filter(lambda x:x.sentiment=='POSITIVE', self.reviews)
        positive_shrunk=positive[:len(negative)]
        self.reviews=negative+positive_shrunk
        random.shuffle(self.reviews)


file_name = 'Books_small.json'
reviews = []
with open(file_name) as f:
    for line in f:
        review = json.loads(line)
        reviews.append(Review(review['reviewText'], review['overall']))

print(reviews[5].score) #test

training,test=train_test_split(reviews,test_size=0.33)
print(training[0].sentiment)

train_x=[x.text for x in training]
train_y=[x.sentiment for x in training]
test_x=[x.text for x in test]
test_y=[x.sentiment for x in test]

train_container=ReivewContainer(training)
test_container=ReivewContainer(test)

train_container.evenly_distribute()
train_x=train_container.get_text()
train_y=train_container.get_sentiment()

test_container.evenly_distribute()
test_x=train_container.get_text()
test_y=train_container.get_sentiment()

print(train_x[0])
vectorizer=CountVectorizer()
train_x_vectors=vectorizer.fit_transform(train_x)
test_x_vectors=vectorizer.transform(test_x)

train_x_vectors[0]
train_x_vectors[0].toarray()


clf_svm= svm.SVC(kernel='linear')
clf_svm.fit(train_x_vectors,train_y) #fit x and y to classifier
print(clf_svm.predict(test_x_vectors[0]))

#Decision Tree
from sklearn.tree import  DecisionTreeClassifier
clf_dec= DecisionTreeClassifier()
clf_dec.fit(train_x_vectors,train_y)
print(clf_dec.predict(test_x_vectors[0]))

#Naive Bayes
from sklearn.naive_bayes import GaussianNB
clf_gnb=GaussianNB()
clf_gnb.fit(train_x_vectors,train_y)
print(clf_gnb.predict(test_x_vectors[0]))

#Logistic Regression
from sklearn.linear_model import LogisticRegression
clf_lgr=LogisticRegression()
clf_lgr.fit(train_x_vectors,train_y)
print(clf_lgr.predict(test_x_vectors[0]))

#EVALUATION

clf_svm.score(test_x_vectors,test_y)
clf_dec.score(test_x_vectors,test_y)
#mean accuracy
#log>svm>dec=gnb

from sklearn.metrics import f1_score
#F1 score

f1_score(test_y,clf_svm.predict(test_x_vectors),average=None,labels=['POSITIVE','NEUTRAL','NEGATIVE'])
#返回的数值是在三种评价中model的表现如何 准确率如何
#positive表现最好 其余两个表现不好

print(train_y.count(('POSITIVE'))) #count how many positive in training data in total
#one way to improve performance is to increase train data, that is, increase the size of dataset



