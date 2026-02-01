# Usage Examples

This directory contains examples demonstrating different use cases of the Football Analysis system.

## Basic Usage

### Example 1: Process a Single Video

```python
from team_assigner.team_assigner import TeamAssigner
from utils.video_utils import read_video, save_video
from trackers.tracker import Tracker
from player_ball_assigner.player_ball_assigner import PlayerBallAssigner
import numpy as np
import os

# Read video
video_frames = read_video('input_videos/my_match.mp4')

# Initialize tracker
tracker = Tracker('models/best.pt')

# Get object tracks
tracks = tracker.get_object_tracks(
    video_frames,
    read_from_stub=False,  # Process from scratch
    stub_path='stubs/my_match_tracks.pkl'
)

# Add statistics
tracks = tracker.add_position_to_tracks(tracks)
tracks = tracker.calculate_player_statistics(
    tracks, 
    fps=30.0,  # Your video's FPS
    pixel_to_meter=0.12
)

# Process ball
tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

# Assign teams and ball possession
team_assigner = TeamAssigner()
team_assigner.assign_team_color(video_frames[0], tracks['players'][0])

player_assigner = PlayerBallAssigner()

for frame_num, player_track in enumerate(tracks['players']):
    ball_bbox = tracks['ball'][frame_num][1]['bbox']
    assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)
    
    if assigned_player != -1:
        tracks['players'][frame_num][assigned_player]['has_ball'] = True
    
    for player_id, track in player_track.items():
        team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
        tracks['players'][frame_num][player_id]['team'] = team
        tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

# Calculate team ball control
team_ball_control = []
for frame_num, player_track in enumerate(tracks['players']):
    ball_possession_team = 0
    for player_id, track in player_track.items():
        if track.get('has_ball', False):
            ball_possession_team = track['team']
            break
    team_ball_control.append(ball_possession_team)
team_ball_control = np.array(team_ball_control)

# Draw annotations
output_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

# Save output
save_video(output_frames, 'output_videos/my_match_analyzed.avi')
```

## Advanced Examples

### Example 2: Custom Calibration

```python
# Measure a known distance in your video (e.g., penalty box width = 16.5m)
known_distance_meters = 16.5
measured_pixels = 165

# Calculate calibration factor
pixel_to_meter = known_distance_meters / measured_pixels

# Use in statistics calculation
tracks = tracker.calculate_player_statistics(
    tracks,
    fps=24.0,
    pixel_to_meter=pixel_to_meter
)
```

### Example 3: Extract Player Statistics

```python
# After processing, extract stats for a specific player
player_id = 5
frame_num = 100

player_data = tracks['players'][frame_num][player_id]

print(f"Player {player_id} at frame {frame_num}:")
print(f"  Position: {player_data['position']}")
print(f"  Total Distance: {player_data['total_distance']:.2f}m")
print(f"  Current Speed: {player_data['speed']:.2f} km/h")
print(f"  Team: {player_data['team']}")
print(f"  Has Ball: {player_data.get('has_ball', False)}")
```

### Example 4: Batch Processing Multiple Videos

```python
import glob

video_files = glob.glob('input_videos/*.mp4')

for video_path in video_files:
    print(f"Processing {video_path}...")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    video_frames = read_video(video_path)
    
    # ... (same processing as above)
    
    output_path = f'output_videos/{video_name}_analyzed.avi'
    save_video(output_frames, output_path)
    
    print(f"Saved to {output_path}")
```

### Example 5: Export Statistics to CSV

```python
import csv

# Extract all player statistics
stats_data = []

for frame_num, player_dict in enumerate(tracks['players']):
    for player_id, track in player_dict.items():
        stats_data.append({
            'frame': frame_num,
            'player_id': player_id,
            'distance': track.get('total_distance', 0),
            'speed': track.get('speed', 0),
            'team': track.get('team', 0),
            'has_ball': track.get('has_ball', False)
        })

# Write to CSV
with open('player_statistics.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['frame', 'player_id', 'distance', 'speed', 'team', 'has_ball'])
    writer.writeheader()
    writer.writerows(stats_data)

print("Statistics exported to player_statistics.csv")
```

## Tips

- **Cache tracking results** with stubs for faster reprocessing
- **Calibrate pixel_to_meter** for accurate distance/speed
- **Adjust FPS** to match your video's actual frame rate
- **Use batch processing** for multiple videos
- **Export data** for further analysis in tools like Excel or Python
