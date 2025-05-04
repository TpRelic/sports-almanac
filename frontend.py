import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from nba_api.live.nba.endpoints import playbyplay, boxscore

def analyze_scoring_play(action):
    """Analyzes if a play resulted in points and how many."""
    desc = action.get('actionType', '').lower()
    shot_result = action.get('shotResult', '').lower()
    
    if shot_result != 'made':
        return 0
    
    if '3pt' in desc:
        return 3
    elif '2pt' in desc:
        return 2
    elif 'free throw' in desc:
        return 1
    return 0

def format_play(action, name, team_code):
    """Formats a play into a readable string with emojis."""
    action_type = action.get('actionType', '')
    shot_result = action.get('shotResult', '')
    
    emoji = "🏀" if shot_result == "Made" else "❌" if shot_result == "Missed" else "🔸"
    return f"{emoji} **{action.get('actionNumber')}** | Q{action.get('period')} {action.get('clock')} — {name} ({team_code}): *{action_type}*"

# Page setup
st.set_page_config(page_title="NBA Live Play‑by‑Play", layout="wide")
st.title("🏀 NBA Live Play‑by‑Play Animation")

# Sidebar controls
st.sidebar.header("Game Configuration")
game_id = st.sidebar.text_input("Game ID", value="0022000196")
animate = st.sidebar.button("Start Animation")
speed = st.sidebar.slider("Animation Speed (seconds)", 0.1, 2.0, 0.8)

if animate:
    try:
        # Fetch game data
        bs = boxscore.BoxScore(game_id)
        data = bs.get_dict().get('game', {})
        
        # Team information
        away_info = data.get('awayTeam', {})
        home_info = data.get('homeTeam', {})
        away_code = away_info.get('teamTricode')
        home_code = home_info.get('teamTricode')
        away_name = away_info.get('teamName')
        home_name = home_info.get('teamName')
        
        # Player rosters
        away_players = away_info.get('players', [])
        home_players = home_info.get('players', [])
        
        # Create player-team mapping
        player_team_map = {
            str(p.get('personId')): away_code for p in away_players
        }
        player_team_map.update({
            str(p.get('personId')): home_code for p in home_players
        })
        
        # Display rosters in sidebar
        st.sidebar.markdown(f"### {away_name} ({away_code})")
        away_roster = pd.DataFrame([
            {'Player': p.get('name', 'Unknown'), 'Number': p.get('jerseyNum', '')}
            for p in away_players
        ])
        st.sidebar.dataframe(away_roster.set_index('Player'))
        
        st.sidebar.markdown(f"### {home_name} ({home_code})")
        home_roster = pd.DataFrame([
            {'Player': p.get('name', 'Unknown'), 'Number': p.get('jerseyNum', '')}
            for p in home_players
        ])
        st.sidebar.dataframe(home_roster.set_index('Player'))
        
        # Setup display areas
        play_col, score_col = st.columns([3, 1])
        play_area = play_col.empty()
        score_area = score_col.empty()
        debug_area = st.empty()
        
        # Initialize scores
        scores = {away_code: 0, home_code: 0}
        
        # Fetch and animate plays
        pbp = playbyplay.PlayByPlay(game_id)
        plays = pbp.get_dict().get('game', {}).get('actions', [])
        
        for play in plays:
            # Get player info
            pid = str(play.get('personId', ''))
            team = player_team_map.get(pid, '')
            name = next(
                (p.get('name', 'Unknown') 
                 for p in (away_players + home_players) 
                 if str(p.get('personId', '')) == pid),
                'Unknown'
            )
            
            # Display the play
            play_line = format_play(play, name, team)
            play_area.markdown(play_line)
            
            # Update score
            points = analyze_scoring_play(play)
            if points > 0 and team in scores:
                scores[team] += points
                
                # Debug scoring
                debug_area.text(
                    f"Score Update: {team} +{points} ({name})"
                )
            
            fig = go.Figure()

            # Add team scores as vertical bars
            fig.add_trace(go.Bar(
                x=[away_name],
                y=[scores[away_code]],
                name=away_code,
                marker_color='#FF4B4B',
                width=0.4,
                text=scores[away_code],
                textposition='outside'
            ))

            fig.add_trace(go.Bar(
                x=[home_name],
                y=[scores[home_code]],
                name=home_code,
                marker_color='#1F77B4',
                width=0.4,
                text=scores[home_code],
                textposition='outside'
            ))

            # Add basketball decoration
            for score, team in zip([scores[away_code], scores[home_code]], [away_name, home_name]):
                fig.add_trace(go.Scatter(
                    x=[team],
                    y=[score + 2],
                    mode='text',
                    text='🏀',
                    textfont=dict(size=24),
                    showlegend=False
                ))

            # Update layout with basketball theme
            fig.update_layout(
                title=dict(
                    text="Live Score Tracker 🏀",
                    y=0.95,
                    x=0.5,
                    xanchor='center',
                    yanchor='top',
                    font=dict(size=24)
                ),
                yaxis=dict(
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=20,
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    title="Points"
                ),
                xaxis=dict(
                    title="Teams"
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                height=400,
            )

            # Add quarter lines
            for i in range(20, 100, 20):
                fig.add_hline(
                    y=i,
                    line_dash="dot",
                    line_color="gray",
                    opacity=0.3
                )

            # Create a unique key for the chart
            unique_key = f"score_chart_{play.get('actionNumber')}_{play.get('period')}_{play.get('clock').replace(':', '')}_{int(time.time()*1000)}"

            # Display the plot with the unique key
            score_area.plotly_chart(
                fig, 
                use_container_width=True,
                key=unique_key
            )

            # Display current quarter and time
            score_area.markdown(f"""
                <div style='text-align: center; background-color: rgba(0,0,0,0.1); padding: 10px; border-radius: 5px;'>
                    <h3>Q{play.get('period')} | {play.get('clock')}</h3>
                    <p>{away_code} {scores[away_code]} - {scores[home_code]} {home_code}</p>
                </div>
            """, unsafe_allow_html=True)

            time.sleep(speed)
        
        st.success("🎉 Game Replay Complete!")
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()