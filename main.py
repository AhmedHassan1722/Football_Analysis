from team_assigner.team_assigner import TeamAssigner
from utils.video_utils import read_video, save_video
from trackers.tracker import Tracker
from player_ball_assigner.player_ball_assigner import PlayerBallAssigner
import os
import numpy as np 

def main():
    # Read Video
    video_frames = read_video('D:\\Nti_football_analysis\\input_videos\\WhatsApp Video 2025-12-14 at 09.56.24_7c2d2ca1.mp4')    # \\ or / or r"\"

    trackers = Tracker('D:\\Nti_football_analysis\\models\\best.pt')
    os.makedirs('stubs', exist_ok=True)
    tracks = trackers.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path='stubs/track_stubs.pkl')


    # Interpolate Ball Positions
    tracks["ball"] = trackers.interpolate_ball_positions(tracks["ball"])

    # Add position tracking and calculate player statistics
    tracks = trackers.add_position_to_tracks(tracks)
    tracks = trackers.calculate_player_statistics(tracks, fps=24.0, pixel_to_meter=0.1)

    # Assign Ball Aquisition
    player_assigner =PlayerBallAssigner()

    # Loop over all the frames to to get the assigned player in each frame
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:     
            tracks['players'][frame_num][assigned_player]['has_ball'] = True

    # Assign Player Teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0],      # first frame image
                                    tracks['players'][0]) # first frame tracking
    
    
    # loop over all the frames   
    for frame_num, player_track in enumerate(tracks['players']):
        # loop over the team member to assign a color of each one
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num],   #current frame image
                                                 track['bbox'],             # the bbox of the player
                                                 player_id)
            tracks['players'][frame_num][player_id]['team'] = team 
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

    # Calculate Team Ball Control
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_possession_team = 0  # 0 means no team has the ball
        for player_id, track in player_track.items():
            if track.get('has_ball', False):
                ball_possession_team = track['team']
                break
        team_ball_control.append(ball_possession_team)
    team_ball_control = np.array(team_ball_control)

    video_frames = trackers.draw_annotations(video_frames, tracks, team_ball_control)

    os.makedirs('output_videos', exist_ok=True)
    # Save video
    save_video(video_frames, 'output_videos/output_video.avi')

main()