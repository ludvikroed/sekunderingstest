import streamlit as st
import time

overskrift = st.empty()
overskrift1 = st.empty()
overskrift2 = st.empty()

with overskrift:
  st.title('Sekunderingsverktøy')

with overskrift1:
  st.write("Når du skriver inn starttider må du skrive: timer:minutter:sekunder:sekunder Eksempell: 12:43:15")

with overskrift2:
  st.write("Det er viktig at du skriver starttidene riktig ellers vil ikke systemet fungere sånn det skal. Det er også viktig at du skriver starttidene i stigene rekkefølge.  Altså sånn at løper en starter først og løper to starter som nr.2")
forklaring_starter = st.empty()
slider = st.empty()

navn1 = st.empty()
starttid1 = st.empty()
navn2 = st.empty()
starttid2 = st.empty()
navn3 = st.empty()
starttid3 = st.empty()
navn4 = st.empty()
starttid4 = st.empty()
navn5 = st.empty()
starttid5 = st.empty()
navn6 = st.empty()
starttid6 = st.empty()

send_starttider1 = st.empty()

knapp_løper_1 = st.empty()
knapp_løper_2 = st.empty()
knapp_løper_3 = st.empty()
knapp_løper_4 = st.empty()
knapp_løper_5 = st.empty()

send_tider = st.empty()

runde_nr = 1

with slider:
  antall_løpere = st.selectbox("Velg hvor mange løpere du vil sekundere", options=[2, 3, 4, 5, 6])
  st.session_state.key = antall_løpere

with navn1:
  løper_en_navninput = st.text_input('Skriv navnet til løper 1:')
with starttid1:
  løper_en_startinput = st.text_input('Skriv starttiden til løper 1:')

with navn2:
  løper_to_navninput = st.text_input('Skriv navnet til løper 2:')
with starttid2:
  løper_to_startinput = st.text_input('Skriv starttiden til løper 2:')

with navn3:
  løper_tre_navninput = st.text_input('Skriv navnet til løper 3:')
with starttid3:
  løper_tre_startinput = st.text_input('Skriv starttiden til løper 3:')

with navn4:
  løper_fire_navninput = st.text_input('Skriv navnet til løper 4:')
with starttid4:
  løper_fire_startinput = st.text_input('Skriv starttiden til løper 4:')

with navn5:
  løper_fem_navninput = st.text_input('Skriv navnet til løper 5:')
with starttid5:
  løper_fem_startinput = st.text_input('Skriv starttiden til løper 5:')

with navn6:
  løper_seks_navninput = st.text_input('Skriv navnet til løper 6:')
with starttid6:
  løper_seks_startinput = st.text_input('Skriv starttiden til løper 6:')

if antall_løpere < 3:
  navn3.empty()
  starttid3.empty()

if antall_løpere < 4:
  navn4.empty()
  starttid4.empty()

if antall_løpere < 5:
  navn5.empty()
  starttid5.empty()

if antall_løpere < 6:
  navn6.empty()
  starttid6.empty()

with send_tider:
  send_starttider = st.button('Jeg er ferdig med å fylle ut tider og navn')

