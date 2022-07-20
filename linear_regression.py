"""
Reads data and does linear regression on it

Open the presentation in the files for more explanations
"""

import numpy as np
import pandas as pd

from constants import *

# CONSTANTS
ERRORAVG_TXT = "erroravg4.txt"
RESULTS_CSV = "Results4.csv"
PRO_SUB_CSV = "pro_sub.csv"
ANTI_SUB_CSV = "anti_sub.csv"
OUTPUT = "good3.csv"
ROW = 0
COL = 1
NUM_OF_TESTS = 100


def fit_linear_regression(des_mat, resp_vec):
    """
    The function returns two sets of values: the first is a numpy array of the coefcient vector `w`
    and the second is a numpy array of the singular values of X.
    :param des_mat: Design matrix - numpy array with p rows and n columns
    :param resp_vec: Response vector - numpy array
    :return:
    """
    des_mat_deg_t, sigma = get_des_mat_deg_t(des_mat)
    w = np.dot(des_mat_deg_t, resp_vec)
    return w


def get_des_mat_deg_t(des_mat):
    """
    returns the design matrix transpose dagger and the singular values of the design matrix.
    :param des_mat: The design matrix
    :return:  (design matrix transpose dagger, singular values of the design matrix)
    """
    u, sigma, v_t = np.linalg.svd(des_mat, full_matrices=False)
    sigma_dag = np.diag(1 / sigma)
    des_max_deg_t = np.dot(u, np.dot(sigma_dag, v_t))
    return des_max_deg_t, sigma


def predict(des_mat, coef_vec, respond_vector):
    """
    Predicts the value of y with the coef values of the design matrix
    :param respond_vector:
    :param des_mat: Design Matrix
    :param coef_vec: The coefficient vector w
    :return:
    """
    y_ans = np.dot(des_mat.T, coef_vec)
    y_ans = (y_ans - np.min(y_ans)) / np.ptp(y_ans)
    categorize = np.where(y_ans >= 0.5, 1, 0)
    false_positive = [1 for i in range(categorize.size) if (categorize[i] == 1 and respond_vector[i] == 0)]
    false_negative = [1 for i in range(categorize.size) if (categorize[i] == 0 and respond_vector[i] == 1)]
    false_positive = int(np.sum(false_positive))
    false_negative = int(np.sum(false_negative))
    return y_ans, false_positive, false_negative


def load_data(anti_path, skep_path):
    """
    Loads a cvs files and returns a numpy matrix
    :return: np array representing the data and the feature names
    """
    gull = read_data(anti_path, True)
    pro = read_data(skep_path, False)
    data = gull.append(pro)
    data.fillna(0, inplace=True)
    data.astype(np.int64)
    data.drop(SUB_SKEPT + SUBS_GULL, axis=1, inplace=True, errors="ignores")
    data.to_csv(OUTPUT)
    data.insert(0, "bias", [1] * data.shape[0])
    return np.array(data).astype(np.int64).T, np.array(data.drop(G_O_METER, axis=1)).astype(np.int64).T, np.array(
        data[G_O_METER].astype(np.int64))


def choose_set(des_mat):
    """
    Chooses a train set and a test set.
    :param des_mat: Design matrix
    :return: design matrix and a test matrix
    """
    num_of_samples = des_mat.shape[COL]
    test_data_size = int(num_of_samples / 4)
    train_data_size = num_of_samples - test_data_size
    train_choices = np.random.choice(num_of_samples, train_data_size, replace=False)
    test_choices = np.setdiff1d(np.arange(num_of_samples), train_choices)
    return des_mat[:, train_choices], des_mat[:, test_choices]


def train_cycle(des_mat, mean_fit):
    """
    Linear regression train cycle
    """
    train_set, test_set = choose_set(des_mat)
    resp_train, resp_test = train_set[1], test_set[1]
    train_set, test_set = np.delete(train_set, 1, 0), np.delete(test_set, 1, 0)
    fitted_vectors = fit_linear_regression(train_set, resp_train)
    mean_fit += fitted_vectors
    return mean_fit


def write_results_to_csv(feat_mean, false_pos, false_neg):
    """
    rites the results to a final csv
    """
    data = pd.read_csv(OUTPUT, index_col=0)
    feat_mean = feat_mean[1:]
    relevant = list(data[data.columns[1:]])
    a = dict()
    for i in range(len(relevant)):
        a[relevant[i]] = feat_mean[i]
    results = pd.DataFrame(list(a.values()), index=list(a.keys()))
    results.to_csv(RESULTS_CSV)
    with open(ERRORAVG_TXT, "w+") as error_file:
        error_file.write("False Positive = " + str(false_pos) + "\nFalse negative = " + str(false_neg))


def main():
    """
    Main learning algorithm,
    """
    design_matrix, test_des_matrix, vect_test = load_data(ANTI_SUB_CSV, PRO_SUB_CSV)
    fitted_mean = np.zeros(design_matrix.shape[0] - 1)
    for j in range(NUM_OF_TESTS + 1):
        fitted_mean = train_cycle(design_matrix, fitted_mean)
    fitted_mean /= NUM_OF_TESTS
    y, false_pos, false_neg = predict(test_des_matrix, fitted_mean, vect_test)
    write_results_to_csv(fitted_mean, false_pos, false_neg)


def read_data(path, gull):
    """
    Reads the dataset csv and returns an arranged numpy matrix with the 20 most subscribed subreddits.
    :param gull: True for the gullible dataset false otherwise
    :param path: path of the dataset
    :return: an arranged numpy matrix with the 20 most subscribed subreddits
    """
    data = pd.read_csv(path, index_col=0)
    g_o_meter = 1 if gull == 1 else 0
    num_of_sub = data.sum(axis=0)
    lowest_sub = data.columns[np.where(num_of_sub < 20)]
    data.drop(lowest_sub, axis=1, inplace=True)
    data.insert(0, G_O_METER, [g_o_meter] * data.shape[0])
    data = data.astype(np.int64)
    return data
