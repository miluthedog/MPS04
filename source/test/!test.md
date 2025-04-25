# Testing phases

### Phase 0: Visualize live signal
- There're vibrations and acceleration signals in the raw data

### Phase 1: Collect data
- Update to MySQL resulting overflow, use .csv instead

### Phase 2: Visualize data
- Acceleration created significatnly large strokes of amplitude
- Vibration amplitude under a threshold but not stable (Larger for vibrate data)

### Phase 3: Collect cycle
- Cycle: Last > 0.15 peak and first 0.03 peak

### Phase 4: Evaluate cycle
- Plot cycles

### Phase 5: Preprocess
- Remove idle states
- Downsampling