if send_starttider:
  if antall_løpere == 2:
    if løper_en_navninput == "" or løper_to_navninput == "":
      st.write('Du må fylle inn navnene til alle løperne')
    elif løper_en_startinput == "" or løper_to_startinput == "":
      st.write('Du må fylle inn starttidene til alle løperene')
    elif løper_en_startinput > løper_to_startinput:
      st.write('Du må skrive starttidene i stigene rekkefølge')
    elif løper_en_navninput == løper_to_navninput:
      st.write('Du har skrevet et navn to ganger')
    else:
      st.session_state["starttider"] = 1

  elif antall_løpere == 3:
    if løper_en_navninput == "" or løper_to_navninput == "" or løper_tre_navninput == "":
      st.write('Du må fylle inn navnene til alle løperne')
    elif løper_en_startinput == "" or løper_to_startinput == "" or løper_tre_startinput == "":
      st.write('Du må fylle inn starttidene til alle løperene')
    elif løper_en_startinput > løper_to_startinput or løper_en_startinput > løper_tre_startinput or løper_to_startinput > løper_tre_startinput:
      st.write('Du må skrive starttidene i stigene rekkefølge')
    elif løper_en_navninput == løper_to_navninput or løper_en_navninput == løper_tre_navninput or løper_to_navninput == løper_tre_navninput:
      st.write('Du har skrevet et navn to ganger')
    else:
      st.session_state["starttider"] = 1

  elif antall_løpere == 4:
    if løper_en_navninput == "" or løper_to_navninput == "" or løper_tre_navninput == "" or løper_fire_navninput == "":
      st.write('Du må fylle inn navnene til alle løperne')
    elif løper_en_startinput == "" or løper_to_startinput == "" or løper_tre_startinput == "" or løper_fire_startinput == "":
      st.write('Du må fylle inn starttidene til alle løperene')
    elif løper_en_startinput > løper_to_startinput or løper_en_startinput > løper_tre_startinput or løper_to_startinput > løper_tre_startinput or løper_en_startinput > løper_fire_startinput or løper_to_startinput > løper_fire_startinput or løper_tre_startinput > løper_fire_startinput:
      st.write('Du må skrive starttidene i stigene rekkefølge')
    elif løper_en_navninput == løper_to_navninput or løper_en_navninput == løper_tre_navninput or løper_to_navninput == løper_tre_navninput or løper_en_navninput == løper_fire_navninput or løper_to_navninput == løper_fire_navninput or løper_tre_navninput == løper_fire_startinput:
      st.write('Du har skrevet et navn to ganger')
    else:
      st.session_state["starttider"] = 1

  elif antall_løpere == 5:
    if løper_en_navninput == "" or løper_to_navninput == "" or løper_tre_navninput == "" or løper_fire_navninput == "" or løper_fem_navninput == "":
      st.write('Du må fylle inn navnene til alle løperne')
    elif løper_en_startinput == "" or løper_to_startinput == "" or løper_tre_startinput == "" or løper_fire_startinput == "" or løper_fire_startinput == "":
      st.write('Du må fylle inn starttidene til alle løperene')
    elif løper_en_startinput > løper_to_startinput or løper_en_startinput > løper_tre_startinput or løper_to_startinput > løper_tre_startinput or løper_en_startinput > løper_fire_startinput or løper_to_startinput > løper_fire_startinput or løper_tre_startinput > løper_fire_startinput or løper_en_startinput > løper_fem_startinput or løper_to_startinput > løper_fem_startinput or løper_tre_startinput > løper_fem_startinput or løper_fire_startinput > løper_fem_startinput:
      st.write('Du må skrive starttidene i stigene rekkefølge')
    elif løper_en_navninput == løper_to_navninput or løper_en_navninput == løper_tre_navninput or løper_to_navninput == løper_tre_navninput or løper_en_navninput == løper_fire_navninput or løper_to_navninput == løper_fire_navninput or løper_tre_navninput == løper_fire_startinput or løper_en_navninput == løper_fem_navninput or løper_to_navninput == løper_fem_startinput or løper_tre_navninput == løper_fem_navninput or løper_fire_navninput == løper_fem_navninput:
      st.write('Du har skrevet et navn to ganger')
    else:
      st.session_state["starttider"] = 1

  elif antall_løpere == 6:
    if løper_en_navninput == "" or løper_to_navninput == "" or løper_tre_navninput == "" or løper_fire_navninput == "" or løper_fem_navninput == "":
      st.write('Du må fylle inn navnene til alle løperne')
    elif løper_en_startinput == "" or løper_to_startinput == "" or løper_tre_startinput == "" or løper_fire_startinput == "" or løper_fire_startinput == "":
      st.write('Du må fylle inn starttidene til alle løperene')
    elif løper_en_startinput > løper_to_startinput or løper_en_startinput > løper_tre_startinput or løper_to_startinput > løper_tre_startinput or løper_en_startinput > løper_fire_startinput or løper_to_startinput > løper_fire_startinput or løper_tre_startinput > løper_fire_startinput or løper_en_startinput > løper_fem_startinput or løper_to_startinput > løper_fem_startinput or løper_tre_startinput > løper_fem_startinput or løper_fire_startinput > løper_fem_startinput or løper_en_startinput > løper_seks_startinput or løper_to_startinput > løper_seks_startinput or løper_tre_startinput > løper_seks_startinput or løper_fire_startinput > løper_seks_startinput or løper_fire_startinput > løper_seks_startinput or løper_fem_startinput > løper_seks_startinput:
      st.write('Du må skrive starttidene i stigene rekkefølge')
    elif løper_en_navninput == løper_to_navninput or løper_en_navninput == løper_tre_navninput or løper_to_navninput == løper_tre_navninput or løper_en_navninput == løper_fire_navninput or løper_to_navninput == løper_fire_navninput or løper_tre_navninput == løper_fire_navninput or løper_en_navninput == løper_fem_navninput or løper_to_navninput == løper_fem_navninput or løper_tre_navninput == løper_fem_navninput or løper_fire_navninput == løper_fem_navninput == løper_en_navninput == løper_seks_navninput or løper_to_navninput == løper_seks_navninput or løper_tre_navninput == løper_seks_navninput or løper_fire_navninput == løper_seks_navninput or løper_fire_navninput == løper_seks_navninput or løper_fem_navninput == løper_seks_navninput:
      st.write('Du har skrevet et navn to ganger')
    else:
      st.session_state["starttider"] = 1

