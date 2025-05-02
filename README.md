# MPS04

## Data
### Data type
- raw: raw data
- cyc: invidual cycle
### Workpiece
- b: black, drop on slider
- w: white, drop on conveyor (longer)
### Error
- E1: vertical axis vibration
- E2: horizontal axis vibration

## Model
### Model type
### Train iterations

## Test
### 0. Visualize sensor signals
### 1. Collect data
- Collect to CSV file
### 2. Visualize data
### 3. Split data -> cycle
- Start (grip): 0.15
- Stop (drop): 0.03
- Length: black ~480k, white ~590k
### 4. Visualize cycle
### 5. Extract and visualize features
- PSD: Downsample, Remove DC offset, clip shock -> extract
- Skewness-Kurtosis: Downsample, Remove DC offset, remove shock -> extract
