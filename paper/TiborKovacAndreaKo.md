# Monitoring Pneumatic Actuators' Behavior Using Real-World Data Set
- Tibor Kovac Andrea Ko

### Abstract
- Signal preprocessing: Peak detection, garbage removal and down-sampling
- Grouping similar pattern: Wards hierarchical clustering with multivariate Euclidean distance calculation and Kohonen self-organizing map

- Visual display can be monitored
- Clustered signal can create a balance set for learning

### Related Works
- Smart manufaturing is trend
- Unstructed data sensed realtime need proprocessing
- Focus on phase: fault detection, identification and estimation in vibrating structures

- Sensor fault detection <paper 1 2> and AI dealt <paper 12 13>
- Data analysis: combination of wavelet transformation, feature extraction and classification with MLP-Artificial NN and support vector machine SVM

- Main steps: Signal acquisition, feature extraction and selection, and fault classification <paper 14 15>
    - Extract representative features: Time-domain statistical analysis, Fourier spectral analysis and wavelet transformation <paper 16>
    - Feature selection: k-nearest neighbor (kNN) negatively affect 
    - Dimension reduction stategies: principle components analysis PCA or distance evalution technique <paper 17>
    - Fault classification: Data unlabeled, unsupervised learning like clustering and suport vector machine SVM>

- Supervised learning fits well, Unsupervised learning goal is to discover unknown classes of items by clustering <paper 24>
- Imbalance class distribution: where significantly more intances from one class, lead to misclassify instances of less represented
- Class imbalance: algorithm adaptation, cost-sensitive learning (classifier) and data resampling (balancing data)
- Hybrid methods: unsupervised learning as data preprocessing for supervised learning

- Undersampling with k-nearest neighbors for data <paper 33>
- Clustering based under sampling (High accuracy) <paper 34>, Fast-CBUS improved computational cost <paper 30>

### Case study
- (Temperature-Vibration spectrum methods) Signal are non-stationary and Fourier spectrum may introduce false alarms/missed detections <paper 35>
- Pattern recognition: analyzing signals from pneumatic actuator realiable, cheap and able to detect wear tear (difficult)

- Signal 0-20mV collected, down-sampling from 7.8e-5 to 1.4e-2 by interpolation
- Signal both operating and idling, latter removed. Run 6-8 cycles
- External_conditions: Mainly compressed air pressure, affect cycle time and signal amplitude

- Cycle time set but not stable, vary 1%. Disturbances like jamming influence cycle time or cause sequence of cycles prematurely aborted
- Preprocessing: Find start of cycle to split cycles

- Clustering: Normalize and downsample, calculate distance matrix, cluster cycles hierarchical to a number
    - Euclidean distance to calculate dissimilarity matrix as input for clustering, 20000 signals per batch (based on computer)
    - Numbers of cluster (4) evaluated by experts
    - Clustering using fastcluster R package applying

- Assembled_clustering: stratified sampling to reduce and balance, calculate distance matrix, cluster cycles, observe timeline of states