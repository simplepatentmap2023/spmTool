import streamlit as st

app_top10 = 'https://youtu.be/lMHR5JcyqZo'
ipc_top10 = 'https://youtu.be/7XQ3f4927q4'
app_coapp = 'https://youtu.be/S4oMCLwdw3U'
heatmap = 'https://youtu.be/UEyYmRQb98w'
radarchart = 'https://youtu.be/iaGRFqoNNoA'

videos = [app_top10, ipc_top10, app_coapp, heatmap, radarchart]

for video in videos:
    st.video(video)
