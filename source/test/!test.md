# Testing phases

### Phase 0: Visualize live signal
- There're vibrations and acceleration signals in the raw data
=> Use acceleration signals to split data

### Phase 1: Collect data
- Update to MySQL resulting overflow
=> Data collected using .csv instead

### Phase 2: Visualize data
- Acceleration created significatnly large strokes of amplitude
=> Split cycle using last 0.2 signal and first 0.05 signal
- Vibration amplitude under a threshold but not stable (Larger for vibrate data)
=> Remove idle states 