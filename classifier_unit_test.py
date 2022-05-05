import numpy as np
from sklearn.metrics import *
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.inspection import permutation_importance
from matplotlib import pyplot as plt

def permutate(clf, X_train, y_train):
    print("Perfoming permutation importance...")
    if type(X_train) != np.ndarray:
        X_train = X_train.toarray()
    if type(y_train) != np.ndarray:
        y_train = y_train.toarray()

    result = permutation_importance(clf, X_train, y_train)
    print("Permutation imporance done! Note, that vector features are not accounted for. Raw importances returned.")
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

def fpr_tpr(classifier, X_train, X_test, y_train, y_test):
    y_train = label_binarize(y_train, classes=np.unique(y_train))
    y_test = label_binarize(y_test, classes=np.unique(y_test))
    
    clf = OneVsRestClassifier(classifier)

    y_score = clf.fit(X_train, y_train).predict_proba(X_test)
    print(y_test.ravel().shape, y_score.ravel().shape)
    if y_test.ravel().shape == y_score.ravel().shape:
        fpr, tpr, _ = roc_curve(y_test.ravel(), y_score.ravel())
    else:
        fpr, tpr, _ = roc_curve(y_test.ravel(), y_score[:,0])

    return fpr, tpr

def test_classifier(classifier, X_train, X_test, y_train, y_test, strategy="most_frequent",
                    give_roc=False, give_importance=False):
    '''Takes preprocessed data as input, categorized labels
    strategy: DummyClassifier strategy,
    give_roc: output tpr, fpr? Takes longer time
    give_importances: output feature importances? Takes a lot longer.
    Is give_roc enabled, the function will return tpr, fpr for classifier and dummy.'''

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
    
    if len(set(y_test))==2:
        auc = roc_auc_score(y_test, preds_prob[:,1])
        dum_auc = roc_auc_score(y_test, dum_probs[:,1])
    else:
        auc = roc_auc_score(y_test, preds_prob, multi_class='ovr')
        dum_auc = roc_auc_score(y_test, dum_probs, multi_class='ovr')

    print(f"Correctly predicted {correct} of {len(preds)}\tDummy: {dum_correct} of {len(preds)}\t{ht(correct, dum_correct)}")
    print(f"Accuracy: {accuracy:.2f}\t\t\tDummy: {dum_accuracy:.2f}\t{ht(accuracy, dum_accuracy)}")
    print(f"Balanced accuracy: {bal_accuracy:.2f}\t\tDummy: {dum_bal_accuracy:.2f}\t{ht(bal_accuracy, dum_bal_accuracy)}")
    print(f"F1 score: {f1:.2f}\t\t\tDummy: {dum_f1:.2f}\t{ht(f1, dum_f1)}")
    print(f"ROC AUC: {auc:.2f}\t\t\tDummy: {dum_auc:.2f}\t{ht(auc, dum_auc)}")

    if give_roc:
        fpr, tpr = fpr_tpr(classifier, X_train, X_test, y_train, y_test)
        dum_fpr, dum_tpr = fpr_tpr(dum, X_train, X_test, y_train, y_test)

        output['tpr'] = tpr
        output['fpr'] = fpr
        output['dum_tpr'] = dum_tpr
        output['dum_fpr'] = dum_fpr

    if give_importance:
        importances = permutate(classifier, X_train, y_train)
        output['importances_mean'] = importances.importances_mean
        output['importances_std'] = importances.importances_std
    
    print("\nOutput keys:")
    for i in output.keys():
        print(i)
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
    


    
