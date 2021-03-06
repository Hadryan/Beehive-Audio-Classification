from __future__ import print_function
import os
import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt

from skrebate import ReliefF

base_dir_train = '/home/chelsi/BUZZ2/train/'
sub_dir_train = ['bee_train', 'noise_train', 'cricket_train']


def read_features():
    D_train = []
    L_train = []

    for label, class_names in enumerate(sub_dir_train, start = 0):
        mvector_fft_path = os.path.join(base_dir_train, class_names, "pyaudio_features", "*.mvector.npy")
        all_files = glob.glob(mvector_fft_path)
        for f in all_files:
            value = np.load(f)
            D_train.append(value[:])
            L_train.append(label)

    return np.array(D_train), np.array(L_train)


X_train, Y_train = read_features()

fs = ReliefF(n_jobs = -1)
fs.fit(X_train, Y_train)
feature_scores = fs.feature_importances_

print ('The indices of best features are: ', fs.top_features_, '\n')
print ('The scores of features are: ', feature_scores, '\n')

#Plotting the feature importances
X = list(range(34))
Y = feature_scores
plt.xlabel("Feature Index")
plt.ylabel("Feature Score")
plt.xticks(np.arange(0,34,2))
plt.plot(X, Y)
plt.savefig('ReliefF_feature_importances.png')
