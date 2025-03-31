# Condition Monitoring of Pneumatic Drive Systems Based on the AI Method Feed-forward Backpropagation Neural Network
- Monica Tiboni & Carlo Remino

### Abstract
- Signal: Using pressure sensors on both chamber and acceleration signal (PSD and time-domain statistical indices)
- Test bench: show reliability of NN, prove model works even with low-cost instrumentation
- (Authors comparing literally everything)

### Intro
- Condition-based maintenace: diagnostic teniques, not only to minimize failures but also reduce planned maintenance, extend component life
- "Several publications explored the ability of NN to dectect and classify faults in pneumatic elements"
- Neural networks as models and classifiers
    - First net trained to predict correct output of valve
    - Second compared energy of signal to detect deviation
- K and S: 9 Features + dynamic error band - identified incorrect supply pressure, diaphragm leakage, and vent blockage faults <paper 25>
- Authors solved the same, S and K detect 19 faults by reducing size of input with PCA then compare to an ANFIS <paper 27>
- Benchmark of valve actuator DAMADICS identifies 19 faults, also evaluate NNs
- Kourd follow Freitas but errors base on Euclidian distance <paper 31>
- Deng follow K and S <paper 32>
- Prabakaran make initial system follow Kourd but second based on a self-organizing map adapt real-time observed <paper 35>
- K and K confirm PCA improves accuracy of clasifier <paper 36>
- Andrade: NARX predicts normal behavior and compare. Other NN classify the fault type. A decision tree makes the final decision <paper 37>
- Demetgul: use NN to detect faults in entire system. Compared results of two different trained NN (unsupervised ART2 and supervised, both good)
- Several authors suggested: closest neighbor interpolation, SMOTE, GANs, random oversampling and others    
- FEM, WPT, SVM,...
- In this, paper use PSD, FFT and statistics and aim for the statistics set that robust enough

### Methodology
1. Methodology description
- Figures decribe pretty good. Main points:
    - Reproduce faults
    - Data and features selections (dimensions reduce)
    - Neural net architecture (layers, neurons, transfer functions, data distribution)
    - Early-stopping (for generalization)
- This approach is experimental-based
2. Experimental Setup
3. Experimental Description
4. Feature Extraction and Dataset Analysis
- PSD and FFT most commonly used, research choose PSD
5. Statistical Analysis
- RMS, skewness and kurtosis considered. Peak and crest depend on sampling frequency which may not true if frequency is low
6. Adopted AI-Based Classifier

### Results
- Bro comparing everything, then make heatmap/graph...