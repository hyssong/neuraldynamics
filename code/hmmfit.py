# # # import libraries
import numpy as np
import scipy.io
from sklearn.cluster import KMeans
from hmmlearn import hmm
import os
import random
import timeit
import pickle
from datetime import datetime
from scipy import stats

# # # parameters
nstate=4
nsubj=27
condition=['rest1','rest2','gradCPTface','gradCPTscene','sitcomep1','sitcomep2','documentary']
print('numState=' + str(nstate))
random.seed(datetime.now())
loaddir = '../fmri'
savedir = '../fmri'

# # # Load fMRI time series and concatenate
# Load time series extracted from preprocessed EPI file
# 25 ROI: 17 cortical networks (Yeo et al., 2011) and 8 subcortical regions (Tian et al., 2020)
data={'rest1':scipy.io.loadmat(loaddir+'/ts_rest1.mat')['ts'],
      'rest2':scipy.io.loadmat(loaddir+'/ts_rest2.mat')['ts'],
      'gradCPTface':scipy.io.loadmat(loaddir+'/ts_gradCPTface.mat')['ts'],
      'gradCPTscene':scipy.io.loadmat(loaddir+'/ts_gradCPTscene.mat')['ts'],
      'sitcomep1':scipy.io.loadmat(loaddir+'/ts_sitcomep1.mat')['ts'],
      'sitcomep2':scipy.io.loadmat(loaddir+'/ts_sitcomep2.mat')['ts'],
      'documentary':scipy.io.loadmat(loaddir+'/ts_documentary.mat')['ts']}

# Concatenate z-normalized time series of all participants' all fMRI scan runs
concatts, subjid, epiid = [], [], []
for subj in range(nsubj):
    for ep, cdt in enumerate(condition):
        if subj==nsubj-2 and cdt=='sitcomep1': # one participant with missing fMRI scan run
            pass
        else:
            # z-normalize ROI time series
            if len(concatts)==0:
                concatts = stats.zscore(data[cdt][subj,:,:], axis=0, ddof=1)
                subjid = np.repeat(subj,stats.zscore(data[cdt][subj,:,:], axis=0, ddof=1).shape[0], 0)
                epiid = np.repeat(ep, stats.zscore(data[cdt][subj, :, :], axis=0, ddof=1).shape[0], 0)
            else:
                concatts = np.concatenate((concatts, stats.zscore(data[cdt][subj, :, :], axis=0, ddof=1)), 0)
                subjid = np.concatenate((subjid, np.repeat(subj, stats.zscore(data[cdt][subj, :, :], axis=0, ddof=1).shape[0], 0)), 0)
                epiid = np.concatenate((epiid, np.repeat(ep, stats.zscore(data[cdt][subj, :, :], axis=0, ddof=1).shape[0], 0)), 0)

print('nTime: '+str(concatts.shape[0]))
print('nRegion: '+str(concatts.shape[1]))
print('subj: '+str(np.unique(subjid)))
print('condition: '+str(np.unique(epiid)))

# # # Initialize with k-means clustering
start = timeit.default_timer()
print('Doing k-means clustering')
kmeans_train = KMeans(n_clusters=nstate, init='k-means++', n_init=50, max_iter=200, tol=0.001).fit(concatts)
stop = timeit.default_timer()
print('Time: ', stop - start)

# # # HMM fit
start = timeit.default_timer()
print('Fitting HMM')
hmmmodel = hmm.GaussianHMM(n_components=nstate, covariance_type='full', means_prior=kmeans_train.cluster_centers_, n_iter=1000, tol=0, init_params='m')
hmmmodel.fit(concatts)
print('HMM fitting finished at ' + str(hmmmodel.monitor_.iter) + ' iterations')
stop = timeit.default_timer()
print('Time: ', stop - start)

# # # Save HMM fit
print('Saving Data')
HMMMODEL = {'niter': hmmmodel.monitor_.iter,
            'nfeatures': hmmmodel.n_features,
            'transmat': hmmmodel.transmat_,
            'startprob': hmmmodel.startprob_,
            'Means': hmmmodel.means_,
            'Covars': hmmmodel.covars_}
scipy.io.savemat(savedir + '/hmmmodel.mat', HMMMODEL)
pickle.dump(hmmmodel, open(savedir + '/hmmfit.pkl', 'wb'))

# # # Save decoded latent state sequence
HMMOUTPUT = {'train_state': hmmmodel.decode(concatts)[1],
             'train_logprob': hmmmodel.decode(concatts)[0],
             'train_posterior': hmmmodel.predict_proba(concatts),
             'subjid':subjid,
             'epiid':epiid}
scipy.io.savemat(savedir + '/hmmdecode.mat', HMMOUTPUT)


