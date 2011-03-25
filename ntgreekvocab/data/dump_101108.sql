--
-- PostgreSQL database dump
--

-- Started on 2010-11-08 23:30:55

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 1928 (class 0 OID 0)
-- Dependencies: 1641
-- Name: ntgreekvocab_simplecard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leehsueh_appsv1
--

SELECT pg_catalog.setval('ntgreekvocab_simplecard_id_seq', 182, true);


--
-- TOC entry 1925 (class 0 OID 125420)
-- Dependencies: 1642
-- Data for Name: ntgreekvocab_simplecard; Type: TABLE DATA; Schema: public; Owner: leehsueh_appsv1
--

COPY ntgreekvocab_simplecard (id, greek_word, part_of_speech, definition, parsing_info, notes, lesson_number) FROM stdin;
1	βλέπω	v	I see	present, active, indicative, 1st person, singular		3
2	γινώσκω	v	I know	present, active, indicative, 1st person, singular		3
3	γράφω	v	I write	present, active, indicative, 1st person, singular		3
4	διδάσκω	v	I teach	present, active, indicative, 1st person, singular		3
5	ἔχω	v	I have	present, active, indicative, 1st person, singular		3
6	λαμβάνω	v	I take, I receive	present, active, indicative, 1st person, singular		3
7	λέγω	v	I say	present, active, indicative, 1st person, singular		3
8	λύω	v	I loose, I destroy	present, active, indicative, 1st person, singular		3
9	ἁδελφός	n	a brother	masculine, singular, nominative		4
10	ἄνθρωπος	n	a man, a person	masculine, singular, nominative	plural form: men, people	4
11	ἀπόστολος	n	an apostle	masculine, singular, nominative		4
12	δοῦλος	n	a slave, a servant	masculine, singular, nominative		4
13	δῶρον	n	a gift	neuter, singular, nominative		4
14	θάνατος	n	a death	masculine, singular, nominative		4
15	ἱερόν	n	a temple	neuter, singular, nominative		4
16	καί	conj	and			4
17	λόγος	n	a word	masculine, singular, nominative		4
18	νόμος	n	a law	masculine, singular, nominative		4
19	οἶκος	n	a house	masculine, singular, nominative		4
20	υἱός	n	a son	masculine, singular, nominative		4
21	ἀλήθεια	n	truth	feminine, singular, nominative		5
22	βασιλεία	n	a kingdom	feminine, singular, nominative		5
23	γραφή	n	a writing, a Scripture	feminine, singular, nominative		5
24	δόξα	n	glory	feminine, singular, nominative		5
25	ἔἱρήνη	n	peace	feminine, singular, nominative		5
26	ἐκκλησία	n	a church	feminine, singular, nominative		5
27	ἐντολή	n	a commandment	feminine, singular, nominative		5
28	ζωή	n	life	feminine, singular, nominative		5
29	ἡμέρα	n	a day	feminine, singular, nominative		5
30	καρδία	n	a heart	feminine, singular, nominative		5
31	παραβολή	n	a parable	feminine, singular, nominative		5
32	φωνή	n	a voice	feminine, singular, nominative		5
33	ψυχή	n	a soul, a life	feminine, singular, nominative		5
34	ὡρα	n	an hour	feminine, singular, nominative		5
35	ἀγαθός, -ή, -όν	adj	good	singular, nominative		6
36	ἄλλος, -η, -ο	adj	other	singular, nominative		6
37	δίκαιος, -α, -ον	adj	righteous	singular, nominative		6
38	ἐγείρω	v	I raise up	present, active, indicative, 1st person, singular		6
39	ἔρημος	n	a desert	feminine, singular, nominative		6
40	ἔσχατος, -η, -ον	adj	last	singular, nominative		6
41	κακός, -ή, -όν	adj	bad	singular, nominative		6
42	καλός, -ή, -όν	adj	good, beautiful	singular, nominative		6
43	κύριος	n	a lord, the Lord	masculine, singular, nominative		6
44	μικρός, -ά, -όν	adj	little, small	singular, nominative		6
45	νεκρός, -ά, -όν	adj	dead	singular, nominative		6
46	ὁδός	n	a road, a way	feminine, singular, nominative		6
47	πιστός, -ή, -όν	adj	faithful	singular, nominative		6
48	πρῶτος, -ή, -όν	adj	first	singular, nominative		6
49	ἄγγελος	n	an angel, a messenger	masculine, singular, nominative		7
50	ἄγω	v	I lead	present, active, indicative, 1st person, singular		7
51	ἀπό	prep	with genitive, from			7
52	βάλλω	v	I throw, I cast, I put	present, active, indicative, 1st person, singular		7
53	διά	prep	with gen., through; with acc., on account of			7
54	εἱς	prep	with acc., into		when used with an articular infinitive, often expresses purpose (e.g. in order to _).	7
55	ἐκ	prep	with gen., out of		ἐξ before vowels	7
56	ἐν	prep	with dat., in			7
57	θεός	n	a god, God	masculine, singular, nominative		7
58	κόσμος	n	a world	masculine, singular, nominative		7
59	λίθος	n	a stone	masculine, singular, nominative		7
60	μαθητής	n	a disciple	masculine, singular, nominative		7
61	μένω	v	I remain	present, active, indicative, 1st person, singular		7
62	μετά	prep	with gen., with; with acc., after			7
63	οὐρανός	n	heaven	masculine, singular, nominative		7
64	πέμπω	v	I send	present, active, indicative, 1st person, singular		7
65	πρός	prep	with acc., to, toward, in the presence of			7
66	προφήτης	n	a prophet	masculine, singular, nominative		7
67	τέκνον	n	a child	neuter, singular, nominative		7
68	τόπος	n	a place	masculine, singular, nominative		7
69	φέρω	v	I bear, I bring	present, active, indicative, 1st person, singular		7
70	αὐτός, -ή, -ό	pn	he, she, it	3rd person, singular, nominative		8
71	δέ	conj	but (light), and		postpositive	8
72	ἐγώ	pn	I	1st person, singular nominative		8
73	εἰμί	v	I am	present, active, indicative, 1st person, singular		8
74	ἡμεῖς	pn	we	1st person, plural, nominative		8
75	σύ	pn	you (singular)	2nd person, singular, nominative		8
76	ὑμεῖς	pn	you (plural)	2nd person, plural, nominative		8
77	ἐμοῦ, μου	pn	of me, my	1st person, singular, genitive		8
78	ἐμοί, μοι	pn	to or for me	1st person, singular, dative		8
79	ἐμέ, με	pn	me	1st person, singular, accusative		8
80	σοῦ	pn	of you, your (singular)	2nd person, singular, genitive		8
81	σοί	pn	to or for you (singular)	2nd person, singular, dative		8
82	σέ	pn	you (direct object, singular)	2nd person, singular, accusative		8
83	 ἀγάπη	n	love	feminine, singular, nominative		9
84	ἁμαρτία	n	a sin, sin	feminine, singular, nominative		9
85	βαπτίζω	v	I baptize	present, active, indicative, 1st person, singular		9
86	διδάσκαλος	n	a teacher	masculine, singular, nominative		9
87	ἐκεῖνος, -η, -ο	pn	that (demonstrative)	singular, nominative		9
88	ἐπαγγελία	n	a promise	feminine, singular, nominative		9
89	εὐαγγέλιον	n	a gospel	neuter, singular, nominative		9
90	κρίνω	v	I judge	present, active, indicative, 1st person, singular		9
91	νῦν	adv	now			9
92	οὗτος, αὕτη, τοῦτο	pn	this	singular, nominative		9
93	οὕτως	adv	thus, so		not to be confused with οὗτος	9
94	πονηρός, -ά, -όν	adj	evil	singular, nominative		9
95	πρόσωπον	n	a face	neuter, singular, nominative		9
96	χαρά	n	joy	feminine, singular, nominative		9
97	ἀκούω	v	I hear	present, active, indicative, 1st person, singular		10
98	ἀλλά	conj	but (stronger than δέ)			10
99	ἁμαρτωλός	n	a sinner	masculine, singular, nominative		10
100	ἀποκρίνομαι	v	I answer	present, middle/passive, indicative, 1st person, singular	deponent, takes the dative	10
101	ἄρχω	v	I rule (takes genitive)	present, active, indicative, 1st person, singular	middle form, I begin	10
102	γίνομαι	v	I become	present, middle/passive, indicative, 1st person, singular	deponent; takes a predicate nominative, not an accusative	10
103	διέρχομαι	v	I go through	present, middle/passive, indicative, 1st person, singular	deponent	10
104	εἰσέρχομαι	v	I go in, I enter	present, middle/passive, indicative, 1st person, singular	deponent	10
105	ἐξέρχομαι	v	I go out	present, middle/passive, indicative, 1st person, singular	deponent	10
106	ἔρχομαι	v	I come, I go	present, middle/passive, indicative, 1st person, singular	deponent	10
107	ὅτι	conj	that, because			10
108	οὐ	adv	not		οὐκ before vowels, οἰχ before the rough breathing. proclitic.	10
109	πορεύομαι	v	I go	present, middle/passive, indicative, 1st person, singular	deponent	10
110	σώζω	v	I save	present, active, indicative, 1st person, singular		10
111	ὑπό	prep	with gen., by (expressing agent); with acc., under			10
112	αἴρω	v	I take up, I take away	present, active, indicative, 1st person, singular		11
113	ἀναβαίνω	v	I go up	present, active, indicative, 1st person, singular	ἀνα means up	11
114	ἀποθνήσκω	v	I die	present, active, indicative, 1st person, singular		11
115	ἀποκτείνω	v	I kill	present, active, indicative, 1st person, singular		11
116	ἁποστέλλω	v	I send (with commission)	present, active, indicative, 1st person, singular		11
117	ἄρτος	n	a piece of bread, a loaf, a bread	masculine, singular, nominative		11
118	βαίνω	v	I go	present, active, indicative, 1st person, singular	This verb by itself does not occur in the NT, but compound forms with prepositions are very common	11
119	ἐσθίω	v	I eat	present, active, indicative, 1st person, singular		11
120	κατά	prep	with gen., against; with acc., according to		original meaning was down, but has many meanings in the NT	11
121	καταβαίνω	v	I go down	present, active, indicative, 1st person, singular		11
122	μέν...δέ	construct	on the one hand...on the other		Used in contrasts, the μέν is often best left untranslated and the δέ then best translated by :but:	11
123	οὐκέτι	adv	no longer			11
124	παρά	prep	with gen., from; with dat., beside, in the presence of; with acc., alongside of			11
125	παραλαμβάνω	v	I receive, I take along	present, active, indicative, 1st person, singular		11
126	σύν	prep	with dat., with		close synonym with μετά with the gen.	11
127	συνάγω	v	I gather together	present, active, indicative, 1st person, singular		11
128	τότε	adv	then			11
129	ἀπέρχομαι	v	I go away	present, middle/passive, indicative, 1st person, singular	deponent	12
130	βιβλίον	n	a book	neuter, singular, nominative/accusative		12
131	δαιμόνιον	n	a demon	neuter, singular, nominative/accusative		12
132	δέχομαι	v	I receive	present, middle/passive, indicative, 1st person, singular	deponent	12
133	έκπορεύομαι	v	I go out	present, middle/passive, indicative, 1st person, singular	deponent	12
134	ἔργον	n	a work	neuter, singular, nominative/accusative		12
135	ἔτι	adv	still, yet			12
136	θάλασσα	n	a lake, a sea	feminine, singular, nominative		12
137	καί...καί	construct	both...and			12
138	κατέρχομαι	v	I go down	present, middle/passive, indicative, 1st person, singular	deponent	12
139	οὑδέ	conj	and not, nor, not even			12
140	οὑδέ...οὐδέ	construct	neither...nor			12
141	ὑπέρ	prep	with gen., in behalf of; with acc., above			12
142	οῦπω	adv	not yet			12
143	περί	prep	with gen., concerning, about; with acc., around			12
144	πλοῖον	n	a boat	neuter, singular, nominative/accusative		12
145	συνέρχομαι	v	I come together	present, middle/passive, indicative, 1st person, singular	deponent	12
146	ἀναβλέπω	v	I look up, I receive my sight	present, active, indicative, 1st person singular		13
147	ἁναβλέψω	v	I will look up, I will receive my sight	future, active, indicative, 1st person singular		13
148	βήσομαι	v	I will go	future, middle, indicative, 1st person singular	future deponent	13
149	γενήσομαι	v	I will become	future, middle, indicative, 1st person, singular	deponent	13
150	γνώσομαι	v	I will know	future, middle, indicative, 1st person, singular	future deponent	13
151	διδάξω	v	I will teach	future, active, indicative, 1st person singular		13
152	διώκω	v	I pursue, I persecute	present, active, indicative, 1st person singular		13
153	διώξω	v	I will pursue, I will persecute	future, active, indicative, 1st person singular		13
154	δοξάζω	v	I glorify	present, active, indicative, 1st person singular		13
155	δοξάσω	v	I will glorify	future, active, indicative, 1st person singular		13
156	ἐλεύσομαι	v	I will come, I will go	future, middle, indicative, 1st person, singular	deponent	13
157	ἕξω	v	I will have	future, active, indicative, 1st person singular	note the rough breathing	13
158	κηρύσσω	v	I proclaim, I preach	present, active, indicative, 1st person singular		13
159	κηρύξω	v	I will proclaim, I will preach	future, active, indicative, 1st person singular		13
160	λήμψομαι	v	I will take, I will receive	future, middle, indicative, 1st person, singular	future deponent	13
161	προσεύχομαι	v	I pray	present, middle/passive, indicative, 1st person, singular	deponent	13
162	προσεύξομαι	v	I will pray	future, middle, indicative, 1st person, singular	deponent	13
163	τυφλός	n	a blind man	masculine, singular, nominative		13
164	δεῖ	v	it is necessary	present, active, indicative, 3rd person, singular	impersonal verb used only in the 3rd person; almost always used with an infinitive subject.	22
165	ἔξεστι(ν)	v	it is lawful, it is permitted	present, active, indicative, 3rd person, singular	impersonal verb used only in the 3rd person; almost always used with an infinitive subject.	22
166	θέλω	v	I wish	present, active, indicative, 1st person, singular		22
167	Ἰηυδαῖος	n	a Jew	masculine, singular, nominative		22
168	κελεύω	v	I command	present, active, indicative, 1st person, singular		22
169	κώμη	n	a village	feminine, singular, nominative		22
170	μέλλω	v	I am about (to do something), I am going (to do something)	present, active, indicative, 1st person, singular		22
171	ὀφείλω	v	I owe, I ought	present, active, indicative, 1st person, singular		22
172	πάσχω	v	I suffer	present, active, indicative, 1st person, singular		22
173	πρό	prep	with gen., before			22
174	σώτηρία	n	salvation	feminine, singular, nominative		22
175	Φαρισαῖος	n	a Pharisee	masculine, singular, nominative		22
176	Χριστός	n	Christ, the Messiah	masculine, singular, nominative		22
177	λύειν	v	to loose	present, active, infinitive		22
178	λύεσθαι	v	to loose for one's self (middle), to be loosed (passive)	present, middle/passive, infinitive		22
179	λῦσαι	v	to loose	1st aorist, active, infinitive		22
180	λύσασθαι	v	to loose for one's self	1st aorist, middle, infinitive		22
181	λυθῆναι	v	to be loosed	1st aorist, passive, infinitive		22
182	εἶναι	v	to be		εἰμί only one infinitive form	22
\.


-- Completed on 2010-11-08 23:30:56

--
-- PostgreSQL database dump complete
--

