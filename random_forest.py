import pandas as pd
import numpy as np
import ast
import random
from sklearn.ensemble import RandomForestClassifier

def determine_features(path):
    results = pd.read_csv(path, sep = ";", names = ["Image", "Intervals0", "Intervals1", "Intervals2", "Number0", "Number1", "Number2"])
    length = len(results)
    for dim in [0,1,2]:
        intervals, number, longest, birth_longest, sec_longest, birth_sec_longest = "Intervals"+str(dim), "Number"+str(dim), "Longest"+str(dim), "Birth Longest"+str(dim), "Second Longest"+str(dim), "Birth Second Longest"+str(dim)
        results[intervals] = [ast.literal_eval(results[intervals][i]) for i in range(length)]
        results[number] = [len(results[intervals][i]) for i in range(length)]
        births = [np.array([ast.literal_eval(results[intervals][i][j].replace(")", "]").replace("infinity", "1000"))[0] for j in range(results[number][i])]) for i in range(length)]
        deaths = [np.array([ast.literal_eval(results[intervals][i][j].replace(")", "]").replace("infinity", "1000"))[1] for j in range(results[number][i])]) for i in range(length)]
        lifespans = np.array(deaths) - np.array(births)
        list_longest, list_birth_longest, list_sec_longest, list_birth_sec_longest = [], [], [], []
        for i in range(length):
            lifespan = list(lifespans[i])
            if len(lifespan)==0:
                list_longest.append(0)
                list_birth_longest.append(0)
            else:
                list_longest.append(max(lifespan))
                list_birth_longest.append(births[i][np.argmax(lifespan)])
                lifespan.remove(max(lifespan))
            if len(lifespan)==0:
                list_sec_longest.append(0)
                list_birth_sec_longest.append(0)
            else:
                list_sec_longest.append(max(lifespan))
                list_birth_sec_longest.append(births[i][np.argmax(lifespan)])
        results[longest], results[birth_longest], results[sec_longest], results[birth_sec_longest] = list_longest, list_birth_longest, list_sec_longest, list_birth_sec_longest
    return results

def over_under_sample_data_train(data, size_data):
    data_morphs = data.loc[data["Morph"] == 1]
    data_originals = data.loc[data["Morph"] == 0]
    data_morphs_undersample = data_morphs.head(round(size_data/2))
    data_originals_oversample = data_originals.copy()
    for _ in range(round(size_data/2 / len(data_originals))-1):
        data_originals_oversample = data_originals_oversample.append(data_originals)
    return data_morphs_undersample.append(data_originals_oversample)

def under_sample_data_test(data):
    data_morphs = data.loc[data["Morph"] == 1]
    data_originals = data.loc[data["Morph"] == 0] 
    number_morphs = round(len(data_originals)/4) # let us assume that 80% are originals, 20% morphs
    return data_originals.append(data_morphs.sample(frac=1).reset_index(drop=True).head(number_morphs))

def calc_score(data_train, data_test, size_data_train):
    data_train = over_under_sample_data_train(data_train, size_data_train)
    data_test = under_sample_data_test(data_test)
    X_train, y_train = data_train[["Number0", "Number1", "Number2","Longest1", "Longest2", "Birth Longest1", "Birth Longest2", "Second Longest0", "Birth Second Longest0"]], data_train["Morph"] 
    X_test, y_test = data_test[["Number0", "Number1", "Number2","Longest1", "Longest2", "Birth Longest1", "Birth Longest2", "Second Longest0", "Birth Second Longest0"]], data_test["Morph"]
    clf = RandomForestClassifier(max_depth=4, random_state=0).fit(X_train, y_train)
    # print(clf.feature_importances_)
    y_pred_proba = clf.predict_proba(X_test)
    number_morphs = sum(y_test)
    indeces = pd.DataFrame([proba[1] for proba in y_pred_proba]).sort_values(by=[0], ascending=False).head(number_morphs).index
    y_pred = np.zeros(len(data_test))
    for i in indeces:
        y_pred[i] = 1
    # compare to random assignment of number_morphs images as morphs
    indeces_random = random.sample(range(len(data_test)), number_morphs)
    y_pred_random = np.zeros(len(data_test))
    for i in indeces_random:
        y_pred_random[i] = 1

    return sum(np.array(y_pred)*np.array(y_test)) / number_morphs, sum(np.array(y_pred_random)*np.array(y_test)) / number_morphs

def cross_fold(data, number_folds, size_data_train):
    length_fold = round(len(data)/number_folds)
    folds = np.split(data, [i*length_fold for i in range(1, number_folds)], axis = 0)
    prec, prec_random = 0, 0
    for i in range(number_folds):
        data_test = folds[i]
        data_train = pd.DataFrame()
        for j in range(number_folds):
            if j != i:
                data_train = data_train.append(folds[j])
        prec_i, prec_random_i = calc_score(data_train, data_test, size_data_train)
        prec, prec_random = prec + prec_i, prec_random + prec_random_i
    return prec / number_folds, prec_random / number_folds

def random_forest(path_morphs, path_originals):
    results_morphs = determine_features(path_morphs)
    results_originals = determine_features(path_originals)
    results_morphs["Morph"] = 1
    results_originals["Morph"] = 0
    results = results_morphs.append(results_originals).reset_index(drop=True).drop_duplicates("Image")
    results = results.sample(frac=1).reset_index(drop=True)
    prec, prec_random = cross_fold(results, 5, 200)
    print("The trained classifier predicts ", prec*100, "% of the morphed images correctly as morphs.")
    print("A random choice predicts ", prec_random*100, "% of the morphed images correctly as morphs.")
    return prec, prec_random