import streamlit as st
import xmltodict
import pandas as pd
import time
import requests


if "tider_er_lastet_ned" not in st.session_state:
	st.session_state["tider_er_lastet_ned"] = False
	st.session_state["hvis_starttider"] = False
try:
	if send_starttider:
		ok = "ok"
except:
	send_starttider = False

def løp_i_dag_er_valgt(id):
	try:
		st.session_state["løpe_id"] = id
		url = "https://live.eqtiming.com/api//Report/221?eventId=" + str(id)
		response = requests.get(url)
		xml_content = response.content

		data_dict = xmltodict.parse(xml_content)

		st.session_state["noe_er_fel_med_link"] = "Det var noe som gikk feil med nedlastning av startliste. Du kan prøver å trykke på kanppen på nytt"
		st.session_state["løpere_data_list"] = [dict(x) for x in data_dict["startliste"]["start"]]
		st.session_state["tider_er_lastet_ned"] = True
	except:
		st.session_state["feil_med_valg_av_renn"] = "Programmet greide ikke å lese EQtiming sin nettside. Det kan være at Startlista på EQtiming er tom."
	st.experimental_rerun()

if "antall_løpere" not in st.session_state:
	st.session_state.antall_løpere = 0

st.title('Sekunderingsverktøy')	

cols = ["Startnummer:","Fornavn:", "Etternavn:", "Klasse:", "Starttid:", "Team:"]
rows = []
startliste_row = []

hvis_løpere = 1

def get_json_data():

	url = "https://events.eqtiming.com/api/Events?query=&dateFrom=2023-01-01+00%3A00&dateTo=2023-05-31+23%3A59&organizationId=0&regionIds=&levelIds=&sportIds=&take=1500&dateSort=true&desc=false&onlyValidated=false&onlyshowfororganizer=false&organizerIds="
	r = requests.get(url)
	json_data = r.json()

	x = 0
	renn = pd.DataFrame()

	for renn_data in json_data:
		sportid_2 = renn_data['Sport']['Parent']['Id']
		sportid_3 = renn_data['Sport']['Parent']['Parent']['Id']

		if sportid_2 == 20 or sportid_3 == 20:
			sport = "Sykkel"#sykkel
		elif sportid_2 == 1:
			sport = "Langrenn"#langrenn
		elif sportid_2 == 5:
			sport = "Skiskyting"#skiskyting
		elif sportid_2 == 15 or sportid_3 == 15:
			sport = "løping"#løping
		elif sportid_2 == 4:
			sport = "Orientering"
		else:
			sport = "Annet"

		
		start_time = renn_data['Starttime'].split("T")[0]	
		end_time = renn_data['EndTime'].split("T")[0]
		name = renn_data['Name']
		active = str(renn_data["Signup"]["Active"])

		sted = renn_data["City"]["Name"]
		arrangerende_klubb = renn_data['Organizer']["Name"]
		renn_id = renn_data['Id']
		row = pd.DataFrame({"navn": name,
							"sted": sted,
							"arrangerende_klubb": arrangerende_klubb,
							"start_dato": start_time,
							"end_dato": end_time,
							"id": renn_id, 
							"active": active,
							"sport": sport},
							index=[0])

		renn = pd.concat([renn, row.reset_index(drop=True)], ignore_index=True)
		x += 1
	return renn
	

