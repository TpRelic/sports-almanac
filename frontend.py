import streamlit as st
import time
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from nba_api.live.nba.endpoints import playbyplay, boxscore
from plotly import subplots as sp
from collections import defaultdict
from get_nba_stats import GameFinder
from ask_ai import get_ai_response

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'game_finder' not in st.session_state:
    st.session_state.game_finder = GameFinder()
if 'current_play' not in st.session_state:
    st.session_state.current_play = None
if 'player_stats' not in st.session_state:
    st.session_state.player_stats = {}
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'current_play_index' not in st.session_state:
    st.session_state.current_play_index = 0
if 'plays' not in st.session_state:
    st.session_state.plays = []

def clear_chat():
    st.session_state.chat_history = []

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

def track_player_stats(play, stats_dict, name, team):
    """Track player statistics for each play."""
    if name not in stats_dict:
        stats_dict[name] = {
            'team': team,
            'name': name,
            'points': 0,
            'rebounds': 0,
            'assists': 0,
            'steals': 0,
            'blocks': 0
        }
    
    action = play.get('actionType', '').lower()
    result = play.get('shotResult', '').lower()
    
    if 'rebound' in action:
        stats_dict[name]['rebounds'] += 1
    elif 'steal' in action:
        stats_dict[name]['steals'] += 1
    elif 'block' in action:
        stats_dict[name]['blocks'] += 1
    elif 'assist' in action:
        stats_dict[name]['assists'] += 1
    elif result == 'made':
        if '3pt' in action:
            stats_dict[name]['points'] += 3
        elif '2pt' in action:
            stats_dict[name]['points'] += 2
        elif 'free throw' in action:
            stats_dict[name]['points'] += 1
            
    return stats_dict

def create_player_performance_charts(player_stats, away_code, home_code):
    """Create simplified player performance visualizations."""
    # Convert stats to DataFrame and sort by points
    stats_df = pd.DataFrame.from_dict(player_stats, orient='index')
    if stats_df.empty:
        return go.Figure()
    
    # Sort by points and add team color coding
    stats_df = stats_df.sort_values('points', ascending=False)
    stats_df['color'] = stats_df['team'].map({
        away_code: '#FF4B4B',
        home_code: '#1F77B4'
    })
    
    # Create subplot figure with adjusted dimensions
    fig = sp.make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            '<b>Points by Player</b>',
            '<b>Player Performance Heatmap</b>'
        ),
        column_widths=[0.5, 0.5],
        horizontal_spacing=0.15  # Increased spacing between subplots
    )
    
    # 1. Points by Player Bar Chart (Vertical)
    fig.add_trace(
        go.Bar(
            x=stats_df['name'],
            y=stats_df['points'],
            marker_color=stats_df['color'],
            text=stats_df['points'],
            textposition='outside',
            textfont=dict(size=12),
            hovertemplate="<b>%{x}</b><br>" +
                         "Points: %{y}<br>" +
                         "<extra></extra>"
        ),
        row=1, col=1
    )
    
    # 2. Player Activity Heatmap
    stats_for_heatmap = ['points', 'rebounds', 'steals', 'blocks']
    activity_matrix = stats_df[stats_for_heatmap].values
    
    fig.add_trace(
        go.Heatmap(
            z=activity_matrix,
            x=[stat.capitalize() for stat in stats_for_heatmap],
            y=stats_df['name'],
            colorscale='RdBu',
            showscale=True,
            text=activity_matrix.round(1),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(
                title='Value',
                thickness=15,
                len=0.9,
                x=1.02
            ),
            hovertemplate="<b>%{y}</b><br>" +
                         "%{x}: %{z}<br>" +
                         "<extra></extra>"
        ),
        row=1, col=2
    )
    
    # Update layout for better readability
    fig.update_layout(
        height=max(400, len(stats_df) * 30),
        showlegend=False,
        title_text="Player Statistics",
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=50, b=100)  # Increased bottom margin for player names
    )
    
    # Update axes for vertical bar chart
    fig.update_xaxes(
        title_text="",
        row=1, col=1,
        tickangle=45,  # Angle player names for better readability
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        title_text="Points Scored",
        row=1, col=1,
        gridcolor='rgba(128, 128, 128, 0.2)',
        title_font=dict(size=12),
        tickfont=dict(size=10),
        autorange=True  # Allow dynamic range based on max score
    )
    
    # Update heatmap axes
    fig.update_yaxes(
        title_text="",
        row=1, col=2,
        tickfont=dict(size=12),
        autorange="reversed"  # Keep player order consistent
    )
    
    return fig

