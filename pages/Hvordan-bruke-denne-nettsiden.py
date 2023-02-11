import streamlit as st

st.header('Hvordan bruke denne nettsiden')

st.subheader('Hvordan sekunder ved å legge ved en fil:')

video_file = open('hvordan bruke sekunderingsprogram.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

st.write('Gå inn på "EQtiming.com"')

st.write("Finn ditt skirenn")

st.write("Trykk på deltakere")
st.write("Trykk på streken øverst i høyre hjørnet")

st.write("Trykk på filer")
st.write("Last ned den øverste filen i xml format")
st.write("Gå tilbake til sekunderingsverktøyet")
st.write('Trykk på "Browse files"')
st.write("Finn filen du lastet ned fra EQtiming. ")
st.write("Det kan være forskjell på teleforner og filsystemet deres. Derfor kan det være at du må lete å eksprementere med hvordan du legger ved filen")

st.write(" ")
st.write(" ")
st.write(" ")
st.write("Lagd av: Ludvik Blichfeldt Rød")
