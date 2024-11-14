import streamlit as st
from streamlit_folium import st_folium
import folium

# Title of the app
st.title("Interactive Map with Draggable Markers")

# Define the initial map center coordinates
map_center = [34.0522, -118.2437]  # Example location: Los Angeles

# Initialize map centered at the specified coordinates
m = folium.Map(location=map_center, zoom_start=10)

# Add a draggable center marker
center_marker = folium.Marker(
    location=map_center,
    popup="Center Marker",
    tooltip="Center Marker",
    draggable=True
)
center_marker.add_to(m)

# Track markers in session state
if "markers" not in st.session_state:
    st.session_state.markers = []

# Button to add a new draggable marker
if st.button("Add a New Draggable Marker"):
    # Add a new draggable marker slightly offset each time
    new_marker = [map_center[0] + 0.01 * len(st.session_state.markers), map_center[1]]
    st.session_state.markers.append(new_marker)

# Add each draggable marker from session state to the map
for marker in st.session_state.markers:
    folium.Marker(location=marker, popup="New Draggable Marker", tooltip="New Marker", draggable=True).add_to(m)

# Display the map
st_folium(m, width=700, height=500)
