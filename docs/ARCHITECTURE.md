# Football Analysis - Architecture

## System Overview

The Football Analysis system is a modular computer vision pipeline that processes football match videos to extract player movements, team dynamics, and ball possession statistics.

## Architecture Diagram

```
┌─────────────────┐
│  Video Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Object Detection (YOLO)         │
│  - Players, Ball, Referees          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Object Tracking (ByteTrack)       │
│  - Maintain consistent IDs          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Ball Interpolation              │
│  - Fill missing detections          │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Position & Statistics Calculation  │
│  - Extract foot positions           │
│  - Calculate distances & speeds     │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Ball Possession Assignment      │
│  - Find closest player to ball      │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Team Assignment (K-means)       │
│  - Cluster by jersey colors         │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Team Ball Control Stats         │
│  - Track possession per frame       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│     Visualization & Rendering       │
│  - Draw annotations on frames       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Video Output   │
└─────────────────┘
```

## Core Components

### 1. Tracker (`trackers/tracker.py`)

**Responsibilities:**
- YOLO-based object detection
- ByteTrack-based object tracking
- Ball position interpolation
- Player position tracking
- Statistics calculation (distance, speed)
- Visualization rendering

**Key Methods:**
- `detect_frames()`: Batch object detection
- `get_object_tracks()`: Track objects across frames
- `add_position_to_tracks()`: Extract player positions
- `calculate_player_statistics()`: Compute distance & speed
- `interpolate_ball_positions()`: Fill missing ball detections
- `draw_annotations()`: Render visualizations

### 2. Team Assigner (`team_assigner/team_assigner.py`)

**Responsibilities:**
- Extract jersey colors from player bounding boxes
- Use K-means clustering to identify two teams
- Assign team colors for visualization

**Algorithm:**
- Extract top-half of player bbox (jersey area)
- Apply K-means (k=2) on color histograms
- Assign each player to nearest cluster

### 3. Player-Ball Assigner (`player_ball_assigner/player_ball_assigner.py`)

**Responsibilities:**
- Determine which player has ball possession
- Calculate nearest player to ball position

**Algorithm:**
- For each frame, compute distance from each player to ball
- Assign possession to closest player within threshold

### 4. Utils (`utils/`)

**video_utils.py:**
- `read_video()`: Load video into frame array
- `save_video()`: Write frames to video file

**bbox_utils.py:**
- `get_center_of_bbox()`: Calculate bbox center
- `get_bbox_width()`: Get bbox width
- `measure_distance()`: Euclidean distance between points

## Data Flow

### Track Data Structure

```python
tracks = {
    "players": [
        {  # Frame 0
            1: {  # Player ID 1
                "bbox": [x1, y1, x2, y2],
                "position": (x_center, y_bottom),
                "total_distance": 125.3,
                "speed": 18.5,
                "team": 1,
                "team_color": (255, 0, 0),
                "has_ball": False
            },
            2: { ... },  # Player ID 2
        },
        { ... },  # Frame 1
    ],
    "ball": [
        { 1: {"bbox": [x1, y1, x2, y2]} },  # Frame 0
        { 1: {"bbox": [x1, y1, x2, y2]} },  # Frame 1
    ],
    "referees": [
        { 1: {"bbox": [x1, y1, x2, y2]} },  # Frame 0
    ]
}
```

## Key Algorithms

### Distance Calculation

1. Extract player foot position (bottom center of bbox)
2. Calculate pixel distance moved between frames
3. Convert to meters: `distance_m = pixel_distance × pixel_to_meter`
4. Accumulate across frames

### Speed Calculation

1. Distance moved in current frame
2. Time delta: `Δt = 1/fps`
3. Speed: `v = distance/Δt × 3.6` (km/h)
4. Apply 5-frame moving average for smoothing

### Ball Interpolation

Uses pandas interpolation to fill missing ball detections:
- Linear interpolation for intermediate frames
- Backfill for missing initial frames

## Performance Optimizations

1. **Batch Processing**: Process frames in batches of 20
2. **Stub Caching**: Cache tracking results to pickle file
3. **Lazy Loading**: Only load what's needed
4. **Vectorized Operations**: Use NumPy for calculations

## Dependencies

- **YOLO (Ultralytics)**: Object detection backbone
- **ByteTrack (Supervision)**: Multi-object tracking
- **OpenCV**: Video I/O and visualization
- **scikit-learn**: K-means clustering
- **pandas**: Time-series interpolation
- **NumPy**: Numerical operations
