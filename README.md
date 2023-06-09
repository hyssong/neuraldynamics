# neuraldynamics

**Song, H., Shim, W. M., Rosenberg, M. D. (2022) Large-scale neural dynamics in a shared low-dimensional state space reflect cognitive and attentional dynamics.**

Raw functional MRI data of the **SitcOm, Nature documentary, Gradcpt (SONG)** dataset is available on OpenNeuro [https://openneuro.org/datasets/ds004592]. The associated behavioral data, processed fMRI output, and main analysis codes are published here. Processed data or analysis on datasets other than SONG are not published. For additional inquiries, please contact Hayoung Song (hyssong@uchicago.edu).

**1. behavior**: behavioral experiment data
  - sitcomep1, sitcomep2, documentary_beh.mat
    - raw continuous engagement ratings from a scale of 1 to 9
    - engagement ratings convolved with hemodynamic response function and z-normalized across time (used to relate with the fMRI latent state dynamics)
    - event index: event 1 and 2 interleaved in sequence
  - gradCPTface, gradCPTscene_beh.mat
    - response time variability (deviance from the mean)
    - response time variability convolved with hemodynamic response function and z-normalized across time (used to relate with the fMRI latent state dynamics)
  - traitscores.csv
    - subjID, sex (male/female), handedness (right/left), age
    - overall engagement ratings (oral report on a scale of 1 to 9) after movie watching scans
    - gradCPT performance: d-prime and mean of response time variability
    - working memory capacity (K) measured with a color working memory task (Zhang & Luck, 2008 *Nature*) using set size 6.
  - hcpparticipants.csv: a list of HCP participant IDs that were used in the study

**2. fmri**: fMRI analysis output
  - ts_*.mat: 25-parcel time series of the 7 runs of the SONG dataset (subj x time x parcel), used as inputs to the HMM.
  - hmmmodel.mat: model parameters estimated from the HMM fit using K=4
    - Means: mixture Gaussian emission probability, mean activity 
    - Covars: mixture Gaussian emission probability, covariance
    - transmat: transition probability (however, a transition probability matrix reported in the manuscript was separately calculated per participant’s fMRI scan)
    - nfeatures: number of input features
    - niter: number of model fitting iterations (maximum set to 1,000)
    - startprob: initial probability which was set as random 
  - hmmoutput.mat: HMM-decoded latent state sequence, summarized per fMRI condition and participant. Running code/hmmfit.py outputs hmmdecode.mat. hmmdecode.mat[‘train_state’] (a decoded discrete latent state sequence) was summarized with participant and condition indices and saved as hmmoutput.mat.
  - state1-4_raw.nii.gz: hmmmodel.mat[‘Means’] projected onto 25 parcels of the MNI152_T1_3mm_brain.nii.gz.

**3. code**: analysis code
  - hmmfit.py: runs HMM, i.e., infers model parameters from ts_*.mat and decodes latent state sequence
  - Jupyter notebooks that reproduce Figure 1 to 5
