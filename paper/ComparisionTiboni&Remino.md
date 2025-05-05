# Review: Condition Monitoring of Pneumatic Drive Systems Based on the AI Method Feed-forward Backpropagation Neural Network
- Monica Tiboni & Carlo Remino

### Abstract
- Compares results obtained with different sensors and features as input
- Features: PSD and statistical indices (time-domain)
- Possible to condition monitoring, increase uptake of maintanance approach

### Introduction - Related Works
- Case study: </br>
<paper 24> De Freitas 2 Networks: model (predict) and classifier (compare signal) </br>
<paper 25 26> K S identified: incorrect pressure, diaphragm leakage, and vent blockage using 9 features. Feature valve respond to step command </br>
<paper 32> Deng follow K S (7 features from step response of valve) </br>
<paper 27 28 29> S K detected 19 faults, reduce input size using PCA and compare to ANFIS </br>
<paper 30> Benchmark of 19 faults. Control Valve, Servo, Positioner, General/External Faults </br>
<paper 31> Kourd follow Freitas but errors identified based on Euclidean distance </br>
<paper 33> S K reduce input with PCA </br>
<paper 34 35> Prabakaran initial system similar to Kourd, then improve with KSOM adapt real-time observed </br>
<paper 36> K K confirmed PCA in improving accuracy </br>
<paper 37> Andrade Networks: NARX to predict state and a classifier for each faults then identify with tree </br>
<paper 38> Demetgul NN to detect faults in entire system. Compared 2 method: supervised-unsupervised (11 faults from 8 signals from sensors) </br>
- Imbalance of dataset: closest neighbor interpolation, SMOTE, GANs, random oversampling and others. FEM, WPT, SVM,... </br>

### Methodology
- Identified feature of faults 
- Trained model using Welch's PSD
- Compare for best suited model structure and features

### Results, Conclusion
- "body" higher accuracy, but "rod" sensors with high PSD and sufficient neurons can achieve perfect classification
- Statistical features "body" monoaxial sensor high accurate and reliable fault detection, "rod" and Arduino are less effective
- Evaluating using weighted error rather than raw accuracy
- Monoaxial "body" using Z-axis signals with 150 Hz PSD and 80% data outperform Arduino sensors in classification errors
- Statistical features "body" make less critical errors, even with less training data