def regn_starttid(start_tid_input):
    løper_start_split = start_tid_input.split(":")
    løper_start_sekunder = int(løper_start_split[0])*3600 + int(løper_start_split[1])*60 + int(løper_start_split[2])
    return (løper_start_sekunder)

def løper_passerer(løper_start_tid):
    løper_pa_tid= time.time()
    løper_tid = løper_pa_tid - løper_start_tid
    return (løper_tid)

def regn_forskjell(start_en, start_to):
    forskjell = start_to - start_en 
    return (forskjell)

def regn_negativ_positiv(forskjell):
  if forskjell < 0:
    bak_foran = 'foran'

  if forskjell == 0:
    bak_foran = 'foran'

  if forskjell > 0:
    bak_foran = 'bak'

  return(bak_foran)

if "starttider" in st.session_state:
  tab1, tab2,  = st.tabs(["Sekundering", "Logg"])
  overskrift.empty()
  overskrift1.empty()
  overskrift2.empty()
  slider.empty()
  forklaring_starter.empty()
  navn1.empty()
  navn2.empty()
  navn3.empty()
  navn4.empty()
  navn5.empty()
  navn6.empty()
  starttid1.empty()
  starttid2.empty()
  starttid3.empty()
  starttid4.empty()
  starttid5.empty()
  starttid6.empty()
  send_starttider1.empty()
  send_tider.empty()

  if "antall_passeringer" not in st.session_state:
    st.session_state["antall_passeringer"] =  0
    antall_passeringer = 0

  if "regning" not in st.session_state:
    st.session_state["regning"] = 1
    if antall_løpere >= 2:
      løper_en_start = regn_starttid(løper_en_startinput)
      løper_to_start = regn_starttid(løper_to_startinput)
      st.session_state["løper_en_start"] = løper_en_start  
      st.session_state["løper_to_start"] = løper_to_start
    if antall_løpere >= 3: 
      løper_tre_start = regn_starttid(løper_tre_startinput)
      st.session_state["løper_tre_start"] = løper_tre_start

    if antall_løpere >= 4:
      løper_fire_start = regn_starttid(løper_fire_startinput)
      st.session_state["løper_fire_start"] = løper_fire_start

    if antall_løpere >= 5:
      løper_fem_start = regn_starttid(løper_fem_startinput)
      st.session_state["løper_fem_start"] = løper_fem_start

    if antall_løpere == 6:
      løper_seks_start = regn_starttid(løper_seks_startinput)
      st.session_state["løper_seks_start"] = løper_seks_start
    
  with tab1:
    st.header("Sekundering")
    st.write('Trykk på navnet til løperen som passerer:')

    if antall_løpere > 1:
      st.write('')
      løper_en_knapp = st.button(løper_en_navninput)
      if løper_en_knapp:
        løper_en_start = st.session_state["løper_en_start"]
        passering_løper_en = løper_passerer(løper_en_start)
        løper_en_navninput, 'har passert'
        st.session_state["passering_løper_en"] = passering_løper_en

    if antall_løpere >= 2:
      st.write('')
      løper_to_knapp = st.button(løper_to_navninput)

      if løper_to_knapp:
        løper_to_start = st.session_state["løper_to_start"]
        passering_løper_en = st.session_state["passering_løper_en"]

        passering_løper_to = løper_passerer(løper_to_start)
        forskjell_på_en_to = regn_forskjell(passering_løper_en, passering_løper_to)

        forskjell_på_en_to = round(forskjell_på_en_to, 1)

        bak_foran = regn_negativ_positiv(forskjell_på_en_to)
        forskjell_på_en_to = abs(forskjell_på_en_to)

        st.session_state["passering_løper_to"] = passering_løper_to

        løper_to_navninput, "er", forskjell_på_en_to, "sekunder", bak_foran, løper_en_navninput

        if 'løper_to_passeringer' not in st.session_state:
          st.session_state["løper_to_passeringer"] = 0

        st.session_state["løper_to_passeringer"] = st.session_state["løper_to_passeringer"] + 1

        a = st.session_state.løper_to_passeringer
        st.session_state[a] = løper_to_navninput, "er", forskjell_på_en_to, "sekunder", bak_foran, løper_en_navninput

    if antall_løpere >= 3:
      st.write('')
      løper_tre_knapp = st.button(løper_tre_navninput)

      if løper_tre_knapp:
        løper_tre_start = st.session_state["løper_tre_start"]
        passering_løper_en = st.session_state["passering_løper_en"]
        passering_løper_to = st.session_state["passering_løper_to"]

        passering_løper_tre = løper_passerer(løper_tre_start)
        st.session_state["passering_løper_tre"] = passering_løper_tre

        forskjell_på_to_tre = regn_forskjell(passering_løper_to, passering_løper_tre)
        forskjell_på_en_tre = regn_forskjell(passering_løper_en, passering_løper_tre)

        forskjell_på_en_tre = round(forskjell_på_en_tre, 1)
        forskjell_på_to_tre = round(forskjell_på_to_tre, 1)

        bak_foran = regn_negativ_positiv(forskjell_på_en_tre)
        forskjell_på_en_tre = abs(forskjell_på_en_tre)

        løper_tre_navninput, "er", forskjell_på_en_tre, "sekunder", bak_foran, løper_en_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_to_tre)
        forskjell_på_to_tre = abs(forskjell_på_to_tre)

        løper_tre_navninput, "er", forskjell_på_to_tre, "sekunder", bak_foran, løper_to_navninput
        if 'løper_tre_passeringer' not in st.session_state:
          st.session_state["løper_tre_passeringer"] = 0

        st.session_state["løper_tre_passeringer"] = st.session_state["løper_tre_passeringer"] + 1

        a = st.session_state.løper_tre_passeringer + 1000
        st.session_state[a] = løper_tre_navninput, "er", forskjell_på_en_tre, "sekunder", bak_foran, løper_en_navninput
        a += 1
        st.session_state["løper_tre_passeringer"] = st.session_state["løper_tre_passeringer"] + 1
        st.session_state[a] = løper_tre_navninput, "er", forskjell_på_to_tre, "sekunder", bak_foran, løper_to_navninput

  
    if antall_løpere >= 4:
      st.write('')
      løper_fire_knapp = st.button(løper_fire_navninput)
  
      if løper_fire_knapp:
        løper_fire_start = st.session_state["løper_fire_start"]
        passering_løper_en = st.session_state["passering_løper_en"]
        passering_løper_to = st.session_state["passering_løper_to"]
        passering_løper_tre = st.session_state["passering_løper_tre"]

        passering_løper_fire = løper_passerer(løper_fire_start)
        st.session_state["passering_løper_fire"] = passering_løper_fire

        forskjell_på_tre_fire = regn_forskjell(passering_løper_tre, passering_løper_fire)
        forskjell_på_to_fire = regn_forskjell(passering_løper_to, passering_løper_fire)
        forskjell_på_en_fire = regn_forskjell(passering_løper_en, passering_løper_fire)

        forskjell_på_tre_fire = round(forskjell_på_tre_fire, 1)
        forskjell_på_to_fire = round(forskjell_på_to_fire, 1)
        forskjell_på_en_fire = round(forskjell_på_en_fire, 1)

        bak_foran = regn_negativ_positiv(forskjell_på_en_fire)
        forskjell_på_en_fire = abs(forskjell_på_en_fire)

        løper_fire_navninput, "er", forskjell_på_en_fire, "sekunder", bak_foran, løper_en_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_to_fire)
        forskjell_på_to_fire = abs(forskjell_på_to_fire)

        løper_fire_navninput, "er", forskjell_på_to_fire, "sekunder", bak_foran, løper_to_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_tre_fire)
        forskjell_på_tre_fire = abs(forskjell_på_tre_fire)

        løper_fire_navninput, "er", forskjell_på_tre_fire, "sekunder", bak_foran, løper_tre_navninput

        if 'løper_fire_passeringer' not in st.session_state:
          st.session_state["løper_fire_passeringer"] = 0

        st.session_state["løper_fire_passeringer"] = st.session_state["løper_fire_passeringer"] + 1
        
        a = st.session_state.løper_fire_passeringer + 2000
        st.session_state[a] = løper_fire_navninput, "er", forskjell_på_en_fire, "sekunder", bak_foran, løper_en_navninput
        st.session_state["løper_fire_passeringer"] = st.session_state["løper_fire_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_fire_navninput, "er", forskjell_på_to_fire, "sekunder", bak_foran, løper_to_navninput
        st.session_state["løper_fire_passeringer"] = st.session_state["løper_fire_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_fire_navninput, "er", forskjell_på_tre_fire, "sekunder", bak_foran, løper_tre_navninput
        
    if antall_løpere >= 5:
      st.write('')
      løper_fem_knapp = st.button(løper_fem_navninput)

      if løper_fem_knapp:
        løper_fem_start = st.session_state["løper_fem_start"]
        passering_løper_en = st.session_state["passering_løper_en"]
        passering_løper_to = st.session_state["passering_løper_to"]
        passering_løper_tre = st.session_state["passering_løper_tre"]
        passering_løper_fire = st.session_state["passering_løper_fire"]

        passering_løper_fem = løper_passerer(løper_fem_start)
        st.session_state["passering_løper_fem"] = passering_løper_fem

        forskjell_på_fire_fem = regn_forskjell(passering_løper_fire, passering_løper_fem)
        forskjell_på_tre_fem = regn_forskjell(passering_løper_tre, passering_løper_fem)
        forskjell_på_to_fem = regn_forskjell(passering_løper_to, passering_løper_fem)
        forskjell_på_en_fem = regn_forskjell(passering_løper_en, passering_løper_fem)

        forskjell_på_en_fem = round(forskjell_på_en_fem, 1)
        forskjell_på_to_fem = round(forskjell_på_to_fem, 1)
        forskjell_på_tre_fem = round(forskjell_på_tre_fem, 1)
        forskjell_på_fire_fem = round(forskjell_på_fire_fem, 1)

        bak_foran = regn_negativ_positiv(forskjell_på_en_fem)
        forskjell_på_en_fem = abs(forskjell_på_en_fem)

        løper_fem_navninput, "er", forskjell_på_en_fem, "sekunder", bak_foran, løper_en_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_to_fem)
        forskjell_på_to_fem = abs(forskjell_på_to_fem)

        løper_fem_navninput, "er", forskjell_på_to_fem, "sekunder", bak_foran, løper_to_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_tre_fem)
        forskjell_på_tre_fem = abs(forskjell_på_tre_fem)

        løper_fem_navninput, "er", forskjell_på_tre_fem, "sekunder", bak_foran, løper_tre_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_fire_fem)
        forskjell_på_fire_fem = abs(forskjell_på_fire_fem)

        løper_fem_navninput, "er", forskjell_på_fire_fem, "sekunder", bak_foran, løper_fire_navninput

        if 'løper_fem_passeringer' not in st.session_state:
          st.session_state["løper_fem_passeringer"] = 0

        st.session_state["løper_fem_passeringer"] = st.session_state["løper_fem_passeringer"] + 1

        a = st.session_state.løper_fem_passeringer + 3000
        st.session_state[a] = løper_fem_navninput, "er", forskjell_på_en_fem, "sekunder", bak_foran, løper_en_navninput
        st.session_state["løper_fem_passeringer"] = st.session_state["løper_fem_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_fem_navninput, "er", forskjell_på_to_fem, "sekunder", bak_foran, løper_to_navninput
        st.session_state["løper_fem_passeringer"] = st.session_state["løper_fem_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_fem_navninput, "er", forskjell_på_tre_fem, "sekunder", bak_foran, løper_tre_navninput
        st.session_state["løper_fem_passeringer"] = st.session_state["løper_fem_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_fem_navninput, "er", forskjell_på_fire_fem, "sekunder", bak_foran, løper_fire_navninput
  
    if antall_løpere >= 6:
      st.write('')
      løper_seks_knapp = st.button(løper_seks_navninput)

      if løper_seks_knapp:
        løper_seks_start = st.session_state["løper_seks_start"]
        passering_løper_en = st.session_state["passering_løper_en"]
        passering_løper_to = st.session_state["passering_løper_to"]
        passering_løper_tre = st.session_state["passering_løper_tre"]
        passering_løper_fire = st.session_state["passering_løper_fire"]
        passering_løper_fem = st.session_state["passering_løper_fem"]

        passering_løper_seks = løper_passerer(løper_seks_start)
        st.session_state["passering_løper_seks"] = passering_løper_seks

        forskjell_på_fem_seks = regn_forskjell(passering_løper_fem, passering_løper_seks)
        forskjell_på_fire_seks = regn_forskjell(passering_løper_fire, passering_løper_seks)
        forskjell_på_tre_seks = regn_forskjell(passering_løper_tre, passering_løper_seks)
        forskjell_på_to_seks = regn_forskjell(passering_løper_to, passering_løper_seks)
        forskjell_på_en_seks = regn_forskjell(passering_løper_en, passering_løper_seks)

        forskjell_på_en_seks = round(forskjell_på_en_seks, 1)
        forskjell_på_to_seks = round(forskjell_på_to_seks, 1)
        forskjell_på_tre_seks = round(forskjell_på_tre_seks, 1)
        forskjell_på_fire_seks = round(forskjell_på_fire_seks, 1)
        forskjell_på_fem_seks = round(forskjell_på_fem_seks, 1)

        bak_foran = regn_negativ_positiv(forskjell_på_en_seks)
        forskjell_på_en_seks = abs(forskjell_på_en_seks)

        løper_seks_navninput, "er", forskjell_på_en_seks, "sekunder", bak_foran, løper_en_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_to_seks)
        forskjell_på_to_seks = abs(forskjell_på_to_seks)

        løper_seks_navninput, "er", forskjell_på_to_seks, "sekunder", bak_foran, løper_to_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_tre_seks)
        forskjell_på_tre_seks = abs(forskjell_på_tre_seks)

        løper_seks_navninput, "er", forskjell_på_tre_seks, "sekunder", bak_foran, løper_tre_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_fire_seks)
        forskjell_på_fire_seks = abs(forskjell_på_fire_seks)

        løper_seks_navninput, "er", forskjell_på_fire_seks, "sekunder", bak_foran, løper_fire_navninput

        bak_foran = regn_negativ_positiv(forskjell_på_fem_seks)
        forskjell_på_fem_seks = abs(forskjell_på_fem_seks)

        løper_seks_navninput, "er", forskjell_på_fem_seks, "sekunder", bak_foran, løper_fem_navninput

        if 'løper_seks_passeringer' not in st.session_state:
          st.session_state["løper_seks_passeringer"] = 0

        st.session_state["løper_seks_passeringer"] = st.session_state["løper_seks_passeringer"] + 1

        a = st.session_state.løper_seks_passeringer + 4000
        st.session_state[a] = løper_seks_navninput, "er", forskjell_på_en_seks, "sekunder", bak_foran, løper_en_navninput
        st.session_state["løper_seks_passeringer"] = st.session_state["løper_seks_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_seks_navninput, "er", forskjell_på_to_seks, "sekunder", bak_foran, løper_to_navninput
        st.session_state["løper_seks_passeringer"] = st.session_state["løper_seks_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_seks_navninput, "er", forskjell_på_tre_seks, "sekunder", bak_foran, løper_tre_navninput
        st.session_state["løper_seks_passeringer"] = st.session_state["løper_seks_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_seks_navninput, "er", forskjell_på_fire_seks, "sekunder", bak_foran, løper_fire_navninput
        st.session_state["løper_seks_passeringer"] = st.session_state["løper_seks_passeringer"] + 1
        a += 1
        st.session_state[a] = løper_seks_navninput, "er", forskjell_på_fem_seks, "sekunder", bak_foran, løper_fem_navninput


  with tab2:
    st.header("Logg")
    logg = st.container()

    st.subheader('Starttider:')
    løper_en_navninput, 'startet:' , løper_en_startinput
    
    løper_to_navninput, 'startet:', løper_to_startinput
    
    if antall_løpere >= 3:
      løper_tre_navninput, 'startet:' , løper_tre_startinput

    if antall_løpere >= 4:
      løper_fire_navninput, 'startet:' , løper_fire_startinput

    if antall_løpere >= 5:
      løper_fem_navninput, 'startet:' , løper_fem_startinput

    if antall_løpere >= 6:
      løper_seks_navninput, 'startet:' , løper_seks_startinput


  if 'løper_to_passeringer' not in st.session_state:
    st.session_state.løper_to_passeringer = 0
  
  if 'løper_tre_passeringer' not in st.session_state:
    st.session_state.løper_tre_passeringer = 0
  
  if 'løper_fire_passeringer' not in st.session_state:
    st.session_state.løper_fire_passeringer = 0
  
  if 'løper_fem_passeringer' not in st.session_state:
    st.session_state.løper_fem_passeringer = 0
  
  if 'løper_seks_passeringer' not in st.session_state:
    st.session_state.løper_seks_passeringer = 0
  
  antall_løpere = st.session_state.key

  

  with tab2:
    st.subheader('Sekunderingstider:')
    passering = 1
    a = 1
    for i in range(st.session_state.løper_to_passeringer):
      'passering', passering, 'for', løper_to_navninput, ':'
      st.markdown(st.session_state[a])
      a += 1
      passering += 1

    if antall_løpere >= 3:
        b = 1001
        passering = 2
        passering_ = 1
        for i in range(st.session_state.løper_tre_passeringer):
          if passering%2 == 0:
            'passering', passering_, 'for', løper_tre_navninput, ':'
            passering_ += 1
          st.markdown(st.session_state[b])
          b += 1
          passering += 1

    if antall_løpere >= 4:
        passering = 3
        passering_ = 1
        b = 2001
        for i in range(st.session_state.løper_fire_passeringer):
          if passering%3 == 0:
            'passering', passering_, 'for', løper_fire_navninput, ':'
            passering_ += 1 
          st.markdown(st.session_state[b])
          b += 1
          passering += 1
    
    if antall_løpere >= 5:
        passering = 4
        passering_ = 1
        b = 3001
        for i in range(st.session_state.løper_fem_passeringer):
          if passering%4 == 0:
            'passering', passering_, 'for', løper_fem_navninput, ':'
            passering_ += 1
          st.markdown(st.session_state[b])
          b += 1
          passering += 1

    if antall_løpere == 6:
        passering = 5
        passering_ = 1
        b = 4001
        for i in range(st.session_state.løper_seks_passeringer):
          if passering%5 == 0:
            'passering', passering_, 'for', løper_seks_navninput, ':'
            passering_ += 1
          st.markdown(st.session_state[b])
          b += 1
          passering += 1

  st.write('')
  st.write('')
  st.write("Trykk på knappen under to ganger for å gå tilbake til starttider." )
  st.write("Advarsel: Du vil miste hele loggen og starttidene du allerede har lagt inn.")
  tilbake = st.button('Gå tilbake til starttider')
  if tilbake:
    for key in st.session_state.keys():
      st.balloons()
      del st.session_state[key]