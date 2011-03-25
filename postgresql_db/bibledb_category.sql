--
-- PostgreSQL database dump
--

-- Started on 2009-12-13 00:35:32

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 1575 (class 1259 OID 24904)
-- Dependencies: 3
-- Name: bibledb_category; Type: TABLE; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

CREATE TABLE bibledb_category (
    id integer NOT NULL,
    category character varying(128) NOT NULL,
    parent_id integer,
    slug character varying(50) NOT NULL
);


ALTER TABLE public.bibledb_category OWNER TO leehsueh_appsv1;

--
-- TOC entry 1574 (class 1259 OID 24902)
-- Dependencies: 1575 3
-- Name: bibledb_category_id_seq; Type: SEQUENCE; Schema: public; Owner: leehsueh_appsv1
--

CREATE SEQUENCE bibledb_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.bibledb_category_id_seq OWNER TO leehsueh_appsv1;

--
-- TOC entry 1868 (class 0 OID 0)
-- Dependencies: 1574
-- Name: bibledb_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leehsueh_appsv1
--

ALTER SEQUENCE bibledb_category_id_seq OWNED BY bibledb_category.id;


--
-- TOC entry 1869 (class 0 OID 0)
-- Dependencies: 1574
-- Name: bibledb_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leehsueh_appsv1
--

SELECT pg_catalog.setval('bibledb_category_id_seq', 22, true);


--
-- TOC entry 1855 (class 2604 OID 24907)
-- Dependencies: 1575 1574 1575
-- Name: id; Type: DEFAULT; Schema: public; Owner: leehsueh_appsv1
--

ALTER TABLE bibledb_category ALTER COLUMN id SET DEFAULT nextval('bibledb_category_id_seq'::regclass);


--
-- TOC entry 1865 (class 0 OID 24904)
-- Dependencies: 1575
-- Data for Name: bibledb_category; Type: TABLE DATA; Schema: public; Owner: leehsueh_appsv1
--

COPY bibledb_category (id, category, parent_id, slug) FROM stdin;
1	Basic Beliefs	\N	basic-beliefs
2	Ten Commandments	\N	ten-commandments
3	Fruits of the Holy Spirit	\N	fruits-holy-spirit
14	Love	3	love
15	Joy	3	joy
16	Peace	3	peace
17	Patience	3	patience
18	Kindness	3	kindness
19	Goodness	3	goodness
20	Faithfulness	3	faithfulness
21	Gentleness	3	gentleness
22	Self-control	3	self-control
4	You shall have no other gods before Me	2	tc01
5	You shall not make for yourself a carved image	2	tc02
6	You shall not take the name of the LORD your God in vain	2	tc03
7	Remember the Sabbath day to keep it holy	2	tc04
8	Honor your father and your mother	2	tc05
9	You shall not murder	2	tc06
10	You shall not commit adultery	2	tc07
11	You shall not steal	2	tc08
12	You shall not bear false witness against your neighbor	2	tc09
13	You shall not covet	2	tc10
\.


--
-- TOC entry 1857 (class 2606 OID 24911)
-- Dependencies: 1575 1575
-- Name: bibledb_category_category_key; Type: CONSTRAINT; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

ALTER TABLE ONLY bibledb_category
    ADD CONSTRAINT bibledb_category_category_key UNIQUE (category);


--
-- TOC entry 1860 (class 2606 OID 24909)
-- Dependencies: 1575 1575
-- Name: bibledb_category_pkey; Type: CONSTRAINT; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

ALTER TABLE ONLY bibledb_category
    ADD CONSTRAINT bibledb_category_pkey PRIMARY KEY (id);


--
-- TOC entry 1863 (class 2606 OID 24948)
-- Dependencies: 1575 1575
-- Name: bibledb_category_slug_key; Type: CONSTRAINT; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

ALTER TABLE ONLY bibledb_category
    ADD CONSTRAINT bibledb_category_slug_key UNIQUE (slug);


--
-- TOC entry 1858 (class 1259 OID 24917)
-- Dependencies: 1575
-- Name: bibledb_category_parent_id; Type: INDEX; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

CREATE INDEX bibledb_category_parent_id ON bibledb_category USING btree (parent_id);


--
-- TOC entry 1861 (class 1259 OID 24918)
-- Dependencies: 1575
-- Name: bibledb_category_slug; Type: INDEX; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

CREATE INDEX bibledb_category_slug ON bibledb_category USING btree (slug);


--
-- TOC entry 1864 (class 2606 OID 24912)
-- Dependencies: 1575 1859 1575
-- Name: parent_id_refs_id_9aca185; Type: FK CONSTRAINT; Schema: public; Owner: leehsueh_appsv1
--

ALTER TABLE ONLY bibledb_category
    ADD CONSTRAINT parent_id_refs_id_9aca185 FOREIGN KEY (parent_id) REFERENCES bibledb_category(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2009-12-13 00:35:32

--
-- PostgreSQL database dump complete
--

