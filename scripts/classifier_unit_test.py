import numpy as np
from sklearn.metrics import *
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.inspection import permutation_importance
from matplotlib import pyplot as plt
import time
import datetime

def permutate(clf, X_train, y_train):
    print("Perfoming *raw* permutation importance...")
    if type(X_train) != np.ndarray:
        X_train = X_train.toarray()
    if type(y_train) != np.ndarray:
        y_train = y_train.toarray()

    result = permutation_importance(clf, X_train, y_train)
    return result

def ht(pred, dum):
    #higher than
    if pred > dum:
        return ':-)'
    elif dum > pred:
        return ':-('
    return ':-|'

def check_fitted(clf): 
    return hasattr(clf, "classes_")

def fpr_tpr(preds_proba, y_test, name=None):
    y_test = label_binarize(y_test, classes=np.unique(y_test))

    fpr, tpr, _ = roc_curve(y_test.ravel(), preds_proba.ravel())

    print(f"ROC AUC control for {name}: {auc(fpr, tpr):.2f}")

    return fpr, tpr

def test_classifier(classifier, X_train, X_test, y_train, y_test, strategy="most_frequent",
                    give_roc=True, give_importance=False, model_name=None):
    '''Takes preprocessed data as input, categorized labels
    strategy: DummyClassifier strategy,
    give_roc: output tpr, fpr? Takes longer time
    give_importances: output feature importances? Takes a lot longer.
    Is give_roc enabled, the function will return tpr, fpr for classifier and dummy.'''
    
    og_time = time.time()
    output = {}

    if not check_fitted(classifier):
        print("Training model...")
        classifier.fit(X_train, y_train)
    else:
        print("Oh, model already fit. Thanks!")
        
    preds = classifier.predict(X_test)
    preds_prob = classifier.predict_proba(X_test)

    print("Training dummy...")
    dum = DummyClassifier(strategy=strategy).fit(X_train, y_train)
    dum_preds = dum.predict(X_test)
    dum_probs = dum.predict_proba(X_test)

    correct = accuracy_score(y_test,preds,normalize=False)
    dum_correct = accuracy_score(y_test,dum_preds,normalize=False)
    accuracy = accuracy_score(y_test, preds)
    dum_accuracy = accuracy_score(y_test, dum_preds)
    bal_accuracy = balanced_accuracy_score(y_test, preds)
    dum_bal_accuracy = balanced_accuracy_score(y_test, dum_preds)
    f1 = f1_score(y_test, preds, average='weighted')
    dum_f1 = f1_score(y_test, dum_preds, average='weighted')
    top_k = top_k_accuracy_score(y_test, preds_prob, k=5)
    dum_top_k = top_k_accuracy_score(y_test, dum_probs)
    cohen = cohen_kappa_score(y_test, preds)
    dum_cohen = cohen_kappa_score(y_test, dum_preds)
    
    if len(set(y_test))==2:
        auc = roc_auc_score(y_test, preds_prob[:,1])
        dum_auc = roc_auc_score(y_test, dum_probs[:,1])
    else:
        auc = roc_auc_score(y_test, preds_prob, multi_class='ovr')
        dum_auc = roc_auc_score(y_test, dum_probs, multi_class='ovr')

    print('-'*10)
    print(f"Correctly predicted {correct} of {len(preds)}\tDummy: {dum_correct} of {len(preds)}\t{ht(correct, dum_correct)}")
    print(f"Accuracy: {accuracy:.2f}\t\t\tDummy: {dum_accuracy:.2f}\t{ht(accuracy, dum_accuracy)}")
    print(f"Balanced accuracy: {bal_accuracy:.2f}\t\tDummy: {dum_bal_accuracy:.2f}\t{ht(bal_accuracy, dum_bal_accuracy)}")
    print(f"TOP 5 accuracy: {top_k:.2f}\t\tDummy: {dum_top_k:.2f}\t{ht(top_k, dum_top_k)}")
    print(f"F1 score: {f1:.2f}\t\t\tDummy: {dum_f1:.2f}\t{ht(f1, dum_f1)}")
    print(f"Cohen's Kappa: {cohen:.2f}\t\tDummy: {dum_cohen:.2f}\t{ht(cohen, dum_cohen)}")
    print(f"ROC AUC: {auc:.2f}\t\t\tDummy: {dum_auc:.2f}\t{ht(auc, dum_auc)}")
    print('-'*10)

    metrics = dict()
    metrics['correct'] = correct
    metrics['accuracy'] = accuracy
    metrics['bal_accuracy'] = bal_accuracy
    metrics['f1'] = f1
    metrics['auc'] = auc
    metrics['top5_accuracy'] = top_k
    metrics['cohen'] = cohen

    dum_metrics = dict()
    dum_metrics['correct'] = dum_correct
    dum_metrics['accuracy'] = dum_accuracy
    dum_metrics['bal_accuracy'] = dum_bal_accuracy
    dum_metrics['f1'] = dum_f1
    dum_metrics['auc'] = dum_auc
    dum_metrics['top5_accuracy'] = dum_top_k
    dum_metrics['cohen'] = dum_cohen


    if give_roc:
        fpr, tpr = fpr_tpr(preds_prob, y_test, name=str(classifier))
        dum_fpr, dum_tpr = fpr_tpr(dum_probs, y_test, name="Dummy")

        output['tpr'] = tpr
        output['fpr'] = fpr
        output['dum_tpr'] = dum_tpr
        output['dum_fpr'] = dum_fpr

    if give_importance:
        importances = permutate(classifier, X_train, y_train)
        output['importances_mean'] = importances.importances_mean
        output['importances_std'] = importances.importances_std

    if model_name:
        output['name'] = model_name
    
    output['model_type'] = str(classifier)
    output['fedtet_estimator'] = classifier
    output['preds'] = preds
    output['preds_proba'] = preds_prob
    output['dum_preds'] = dum_preds
    output['dum_preds_proba'] = dum_probs
    output['cnf_matrix'] = confusion_matrix(y_test, preds)
    output['dum_cnf_matrix'] = confusion_matrix(y_test, dum_preds)
    output['metrics'] = metrics
    output['dum_metrics'] = dum_metrics
    
    # print("\nOutput keys:")
    # for i in output.keys():
    #     print(i)
    process_time = str(datetime.timedelta(seconds=time.time()-og_time))
    print("Process time:", process_time)
    output['proctime'] = process_time
    
    return output

    
    
if __name__ == "__main__":
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    
    iris = datasets.load_iris()
    X,y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    clf = LogisticRegression()
    output = test_classifier(clf, X_train, X_test, y_train, y_test, give_roc=True, give_importance=True)
    


    