if st.session_state["hvis_starttider"] == False:
	if st.session_state["tider_er_lastet_ned"]  == False:
		if "feil_med_valg_av_renn" in st.session_state:
			st.warning(st.session_state["feil_med_valg_av_renn"])			
			
		with st.expander("Søk"):
			søk = st.text_input("Søk", label_visibility="collapsed")
			sport = st.selectbox(" ", ["Alle sporter", "Langrenn", "Skiskyting", "Løping", "Orientering", "Sykkel",  "Annet"], label_visibility="collapsed")
			dato_valgt = st.date_input("Hvis rennet ditt ikke er i dag kan du velge dato rennet går her:")
			dato_valgt = str(dato_valgt)
			hva_søkes = st.radio("Velg hva du vil søke på", ["Dato valgt", "Alle konkuranser"], label_visibility="collapsed")

		with st.expander("Velg hva som skal hvises på knappene:"):
			KnappHvisArrangereneSport = st.checkbox("Sport")
			KnappHvisArrangereneklubb = st.checkbox("Arrangør")
			KnappHvisSted = st.checkbox("Sted")

		if "alle_renn" not in st.session_state:
			st.session_state["alle_renn"] = get_json_data()
		if dato_valgt not in st.session_state:
			st.session_state[dato_valgt + "dato"] = st.session_state["alle_renn"][st.session_state["alle_renn"]['start_dato'].str.contains(dato_valgt)]

		if hva_søkes == "Alle konkuranser":
			df = st.session_state["alle_renn"]
		else:
			df = st.session_state[dato_valgt + "dato"]
		
		if sport != "Alle sporter":
			df = df[df['sport'].str.lower().str.contains(sport.lower())]	
		
		if søk != "":
			df = df[df['navn'].str.lower().str.contains(søk.lower())]	

		teller = 0
		a = 1
		for index, row in df.iterrows():
			button_label = row['navn']
			if KnappHvisArrangereneSport:
				button_label = button_label + " (Sport: " + row['sport'] + ")"
			if KnappHvisArrangereneklubb:
				button_label = button_label + " (Arrangør: " + row['arrangerende_klubb'] + ")"
			if KnappHvisSted:
				button_label = button_label + " (Sted: " + row['sted'] + ")"

			renn_er_valgt = st.button( "(" + str(a) + ") " + button_label)
			
			if renn_er_valgt:
				løp_i_dag_er_valgt(row['id'])
			a += 1
	hvis_løpere = 0

	if st.session_state["tider_er_lastet_ned"]:
		tab2, tab3, tab4 = st.tabs(["Velg løpere", "Startlister", "Løpere valgt"])
	
		if "resatt" not in st.session_state:
			if "Lister_er_lagd" not in st.session_state:
				klasser_dict = {'Startliste:': ''}
				klasser_dict_to = {'Velg klasse her': '', 'Startliste:': ''}				
	
				st.session_state["klasser_dict_to"] = klasser_dict_to
				st.session_state["klasser_dict"] = klasser_dict

				x = 0
				a = 0

				rows = pd.DataFrame(columns=cols)
				startliste_row = pd.DataFrame(columns=cols)
				
				for i in(st.session_state["løpere_data_list"]):
					løper = (st.session_state["løpere_data_list"][x])
					fornavn = (løper['@fornavn'])
					etternavn = (løper['@etternavn'])
					klasse = (løper['@klasse'])
					starttid = (løper['@starttid'])
					startnr = (løper['@startno'])
					team = (løper['@team'])
					csvid = klasse + ".csv"

					if klasse not in klasser_dict:
						klasser_dict[klasse] = klasse
						klasser_dict_to[klasse] = klasse  
						st.session_state[csvid] = pd.DataFrame(columns=cols)
		
					rows_ny = pd.DataFrame({"Startnummer:": startnr,
											"Fornavn:": fornavn,
											"Etternavn:": etternavn,
											"Klasse:": klasse,
											"Starttid:": starttid,
											"Team:": team},
											index=["løper"])

					startliste_row_ny = pd.DataFrame({"Startnummer:": startnr,
														"Fornavn:": fornavn,
														"Etternavn:": etternavn,
														"Klasse:": klasse,
														"Starttid:": starttid,
														"Team:": team},
														index=["løper"])


					st.session_state[csvid] = pd.concat([st.session_state[csvid], rows_ny])
					
					startliste_row = pd.concat([startliste_row, startliste_row_ny])
					x += 1
				
				df = pd.DataFrame(rows_ny, columns=cols)
				st.session_state[klasse + '.csv'] = df
				
				startliste = pd.DataFrame(startliste_row, columns=cols)
				st.session_state["Startliste:.csv"] = startliste
				st.session_state["Lister_er_lagd"] = True

			with tab3:
				klasser_dict_to = st.session_state["klasser_dict_to"]

				klasse_som_sekunderes = st.selectbox('Velg hvilken klasse du vil se', klasser_dict_to)

				if klasse_som_sekunderes != 'Velg klasse her':
					df = st.session_state[klasse_som_sekunderes + '.csv']
					st.dataframe(df)
			with tab4:
				if st.session_state.antall_løpere == 0:
					st.write("Du har valgt null løpere")
				if st.session_state.antall_løpere >= 1:
					antall_løpere = st.session_state.antall_løpere
					n = 1
					st.subheader("Her er løperne du har valgt for å sekundere: ")
					if st.session_state.antall_løpere >= 2:
						send_starttider = st.button("Start å sekundere løpere.")
						if send_starttider:
							st.session_state["hvis_starttider"] = True

				if "rerun" in st.session_state:
					st.write("Du har valgt maks antall av løpere for å sekundere trykk på knappen for å starte å sekundere.")
				for i in range(st.session_state.antall_løpere):
					if n == 1:
						løper = "en"
					elif n == 2:
						løper = "to"
					elif n == 3:
						løper = "tre"
					elif n == 4:
						løper = "fire"
					elif n == 5:
						løper = "fem"
					elif n == 6:
						løper = "seks"
					n_str = str(n)
					st.subheader("Løper " + n_str + ":")
					navn = "løper_" + løper + "_navninput"
					starttid = "løper_" + løper + "_startinput"

					st.write("Navn: " + st.session_state[navn])
					st.write("Starttid: " + st.session_state[starttid])
					
					n += 1

			with tab2:
				antall_løpere = st.session_state.antall_løpere
				if antall_løpere >= 2:
					st.write("Du har valgt " + løper + " løpere")
					send_starttider = st.button("Start å sekundere løpere")
					if send_starttider:
						st.session_state["hvis_starttider"] = True
				

				if "rerun" in st.session_state:
					st.write("Du har valgt maks antall av løpere for å sekundere trykk på knappen for å starte å sekundere.")
					for i in range(st.session_state.antall_løpere):
						if n == 1:
							løper = "en"
						elif n == 2:
							løper = "to"
						elif n == 3:
							løper = "tre"
						elif n == 4:
							løper = "fire"
						elif n == 5:
							løper = "fem"
						elif n == 6:
							løper = "seks"
						n_str = str(n)
						st.subheader("Løper " + n_str + ":")
						navn = "løper_" + løper + "_navninput"
						starttid = "løper_" + løper + "_startinput"

						st.write("Navn: " + st.session_state[navn])
						st.write("Starttid: " + st.session_state[starttid])
						
						n += 1
				
				if st.session_state["antall_løpere"] != 6:
					st.subheader("Velg hvilke løpere du vil sekundere:")
					st.write("Husk at seks løpere er maks.")
					if antall_løpere == 0:
						løper = "null"
					elif antall_løpere == 1:
						løper = "en"
					elif antall_løpere == 2:
						løper = "to"
					elif antall_løpere == 3:
						løper = "tre"
					elif antall_løpere == 4:
						løper = "fire"
					elif antall_løpere == 5:
						løper = "fem"
					elif antall_løpere == 6:
						løper = "seks"
					st.write("Du må velge minst to løpere for å sekundere.")
					if antall_løpere == 0:
						st.write("Du har valgt " + løper + " løpere.")
					else:
						st.write("Du har valgt " + løper + " løper.")
					

				if "rerun" not in st.session_state:
					klasser_dict = st.session_state["klasser_dict"]
					if antall_løpere < 6:
						with st.expander("Velg klasse(ikke obligatorisk)"):
							klasse_som_sekunderes_en = st.selectbox("collapsed", options=klasser_dict, label_visibility="collapsed")
						with st.expander("Velg hva som skal hvises på knappene(ikke obligatorisk)"):
							hva_som_hvises_strnr = st.checkbox("Startnummer")
							hva_som_hvises_team = st.checkbox("Team")
							hva_som_hvises_start_tid = st.checkbox("Starttid")
							hva_som_hvises_klasse = st.checkbox("Klasse")
						with st.expander("Søk"):
							search_term = st.text_input("Søk:", label_visibility="collapsed")
							type_søk = st.selectbox("Velg hva du vil søke etter",["Fornavn:", "Etternavn:", "Team:", "Startnummer:", "Starttid:"] )
							df = st.session_state[klasse_som_sekunderes_en + ".csv"]
							result = df[df[type_søk].str.lower().str.contains(search_term.lower())]
							x = 0

							if result.empty:
								result = df[df["Fornavn:"].str.lower().str.contains(search_term.lower())]
								if result.empty == False:
									reader_obj = result
									st.write("Fant ingen som har " + search_term + " som " + type_søk + " men jeg falt noen med det som Fornavn")
									x = 1
								result = df[df["Etternavn:"].str.lower().str.contains(search_term.lower())]
								if result.empty == False:
									reader_obj = result
									st.write("Fant ingen som har " + search_term + " som " + type_søk + " men jeg falt noen med det som Etternavn")
									x = 1
								result = df[df["Team:"].str.lower().str.contains(search_term.lower())]
								if result.empty == False:
									reader_obj = result
									st.write("Fant ingen som har " + search_term + " som " + type_søk + " men jeg falt noen med det som Team")
									x = 1
								result = df[df["Startnummer:"].str.lower().str.contains(search_term.lower())]
								if result.empty == False:
									reader_obj = result
									st.write("Fant ingen som har " + search_term + " som " + type_søk + " men jeg falt noen med det som Startnummer")
									x = 1
								result = df[df["Starttid:"].str.lower().str.contains(search_term.lower())]
								if result.empty == False:
									reader_obj = result
									st.write("Fant ingen som har " + search_term + " som " + type_søk + " men jeg falt noen med det som Starttid")
									x = 1
								if x == 0:
									st.write("Fant ingen " + search_term)

						st.session_state["klasse_som_sekunders"] = klasse_som_sekunderes_en
						if x != 1:
							reader_obj = result
				if "løper_nummer" not in st.session_state:
					st.session_state["løper_nummer"] = 1
				if "forrige_løper" not in st.session_state:
					st.session_state["forrige_løper"] = 1
				
				if antall_løpere == 6:
					reader_obj = pd.DataFrame()

				count_row = reader_obj.shape[0]
				teller = 0
				for row in range(count_row):
					k = str(row)
					knapp = k + 'knapp'
					knapp_id = k + 'knapp'	
					liste_med_løpere = []
					startnummer = str(reader_obj["Startnummer:"][teller])
					fornavn = str(reader_obj["Fornavn:"][teller])
					etternavn = str(reader_obj["Etternavn:"][teller])
					team = str(reader_obj["Team:"][teller])
					starttid = str(reader_obj["Starttid:"][teller])
					klasse = str(reader_obj["Klasse:"][teller])

					løper_navn_og_data = fornavn + " " + etternavn
					løper_navn = fornavn + " " + etternavn
					if hva_som_hvises_strnr:
						løper_navn_og_data = løper_navn_og_data + " (Startnummer: " + str(startnummer) + ")"
					if hva_som_hvises_team:
						løper_navn_og_data = løper_navn_og_data + " (Team: " + str(team) + ")"
					if hva_som_hvises_start_tid:
						løper_navn_og_data = løper_navn_og_data + " (Starttid: " + str(starttid) + ")"
					if hva_som_hvises_klasse:
						løper_navn_og_data = løper_navn_og_data + " (Klasse: " + str(klasse) + ")"

					if "maks_valgt" not in st.session_state:	
						if løper_navn not in st.session_state:
							if løper_navn in liste_med_løpere:
								knapp = st.button(løper_navn_og_data + " " + str(teller), disabled=False)
							else:
								knapp = st.button(løper_navn_og_data, disabled=False)
	
						if løper_navn in st.session_state:
							if løper_navn_og_data in liste_med_løpere:
								knapp = st.button(løper_navn_og_data + " " + str(teller), disabled=True)
								st.write(løper_navn_og_data + " er valgt")
							else:
								knapp = st.button(løper_navn_og_data, disabled=True)
								st.write(løper_navn_og_data + " er valgt")

						liste_med_løpere.append(løper_navn)

					n = 1
					if knapp:
						startnummer = str(reader_obj["Startnummer:"][teller])
						fornavn = str(reader_obj["Fornavn:"][teller])
						etternavn = str(reader_obj["Etternavn:"][teller])
						st.session_state[løper_navn] = True
						if st.session_state["løper_nummer"] == 1:
							løper = "en"
						elif st.session_state["løper_nummer"] == 2:
							løper = "to"
						elif st.session_state["løper_nummer"] == 3:
							løper = "tre"
						elif st.session_state["løper_nummer"] == 4:
							løper = "fire"
						elif st.session_state["løper_nummer"] == 5:
							løper = "fem"
						elif st.session_state["løper_nummer"] == 6:
							løper = "seks"
							
						elif st.session_state["løper_nummer"] >= 7:
							st.session_state["stop"] = True
							if "rerun" not in st.session_state:
								st.session_state["rerun"] = 1
								st.experimental_rerun()

						if "stop" not in st.session_state:
							st.session_state["knapp_for_reset" + løper] = knapp_id
							fornavn = reader_obj["Fornavn:"][teller]
							etternavn = reader_obj["Etternavn:"][teller]
							st.session_state['løper_' + løper + '_navninput'] = fornavn + ' ' + etternavn
							st.session_state['løper_' + løper + '_startinput'] = reader_obj["Starttid:"][teller]
							st.session_state['løper_' + løper + '_startnr'] = reader_obj["Startnummer:"][teller]

							st.write(st.session_state['løper_' + løper + '_navninput'], "er valgt")
							st.session_state[knapp_id] = 1
							
							if løper == "en":
								st.write("Du har valgt " + løper + " løper. Husk at seks løpere er maks")
								st.write("For å starte å sekundere må du velge minst to løpere")

							elif løper == "seks":
								st.subheader("Du har valgt maks antall av løpere.")
							else:
								st.write("Du har valgt " + løper + " løpere. Husk at seks løpere er maks")
								st.write("Hvis du ikke vil sekundere flere løpere kan du bla øverst på siden for å starte å sekundere")

							st.session_state.antall_løpere = st.session_state["løper_nummer"]
							if st.session_state["løper_nummer"] == 6:
								st.session_state["maks_valgt"] = 1

							st.session_state["løper_nummer"] = st.session_state["løper_nummer"] + 1
							st.experimental_rerun()
					teller += 1