# Page setup
st.set_page_config(page_title="NBA Live Play‑by‑Play", layout="wide")
st.title("🏀 NBA Live Play‑by‑Play Animation")

# Sidebar controls with Game Finder integration
st.sidebar.header("Game Configuration")

# Date selector
date = st.sidebar.date_input("Select Date", value=pd.to_datetime('2025-01-01'))
date_str = date.strftime('%Y-%m-%d')

# Get available games for selected date
games = st.session_state.game_finder.get_available_games(date_str)
if games:
    game_options = list(games.keys())
    selected_game = st.sidebar.selectbox("Select Game", options=game_options)
    game_id = f"00{games[selected_game]}" if selected_game else None
else:
    st.sidebar.error("No games found for selected date")
    game_id = None

# Animation controls
animate = st.sidebar.button("Start Animation")
speed = st.sidebar.slider("Animation Speed (seconds)", 0.05, 2.0, 0.05)

# Add chat interface in sidebar
chat_container = st.sidebar.container()
with chat_container:
    st.markdown("---")
    st.header("Game Analysis Chat")
    
    with st.form(key='chat_form', clear_on_submit=True):
        chat_input = st.text_input("Ask about the game:", 
                                  placeholder="e.g., Who scored the most points?")
        col1, col2 = st.columns([1,1])
        with col1:
            submit_chat = st.form_submit_button("Ask AI")
        with col2:
            clear_chat = st.form_submit_button("Clear", on_click=clear_chat)
        
        if submit_chat and chat_input:
            try:
                # Initialize variables
                play_history = []
                
                # Access data from session state
                plays = st.session_state.get('plays', [])
                player_team_map = st.session_state.get('player_team_map', {})
                away_players = st.session_state.get('away_players', [])
                home_players = st.session_state.get('home_players', [])
                player_stats = st.session_state.get('player_stats', {})
                play_line = st.session_state.get('current_play', "")
                
                # Create game context
                game_context = {
                    'game_id': game_id,
                    'scores': st.session_state.scores,
                    'current_play': play_line,
                    'player_stats': player_stats,
                    'play_by_play': []  # Initialize empty list for play history
                }
                
                # Add play-by-play history to context if available
                if plays:
                    for p in plays:
                        pid = str(p.get('personId', ''))
                        team = player_team_map.get(pid, '')
                        name = next(
                            (player.get('name', 'Unknown') 
                             for player in (away_players + home_players) 
                             if str(player.get('personId', '')) == pid),
                            'Unknown'
                        )
                        play_history.append(format_play(p, name, team))
                    game_context['play_by_play'] = play_history[-10:]
                
                # Get AI response
                with st.spinner("Thinking..."):
                    response = get_ai_response(chat_input, game_context)
                    st.session_state.chat_history.append(("user", chat_input))
                    st.session_state.chat_history.append(("ai", response))
                    
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")

    # Display chat history in scrollable container
    with st.container():
        for role, message in reversed(st.session_state.chat_history):
            st.markdown(
                f"""<div style='border-left: 3px solid {"#0066cc" if role == "ai" else "#666666"}; 
                padding-left: 10px; margin: 10px 0;'>
                <p><strong>{'AI' if role == 'ai' else 'You'}:</strong> {message}</p>
                </div>""", 
                unsafe_allow_html=True
            )

# Main game animation section
if animate:
    st.session_state.play_index = 0  # Restart if manually triggered

if animate and game_id:
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
        analytics_area = st.empty()
        
        # Initialize scores
        scores = {away_code: 0, home_code: 0}
        player_stats = {}
        
        # Fetch and animate plays
        pbp = playbyplay.PlayByPlay(game_id)
        plays = pbp.get_dict().get('game', {}).get('actions', [])
                # Fetch and store plays
        st.session_state.plays = plays  # <- Save to session_state

        for i in range(st.session_state.play_index, len(plays)):
            play = plays[i]
            st.session_state.play_index = i + 1

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
            
            # Update player stats and heatmap
            if name != 'Unknown':
                player_stats = track_player_stats(play, player_stats, name, team)
                
                if play.get('actionNumber', 0) % 10 == 0:
                    analytics_key = f"analytics_{play.get('actionNumber')}_{int(time.time()*1000)}"
                    try:
                        analytics_fig = create_player_performance_charts(player_stats, away_code, home_code)
                        analytics_area.plotly_chart(
                            analytics_fig,
                            use_container_width=True,
                            key=analytics_key
                        )
                    except Exception as chart_error:
                        st.warning(f"Could not update analytics: {str(chart_error)}")
            
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