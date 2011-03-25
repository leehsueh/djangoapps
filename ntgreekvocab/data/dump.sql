--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: ntgreekvocab_simplecard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leehsueh_appsv1
--

SELECT pg_catalog.setval('ntgreekvocab_simplecard_id_seq', 229, true);


--
-- Data for Name: ntgreekvocab_simplecard; Type: TABLE DATA; Schema: public; Owner: leehsueh_appsv1
--

COPY ntgreekvocab_simplecard (id, greek_word, part_of_speech, definition, parsing_info, notes, lesson_number) FROM stdin;
85	βλέπω	v	I see	present, active, indicative, 1st person, singular		3
86	γινώσκω	v	I know	present, active, indicative, 1st person, singular		3
87	γράφω	v	I write	present, active, indicative, 1st person, singular		3
88	διδάσκω	v	I teach	present, active, indicative, 1st person, singular		3
89	ἔχω	v	I have	present, active, indicative, 1st person, singular		3
90	λαμβάνω	v	I take, I receive	present, active, indicative, 1st person, singular		3
91	λέγω	v	I say	present, active, indicative, 1st person, singular		3
92	λύω	v	I loose, I destroy	present, active, indicative, 1st person, singular		3
93	ἁδελφός	n	a brother	masculine, singular, nominative		4
94	ἄνθρωπος	n	a man, a person	masculine, singular, nominative	plural form: men, people	4
95	ἀποστολος	n	an apostle	masculine, singular, nominative		4
96	δοῦλος	n	a slave, a servant	masculine, singular, nominative		4
97	δῶρον	n	a gift	neuter, singular, nominative		4
98	θάνατος	n	a death	masculine, singular, nominative		4
99	ἱερόν	n	a temple	neuter, singular, nominative		4
100	καί	conj	and			4
101	λόγος	n	a word	masculine, singular, nominative		4
102	νόμος	n	a law	masculine, singular, nominative		4
103	οἶκος	n	a house	masculine, singular, nominative		4
104	υἱός	n	a son	masculine, singular, nominative		4
105	ἀλήθεια	n	truth	feminine, singular, nominative		5
106	βασιλεία	n	a kingdom	feminine, singular, nominative		5
107	γραφή	n	a writing, a Scripture	feminine, singular, nominative		5
108	δόξα	n	glory	feminine, singular, nominative		5
109	ἔἱρήνη	n	peace	feminine, singular, nominative		5
110	ἐκκλησία	n	a church	feminine, singular, nominative		5
111	ἐντολή	n	a commandment	feminine, singular, nominative		5
112	ζωή	n	life	feminine, singular, nominative		5
113	ἡμέρα	n	a day	feminine, singular, nominative		5
114	καρδία	n	a heart	feminine, singular, nominative		5
115	παραβολή	n	a parable	feminine, singular, nominative		5
116	φωνή	n	a voice	feminine, singular, nominative		5
117	ψυχή	n	a soul, a life	feminine, singular, nominative		5
118	ὡρα	n	an hour	feminine, singular, nominative		5
119	ἀγαθος, -ή, -όν	adj	good	singular, nominative		6
120	ἄλλος, -η, -ο	adj	other	singular, nominative		6
121	δίκαιος, -α, -ον	adj	righteous	singular, nominative		6
122	ἐγείρω	v	I raise up	present, active, indicative, 1st person, singular		6
123	ἔρημος	n	a desert	feminine, singular, nominative		6
124	ἔσχατος, -η, -ον	adj	last	singular, nominative		6
125	κακός, -ή, -όν	adj	bad	singular, nominative		6
126	καλός, -ή, -όν	adj	good, beautiful	singular, nominative		6
127	κύριος	n	a lord, the Lord	masculine, singular, nominative		6
128	μικρός, -ά, -όν	adj	little, small	singular, nominative		6
129	νεκρός, -ά, -όν	adj	dead	singular, nominative		6
130	ὁδός	n	a road, a way	feminine, singular, nominative		6
131	πιστός, -ή, -όν	adj	faithful	singular, nominative		6
132	πρῶτος, -ή, -όν	adj	first	singular, nominative		6
133	ἄγγελος	n	an angel, a messenger	masculine, singular, nominative		7
134	ἄγω	v	I lead	present, active, indicative, 1st person, singular		7
135	ἀπό	prep	with genitive, from			7
136	βάλλω	v	I throw, I cast, I put	present, active, indicative, 1st person, singular		7
137	διά	prep	with gen., through; with acc., on account of			7
138	εἱς	prep	with acc., into			7
139	ἐκ	prep	with gen., out of		ἐξ before vowels	7
140	ἐν	prep	with dat., in			7
141	θεός	n	a god, God	masculine, singular, nominative		7
142	κόσμος	n	a world	masculine, singular, nominative		7
143	λίθος	n	a stone	masculine, singular, nominative		7
144	μαθητής	n	a disciple	masculine, singular, nominative		7
145	μένω	v	I remain	present, active, indicative, 1st person, singular		7
146	μετά	prep	with gen., with; with acc., after			7
147	οὐρανός	n	heaven	masculine, singular, nominative		7
148	πέμπω	v	I send	present, active, indicative, 1st person, singular		7
149	πρός	prep	with acc., to, toward, in the presence of			7
150	προφήτης	n	a prophet	masculine, singular, nominative		7
151	τέκνον	n	a child	neuter, singular, nominative		7
152	τόπος	n	a place	masculine, singular, nominative		7
153	φέρω	v	I bear, I bring	present, active, indicative, 1st person, singular		7
154	αὐτός, -ή, -ό	pn	he, she, it	3rd person, singular, nominative		8
155	δέ	conj	but (light), and		postpositive	8
156	ἐγώ	pn	I	1st person, singular nominative		8
157	εἰμί	v	I am	present, active, indicative, 1st person, singular		8
158	ἡμεῖς	pn	we	1st person, plural, nominative		8
159	σύ	pn	you (singular)	2nd person, singular, nominative		8
160	ὑμεῖς	pn	you (plural)	2nd person, plural, nominative		8
161	ἐμοῦ, μου	pn	of me, my	1st person, singular, genitive		8
162	ἐμοί, μοι	pn	to or for me	1st person, singular, dative		8
163	ἐμέ, με	pn	me	1st person, singular, accusative		8
164	σοῦ	pn	of you, your (singular)	2nd person, singular, genitive		8
165	σοί	pn	to or for you (singular)	2nd person, singular, dative		8
166	σέ	pn	you (direct object, singular)	2nd person, singular, accusative		8
167	 ἀγάπη	n	love	feminine, singular, nominative		9
168	ἁμαρτία	n	a sin, sin	feminine, singular, nominative		9
169	βαπτίζω	v	I baptize	present, active, indicative, 1st person, singular		9
170	διδάσκαλος	n	a teacher	masculine, singular, nominative		9
171	ἐκεῖνος, -η, -ο	pn	that (demonstrative)	singular, nominative		9
172	ἐπαγγελία	n	a promise	feminine, singular, nominative		9
173	εὐαγγέλιον	n	a gospel	neuter, singular, nominative		9
174	κρίνω	v	I judge	present, active, indicative, 1st person, singular		9
175	νῦν	adv	now			9
176	οὗτος, αὕτη, τοῦτο	pn	this	singular, nominative		9
177	οὕτως	adv	thus, so			9
178	πονηρός, -ά, -όν	adj	evil	singular, nominative		9
179	πρόσωπον	n	a face	neuter, singular, nominative		9
180	χαρά	n	joy	feminine, singular, nominative		9
181	ἀκούω	v	I hear	present, active, indicative, 1st person, singular		10
182	ἀλλά	conj	but (stronger than δέ)			10
183	ἁμαρτωλός	n	a sinner	masculine, singular, nominative		10
184	ἀποκρίνομαι	v	I answer	present, middle/passive, indicative, 1st person, singular	deponent, takes the dative	10
185	ἄρχω	v	I rule (takes genitive)	present, active, indicative, 1st person, singular	middle form, I begin	10
186	γίνομαι	v	I become	present, middle/passive, indicative, 1st person, singular	deponent; takes a predicate nominative, not an accusative	10
187	διέρχομαι	v	I go through	present, middle/passive, indicative, 1st person, singular	deponent	10
188	εἰσέρχομαι	v	I go in, I enter	present, middle/passive, indicative, 1st person, singular	deponent	10
189	ἐξέρχομαι	v	I go out	present, middle/passive, indicative, 1st person, singular	deponent	10
190	ἔρχομαι	v	I come, I go	present, middle/passive, indicative, 1st person, singular	deponent	10
191	ὅτι	conj	that, because			10
192	οὐ	adv	not		οὐκ before vowels, οἰχ before the rough breathing. proclitic.	10
193	πορεύομαι	v	I go	present, middle/passive, indicative, 1st person, singular	deponent	10
194	σώζω	v	I save	present, active, indicative, 1st person, singular		10
195	ὑπό	prep	with gen., by (expressing agent); with acc., under			10
196	αἴρω	v	I take up, I take away	present, active, indicative, 1st person, singular		11
197	ἀναβαίνω	v	I go up	present, active, indicative, 1st person, singular	ἀνα means up	11
198	ἀποθνήσκω	v	I die	present, active, indicative, 1st person, singular		11
199	ἀποκτείνω	v	I kill	present, active, indicative, 1st person, singular		11
200	ἁποστέλλω	v	I send (with commission)	present, active, indicative, 1st person, singular		11
201	ἄρτος	n	a piece of bread, a loaf, a bread	masculine, singular, nominative		11
202	βαίνω	v	I go	present, active, indicative, 1st person, singular	This verb by itself does not occur in the NT, but compound forms with prepositions are very common	11
203	ἐσθίω	v	I eat	present, active, indicative, 1st person, singular		11
204	καταβαίνω	v	with gen., against; with acc., according to	present, active, indicative, 1st person, singular	original meaning was down, but has many meanings in the NT	11
205	μέν...δέ	construct	on the one hand...on the other		Used in contrasts, the μέν is often best left untranslated and the δέ then best translated by :but:	11
206	οὐκέτι	adv	no longer			11
207	παρά	prep	with gen., from; with dat., beside, in the presence of; with acc., alongside of			11
208	παραλαμβάνω	v	I receive, I take along	present, active, indicative, 1st person, singular		11
209	σύ́ν	prep	with dat., with		close synonym with μετά with the gen.	11
210	συνάγω	v	I gather together	present, active, indicative, 1st person, singular		11
211	τότε	adv	then			11
212	ἀπέρχομαι	v	I go away	present, middle/passive, indicative, 1st person, singular	deponent	12
213	βιβλίον	n	a book	neuter, singular, nominative/accusative		12
214	δαιμόνιον	n	a demon	neuter, singular, nominative/accusative		12
215	δέχομαι	v	I receive	present, middle/passive, indicative, 1st person, singular	deponent	12
216	έκπορεύομαι	v	I go out	present, middle/passive, indicative, 1st person, singular	deponent	12
217	ἔργον	n	a work	neuter, singular, nominative/accusative		12
218	ἔτι	adv	still, yet			12
219	θάλασσα	n	a lake, a sea	feminine, singular, nominative		12
220	καί...καί	construct	both...and			12
221	κατέρχομαι	v	I go down	present, middle/passive, indicative, 1st person, singular	deponent	12
222	οὑδέ	conj	and not, nor, not even			12
223	οὑδέ...οὐδέ	construct	neither...nor			12
224	ὐπέρ	prep	with gen., in behalf of; with acc., above			12
225	οῦπω	adv	not yet			12
226	περί	prep	with gen., concerning, about; with acc., around			12
227	πλοῖον	n	a boat	neuter, singular, nominative/accusative		12
228	συνέρχομαι	v	I come together	present, middle/passive, indicative, 1st person, singular	deponent	12
229	τεστ	n				
\.


--
-- PostgreSQL database dump complete
--