runde_nr = 1

def regn_fra_sekk_til_min(seconds):
	if seconds < 60:
		return "0" + ":" + "0" + ":" + str(seconds)
	elif seconds < 3600:
		minutes = seconds // 60
		remaining_seconds = seconds % 60
		return "0" + ":" + str(minutes) + ":" + str(remaining_seconds)
	else:
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60
		remaining_seconds = (seconds % 3600) % 60
		return str(hours) + ":" + str(minutes) + ":" + str(remaining_seconds)

def regn_starttid(start_tid_input):
		løper_start_split = start_tid_input.split(":")
		løper_start_sekunder = int(løper_start_split[0])*3600 + int(løper_start_split[1])*60 + int(løper_start_split[2])
		return (løper_start_sekunder)

if send_starttider:
	løper_en_navninput = st.session_state['løper_en_navninput']
	løper_to_navninput = st.session_state['løper_to_navninput']
	løper_en_startinput = st.session_state['løper_en_startinput']
	løper_to_startinput = st.session_state['løper_to_startinput']

	antall_løpere = st.session_state.antall_løpere

	if st.session_state.antall_løpere >= 3:
		løper_tre_navninput = st.session_state['løper_tre_navninput']
		løper_tre_startinput = st.session_state['løper_tre_startinput']
	
	if st.session_state.antall_løpere >= 4:
		løper_fire_navninput = st.session_state['løper_fire_navninput']
		løper_fire_startinput = st.session_state['løper_fire_startinput']

	if st.session_state.antall_løpere >= 5:
		løper_fem_navninput = st.session_state['løper_fem_navninput']
		løper_fem_startinput = st.session_state['løper_fem_startinput']
	
	if st.session_state.antall_løpere == 6:
		løper_seks_navninput = st.session_state['løper_seks_navninput']
		løper_seks_startinput = st.session_state['løper_seks_startinput']

	def rekkefølge_feil(løperEn, løperTo, løperEnNavn, løperToNavn, løperEnStrNr, løperToStrNr):
		løper_en_str_nr = løperEnStrNr
		løper_to_str_nr = løperToStrNr
		løperEnStrNr = løper_to_str_nr
		løperToStrNr = løper_en_str_nr
		løper_en = løperEn
		løper_to = løperTo
		løperEn = løper_to
		løperTo = løper_en
		løper_enNavn = løperEnNavn
		løper_toNavn = løperToNavn
		løperEnNavn = løper_toNavn
		løperToNavn= løper_enNavn
		return løperEn, løperTo, løperEnNavn, løperToNavn, løperEnStrNr, løperToStrNr
	
	n = 1
	for i in range(antall_løpere):
		if n == 1:
			løper = "en"
			løper_start = regn_starttid(løper_en_startinput)
		elif n == 2:
			løper = "to"
			løper_start = regn_starttid(løper_to_startinput)
		elif n == 3:
			løper = "tre"
			løper_start = regn_starttid(løper_tre_startinput)
		elif n == 4:
			løper = "fire"
			løper_start = regn_starttid(løper_fire_startinput)
		elif n == 5:
			løper = "fem"
			løper_start = regn_starttid(løper_fem_startinput)
		elif n == 6:
			løper = "seks"
			løper_start = regn_starttid(løper_seks_startinput)
		st.session_state["løper_" + løper + "_start"] = løper_start
		st.write(løper, "hallo")
		st.session_state["løper_" + løper + "_start"]
		n += 1

	def rekkefølge_feil_en(en, to):
		if st.session_state["løper_" + en + "_start"] > st.session_state["løper_" + to + "_start"]:
			st.write(st.session_state['løper_' + to + '_navninput'])

			omregning = rekkefølge_feil(st.session_state["løper_" + en + "_start"], st.session_state["løper_" + to + "_start"], st.session_state["løper_" + en + "_navninput"], st.session_state["løper_" + to + "_navninput"], st.session_state['løper_' + en + '_startnr'], st.session_state['løper_' + to + '_startnr'])
			st.session_state["løper_" + en + "_start"] = omregning[0]
			st.session_state["løper_" + to + "_start"] = omregning[1]
			st.session_state['løper_' + en + '_navninput'] = omregning[2]
			st.session_state['løper_' + to + '_navninput'] = omregning[3]
			st.session_state['løper_' + en + '_startnr'] = omregning[4]
			st.session_state['løper_' + to + '_startnr'] = omregning[5]
			st.write(st.session_state['løper_' + to + '_navninput'])

	for i in range(5):
		rekkefølge_feil_en("en", "to")
		if antall_løpere > 2:
			rekkefølge_feil_en("en", "tre")
			rekkefølge_feil_en("to", "tre")
		if antall_løpere > 3:
			rekkefølge_feil_en("en", "fire")
			rekkefølge_feil_en("to", "fire")
			rekkefølge_feil_en("tre", "fire")
		if antall_løpere > 4:
			rekkefølge_feil_en("en", "fem")
			rekkefølge_feil_en("to", "fem")
			rekkefølge_feil_en("tre", "fem")
			rekkefølge_feil_en("fire", "fem")
		if antall_løpere > 5:
			rekkefølge_feil_en("en", "seks")
			rekkefølge_feil_en("to", "seks")
			rekkefølge_feil_en("tre", "seks")
			rekkefølge_feil_en("fire", "seks")
			rekkefølge_feil_en("fem", "seks")
	st.experimental_rerun()

def løper_passerer(løper_start_tid):
	løper_pa_tid= time.time()
	løper_tid = løper_pa_tid - løper_start_tid
	return (løper_tid)

def regn_forskjell(start_en, start_to):
	forskjell = start_to - start_en 
	return (forskjell)

def regn_negativ_positiv(forskjell):
	if forskjell < 0:
		bak_foran = ' foran '

	if forskjell == 0:
		bak_foran = ' foran '

	if forskjell > 0:
		bak_foran = ' bak '

	return(bak_foran)

def skriv_to_løpere(passering_løper_en, passering_løper_to, løper_en_navn, løper_to_navn):
	forskjell_på_en_to = regn_forskjell(passering_løper_en, passering_løper_to)

	forskjell_på_en_to = round(forskjell_på_en_to, 1)

	bak_foran = regn_negativ_positiv(forskjell_på_en_to)
	forskjell_på_en_to = abs(forskjell_på_en_to)

	st.session_state["passering_løper_to"] = passering_løper_to

	skriv = løper_to_navn + " er " + str(forskjell_på_en_to) + " sekunder" + bak_foran + løper_en_navn
	return skriv

if st.session_state["hvis_starttider"]:
	løper_en_navninput = st.session_state['løper_en_navninput']
	løper_to_navninput = st.session_state['løper_to_navninput']
	løper_en_startinput = st.session_state['løper_en_startinput']
	løper_to_startinput = st.session_state['løper_to_startinput']
	løper_en_startnr = st.session_state['løper_en_startnr']
	løper_to_startnr = st.session_state['løper_to_startnr']

	antall_løpere = st.session_state.antall_løpere
	if st.session_state.antall_løpere >= 3:
		løper_tre_navninput = st.session_state['løper_tre_navninput']
		løper_tre_startinput = st.session_state['løper_tre_startinput']
		løper_tre_startnr = st.session_state['løper_tre_startnr']
	
	if st.session_state.antall_løpere >= 4:
		løper_fire_navninput = st.session_state['løper_fire_navninput']
		løper_fire_startinput = st.session_state['løper_fire_startinput']
		løper_fire_startnr = st.session_state['løper_fire_startnr']

	if st.session_state.antall_løpere >= 5:
		løper_fem_navninput = st.session_state['løper_fem_navninput']
		løper_fem_startinput = st.session_state['løper_fem_startinput']
		løper_fem_startnr = st.session_state['løper_fem_startnr']
	
	if st.session_state.antall_løpere == 6:
		løper_seks_navninput = st.session_state['løper_seks_navninput']
		løper_seks_startinput = st.session_state['løper_seks_startinput']
		løper_seks_startnr = st.session_state['løper_seks_startnr']

	
	tab3 = st.empty()

	if st.session_state["antall_løpere"] >= 3:
		løper_tre_navninput = st.session_state['løper_tre_navninput']
	
	if st.session_state.antall_løpere >= 4:
		løper_fire_navninput = st.session_state['løper_fire_navninput']

	if st.session_state.antall_løpere >= 5:
		løper_fem_navninput = st.session_state['løper_fem_navninput']
	
	if st.session_state.antall_løpere == 6:
		løper_seks_navninput = st.session_state['løper_seks_navninput']

	tab1, tab2, tab3, tab4  = st.tabs(["Sekundering", "Logg", "Startliste", "Link resultater"])
	with tab4:
		st.write("Her er link til resultatlista:")
		st.write("https://live.eqtiming.com/" + str(st.session_state["løpe_id"]) + "#result")

	if "antall_passeringer" not in st.session_state:
		st.session_state["antall_passeringer"] =  0
		antall_passeringer = 0
		

	with tab1:
		data_log = pd.DataFrame(columns=["Passering", "Løper", "Forskjellen(sekunder)", "Hvem er han foran/bak"])

		st.header("Sekundering")
		st.write('Trykk på navnet til løperen som passerer:')

		antall_løpere = st.session_state.antall_løpere
		if 'lapping_for_en' not in st.session_state:
			st.session_state["lapping_for_en"] = 0
			st.session_state["lapping_for_to"] = 0
			st.session_state["lapping_for_tre"] = 0
			st.session_state["lapping_for_fire"] = 0
			st.session_state["lapping_for_fem"] = 0
			st.session_state["lapping_for_seks"] = 0
			st.session_state["data_log"] = []
			st.session_state["data_log_col"] = data_log

		data_log = pd.DataFrame(columns=["Navn", "Startnummer", "Passeringstid", "Starttid", "Tid brukt", "Tid bak"])
					
		if antall_løpere > 1:
			st.write('')
			løper_en_knapp = st.button(løper_en_startnr + " " + løper_en_navninput)
			if løper_en_knapp:
				st.session_state["lapping_for_en"] += 1
				st.session_state["siste_passering_løper_en"] = løper_passerer(st.session_state["løper_en_start"])
				a = 1
				n = 1
				for i in range(5):
					if n == 1:
						løper = "to"
					elif n == 2:
						løper = "tre"
					elif n == 3:
						løper = "fire"
					elif n == 4:
						løper = "fem"
					elif n == 5:
						løper = "seks"

					if st.session_state["lapping_for_" + løper] == st.session_state["lapping_for_en"]:
						st.write(skriv_to_løpere(st.session_state["siste_passering_løper_" + løper], st.session_state["siste_passering_løper_en"], st.session_state["løper_" + løper + "_navninput"], st.session_state["løper_en_navninput"]))
						a += 1
					n += 1
				if a == 1:
					st.write(st.session_state["løper_en_navninput"] + " har passert")


				passerings_logg = str(st.session_state["lapping_for_en"]) + "logg"

				if passerings_logg not in st.session_state:
					st.session_state[passerings_logg] = data_log
				t = time.localtime()

				current_time = time.strftime("%H:%M:%S", t)

				tid_minus_start = time.time() - st.session_state["løper_en_start"] 
				starttid = st.session_state["løper_en_startinput"]
				starttid_sekunder = regn_starttid(str(current_time)) - regn_starttid(str(st.session_state["løper_en_startinput"]))
				starttid_sekunder_formatert = regn_fra_sekk_til_min(starttid_sekunder)
				df = pd.DataFrame({"Navn": [løper_en_navninput], 
					"Startnummer": [løper_en_startnr], 
					"Tid bak": ["ikke regnet ut enda"],
					"Passeringstid": [current_time],
					"Starttid": [starttid],
					"Tid brukt": [starttid_sekunder_formatert],
					'Tid brukt(sekunder)': [starttid_sekunder]},
					index= [""])

				df_2 = st.session_state[passerings_logg]

				st.session_state[passerings_logg] = pd.concat([df_2, df])

		if antall_løpere >= 2:
			st.write('')
			løper_to_knapp = st.button(løper_to_startnr + " " + løper_to_navninput)

			if løper_to_knapp:
				st.session_state["lapping_for_to"] += 1
				st.session_state["siste_passering_løper_to"] = løper_passerer(st.session_state["løper_to_start"])
				a = 1
				n = 1
				for i in range(5):
					if n == 1:
						løper = "en"
					elif n == 2:
						løper = "tre"
					elif n == 3:
						løper = "fire"
					elif n == 4:
						løper = "fem"
					elif n == 5:
						løper = "seks"

					if st.session_state["lapping_for_" + løper] == st.session_state["lapping_for_to"]:
						st.write(skriv_to_løpere(st.session_state["siste_passering_løper_" + løper], st.session_state["siste_passering_løper_to"], st.session_state["løper_" + løper + "_navninput"], st.session_state["løper_to_navninput"]))
						a += 1
					n += 1
				if a == 1:
					st.write(st.session_state["løper_to_navninput"] + " har passert")

				passerings_logg = str(st.session_state["lapping_for_to"]) + "logg"

				if passerings_logg not in st.session_state:
					st.session_state[passerings_logg] = data_log
				t = time.localtime()

				current_time = time.strftime("%H:%M:%S", t)

				tid_minus_start = time.time() - st.session_state["løper_to_start"] 
				starttid = st.session_state["løper_to_startinput"]
				starttid_sekunder = regn_starttid(str(current_time)) - regn_starttid(str(st.session_state["løper_to_startinput"]))

				df = pd.DataFrame({"Navn": [løper_to_navninput], 
					"Startnummer": [løper_to_startnr], 
					"Tid bak": ["ikke regnet ut enda"],
					"Passeringstid": [current_time],
					"Starttid": [starttid],
					"Tid brukt": [regn_fra_sekk_til_min(starttid_sekunder)],
					'Tid brukt(sekunder)': [starttid_sekunder]},
					index= [" "])

				df_2 = st.session_state[passerings_logg]

				st.session_state[passerings_logg] = pd.concat([df_2, df])
		if antall_løpere >= 3:
			
			st.write('')
			løper_tre_knapp = st.button(løper_tre_startnr + " " + løper_tre_navninput)

			if løper_tre_knapp:
				st.session_state["lapping_for_tre"] += 1
				st.session_state["siste_passering_løper_tre"] = løper_passerer(st.session_state["løper_tre_start"])
				a = 1
				n = 1
				for i in range(5):
					if n == 1:
						løper = "en"
					elif n == 2:
						løper = "to"
					elif n == 3:
						løper = "fire"
					elif n == 4:
						løper = "fem"
					elif n == 5:
						løper = "seks"

					if st.session_state["lapping_for_" + løper] == st.session_state["lapping_for_tre"]:
						st.write(skriv_to_løpere(st.session_state["siste_passering_løper_" + løper], st.session_state["siste_passering_løper_tre"], st.session_state["løper_" + løper + "_navninput"], st.session_state["løper_tre_navninput"]))
						a += 1
					n += 1
				if a == 1:
					st.write(st.session_state["løper_tre_navninput"] + " har passert")

				passerings_logg = str(st.session_state["lapping_for_tre"]) + "logg"

				if passerings_logg not in st.session_state:
					st.session_state[passerings_logg] = data_log
				t = time.localtime()

				current_time = time.strftime("%H:%M:%S", t)

				tid_minus_start = time.time() - st.session_state["løper_tre_start"] 
				starttid = st.session_state["løper_tre_startinput"]
				starttid_sekunder = regn_starttid(str(current_time)) - regn_starttid(str(st.session_state["løper_tre_startinput"]))

				df = pd.DataFrame({"Navn": [løper_tre_navninput], 
					"Startnummer": [løper_tre_startnr], 
					"Tid bak": ["ikke regnet ut enda"],
					"Passeringstid": [current_time],
					"Starttid": [starttid],
					"Tid brukt": [regn_fra_sekk_til_min(starttid_sekunder)],
					'Tid brukt(sekunder)': [starttid_sekunder]},
					index= [" "])

				df_2 = st.session_state[passerings_logg]

				st.session_state[passerings_logg] = pd.concat([df_2, df])


		if antall_løpere >= 4:
			st.write('')
			løper_fire_knapp = st.button(løper_fire_startnr + " " + løper_fire_navninput)

			if løper_fire_knapp:
				st.session_state["lapping_for_fire"] += 1

				st.session_state["siste_passering_løper_fire"] = løper_passerer(st.session_state["løper_fire_start"])
				a = 1
				n = 1
				for i in range(5):
					if n == 1:
						løper = "en"
					elif n == 2:
						løper = "to"
					elif n == 3:
						løper = "tre"
					elif n == 4:
						løper = "fem"
					elif n == 5:
						løper = "seks"

					if st.session_state["lapping_for_" + løper] == st.session_state["lapping_for_fire"]:
						st.write(skriv_to_løpere(st.session_state["siste_passering_løper_" + løper], st.session_state["siste_passering_løper_fire"], st.session_state["løper_" + løper + "_navninput"], st.session_state["løper_fire_navninput"]))
						a += 1
					n += 1
				if a == 1:
					st.write(st.session_state["løper_fire_navninput"] + " har passert")


				passerings_logg = str(st.session_state["lapping_for_fire"]) + "logg"

				if passerings_logg not in st.session_state:
					st.session_state[passerings_logg] = data_log
				t = time.localtime()

				current_time = time.strftime("%H:%M:%S", t)

				tid_minus_start = time.time() - st.session_state["løper_fire_start"] 
				starttid = st.session_state["løper_fire_startinput"]
				starttid_sekunder = regn_starttid(str(current_time)) - regn_starttid(str(st.session_state["løper_fire_startinput"]))

				df = pd.DataFrame({"Navn": [løper_fire_navninput], 
					"Startnummer": [løper_fire_startnr], 
					"Tid bak": ["ikke regnet ut enda"],
					"Passeringstid": [current_time],
					"Starttid": [starttid],
					"Tid brukt": [regn_fra_sekk_til_min(starttid_sekunder)],
					'Tid brukt(sekunder)': [starttid_sekunder]},
					index= [" "])

				df_2 = st.session_state[passerings_logg]

				st.session_state[passerings_logg] = pd.concat([df_2, df])

		if antall_løpere >= 5:
			st.write('')
			løper_fem_knapp = st.button(løper_fem_startnr + " " + løper_fem_navninput)

			if løper_fem_knapp:
				st.session_state["lapping_for_fem"] += 1
				st.session_state["siste_passering_løper_fem"] = løper_passerer(st.session_state["løper_fem_start"])
				
				a = 1
				n = 1
				for i in range(5):
					if n == 1:
						løper = "en"
					elif n == 2:
						løper = "to"
					elif n == 3:
						løper = "tre"
					elif n == 4:
						løper = "fire"
					elif n == 5:
						løper = "seks"

					if st.session_state["lapping_for_" + løper] == st.session_state["lapping_for_fem"]:
						st.write(skriv_to_løpere(st.session_state["siste_passering_løper_" + løper], st.session_state["siste_passering_løper_fem"], st.session_state["løper_" + løper + "_navninput"], st.session_state["løper_fem_navninput"]))
						a += 1

					n += 1
				if a == 1:
					st.write(st.session_state["løper_fem_navninput"] + " har passert")

				passerings_logg = str(st.session_state["lapping_for_fem"]) + "logg"

				if passerings_logg not in st.session_state:
					st.session_state[passerings_logg] = data_log
				t = time.localtime()

				current_time = time.strftime("%H:%M:%S", t)

				tid_minus_start = time.time() - st.session_state["løper_fem_start"] 
				starttid = st.session_state["løper_fem_startinput"]
				starttid_sekunder = regn_starttid(str(current_time)) - regn_starttid(str(st.session_state["løper_fem_startinput"]))

				df = pd.DataFrame({"Navn": [løper_fem_navninput], 
					"Startnummer": [løper_fem_startnr], 
					"Tid bak": ["ikke regnet ut enda"],
					"Passeringstid": [current_time],
					"Starttid": [starttid],
					"Tid brukt": [regn_fra_sekk_til_min(starttid_sekunder)],
					'Tid brukt(sekunder)': [starttid_sekunder]},
					index= [" "])

				df_2 = st.session_state[passerings_logg]

				st.session_state[passerings_logg] = pd.concat([df_2, df])

		if antall_løpere >= 6:
			st.write('')
			løper_seks_knapp = st.button(løper_seks_startnr + " " + løper_seks_navninput)

			if løper_seks_knapp:
				st.session_state["lapping_for_seks"] += 1
				st.session_state["siste_passering_løper_seks"] = løper_passerer(st.session_state["løper_seks_start"])
				
				n = 1
				a = 1
				for i in range(5):
					if n == 1:
						løper = "en"
					elif n == 2:
						løper = "to"
					elif n == 3:
						løper = "tre"
					elif n == 4:
						løper = "fire"
					elif n == 5:
						løper = "fem"

					if st.session_state["lapping_for_" + løper] == st.session_state["lapping_for_seks"]:
						st.write(skriv_to_løpere(st.session_state["siste_passering_løper_" + løper], st.session_state["siste_passering_løper_seks"], st.session_state["løper_" + løper + "_navninput"], st.session_state["løper_seks_navninput"]))
						a += 1
					n += 1
				if a == 1:
					st.write(st.session_state["løper_seks_navninput"] + " har passert")

				passerings_logg = str(st.session_state["lapping_for_seks"]) + "logg"

				if passerings_logg not in st.session_state:
					st.session_state[passerings_logg] = data_log
				t = time.localtime()

				current_time = time.strftime("%H:%M:%S", t)

				tid_minus_start = time.time() - st.session_state["løper_seks_start"] 
				starttid = st.session_state["løper_seks_startinput"]
				starttid_sekunder = regn_starttid(str(current_time)) - regn_starttid(str(st.session_state["løper_seks_startinput"]))

				df = pd.DataFrame({"Navn": [løper_seks_navninput], 
					"Startnummer": [løper_seks_startnr], 
					"Tid bak": ["ikke regnet ut enda"],
					"Passeringstid": [current_time],
					"Starttid": [starttid],
					"Tid brukt": [regn_fra_sekk_til_min(starttid_sekunder)],
					'Tid brukt(sekunder)': [starttid_sekunder]},
					index= [" "])

				df_2 = st.session_state[passerings_logg]

				st.session_state[passerings_logg] = pd.concat([df_2, df])

	with tab2:
		løper_en_navninput = st.session_state['løper_en_navninput']
		løper_to_navninput = st.session_state['løper_to_navninput']
		løper_en_startinput = st.session_state['løper_en_startinput']
		løper_to_startinput = st.session_state['løper_to_startinput']
		antall_løpere = st.session_state.antall_løpere

		if st.session_state.antall_løpere >= 3:
			løper_tre_navninput = st.session_state['løper_tre_navninput']
			løper_tre_startinput = st.session_state['løper_tre_startinput']
		
		if st.session_state.antall_løpere >= 4:
			løper_fire_navninput = st.session_state['løper_fire_navninput']
			løper_fire_startinput = st.session_state['løper_fire_startinput']

		if st.session_state.antall_løpere >= 5:
			løper_fem_navninput = st.session_state['løper_fem_navninput']
			løper_fem_startinput = st.session_state['løper_fem_startinput']
		
		if st.session_state.antall_løpere == 6:
			løper_seks_navninput = st.session_state['løper_seks_navninput']
			løper_seks_startinput = st.session_state['løper_seks_startinput']


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

	with tab3:
		klasser_dict_to = st.session_state["klasser_dict_to"]
		klasse_som_sekunderes = st.selectbox('Velg hvilken klasse du vil se', klasser_dict_to)

		if klasse_som_sekunderes != 'Velg klasse her':
			df = st.session_state[klasse_som_sekunderes + '.csv']
			st.dataframe(df)
	
	with tab2:
		st.header("Logg")
		st.subheader('Sekunderingstider:')
		st.write("Starttid, passeringstid og tid brukt er i timer minutter sekunder.")
		n = 1

		for i in range(50):
			logg = str(n) + "logg"
			if logg in st.session_state:
				st.write(("Passering " + str(n)  + ":"))
				df = st.session_state[logg]
				df.sort_values(by='Tid brukt(sekunder)', ascending=True, inplace=True)
				
				if st.session_state["lapping_for_to"] >= n:
					try:
						value_0 = df.iloc[0, 6]
						df.iloc[0, 5] = "0"
						value_1 = df.iloc[1, 6]
						value_1 = value_1 - value_0
						df.iloc[1, 5] = value_1
						index_liste = [1, 2]
					except:
						mongo = "mongo"

				if antall_løpere > 2:
					if st.session_state["lapping_for_tre"] >= n:
						try:
							value_2 = df.iloc[2, 6]
							value_2 = value_2 - value_0
							df.iloc[2, 5] = value_2
							index_liste = [1, 2, 3]
						except:
							mongo = "mongo"

				if antall_løpere > 3:
					if st.session_state["lapping_for_fire"] >= n:
						try:
							value_3 = df.iloc[3, 6]
							value_3 = value_3 - value_0
							df.iloc[3, 5] = value_3
							index_liste = [1, 2, 3, 4]
						except:
							mongo = "mongo"

				if antall_løpere > 4:
					if st.session_state["lapping_for_fem"] >= n:
						try:
							value_4 = df.iloc[4, 6]
							value_4 = value_4 - value_0
							df.iloc[4, 5] = value_4
							index_liste = [1, 2, 3, 4, 5]
						except:
							mongo = "mongo"

				if antall_løpere > 5:
					if st.session_state["lapping_for_seks"] >= n:
						try:
							value_5 = df.iloc[5, 6]
							value_5 = value_5 - value_0
							df.iloc[5, 5] = value_5
							index_liste = [1, 2, 3, 4, 5, 6]
						except:
							mongo = "mongo"
				if st.session_state["lapping_for_to"] >= n:
					try:
						df.index = index_liste
					except:
						mongo = "mongo"
					st.dataframe(df)

			else:
				break
			n += 1
