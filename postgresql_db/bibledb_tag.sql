--
-- PostgreSQL database dump
--

-- Started on 2009-12-13 00:36:23

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
-- TOC entry 1577 (class 1259 OID 24921)
-- Dependencies: 3
-- Name: bibledb_tag; Type: TABLE; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

CREATE TABLE bibledb_tag (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    slug character varying(32) NOT NULL
);


ALTER TABLE public.bibledb_tag OWNER TO leehsueh_appsv1;

--
-- TOC entry 1576 (class 1259 OID 24919)
-- Dependencies: 3 1577
-- Name: bibledb_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: leehsueh_appsv1
--

CREATE SEQUENCE bibledb_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.bibledb_tag_id_seq OWNER TO leehsueh_appsv1;

--
-- TOC entry 1865 (class 0 OID 0)
-- Dependencies: 1576
-- Name: bibledb_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: leehsueh_appsv1
--

ALTER SEQUENCE bibledb_tag_id_seq OWNED BY bibledb_tag.id;


--
-- TOC entry 1866 (class 0 OID 0)
-- Dependencies: 1576
-- Name: bibledb_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: leehsueh_appsv1
--

SELECT pg_catalog.setval('bibledb_tag_id_seq', 5, true);


--
-- TOC entry 1855 (class 2604 OID 24924)
-- Dependencies: 1576 1577 1577
-- Name: id; Type: DEFAULT; Schema: public; Owner: leehsueh_appsv1
--

ALTER TABLE bibledb_tag ALTER COLUMN id SET DEFAULT nextval('bibledb_tag_id_seq'::regclass);


--
-- TOC entry 1862 (class 0 OID 24921)
-- Dependencies: 1577
-- Data for Name: bibledb_tag; Type: TABLE DATA; Schema: public; Owner: leehsueh_appsv1
--

COPY bibledb_tag (id, name, slug) FROM stdin;
1	Loving God	loving-god
2	Servitude	servitude
3	Evangelism	evangelism
4	Pastoring	pastoring
5	Interpersonal Relationships	interpersonal-relationships
\.


--
-- TOC entry 1857 (class 2606 OID 24928)
-- Dependencies: 1577 1577
-- Name: bibledb_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

ALTER TABLE ONLY bibledb_tag
    ADD CONSTRAINT bibledb_tag_name_key UNIQUE (name);


--
-- TOC entry 1859 (class 2606 OID 24926)
-- Dependencies: 1577 1577
-- Name: bibledb_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

ALTER TABLE ONLY bibledb_tag
    ADD CONSTRAINT bibledb_tag_pkey PRIMARY KEY (id);


--
-- TOC entry 1861 (class 2606 OID 24940)
-- Dependencies: 1577 1577
-- Name: bibledb_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: leehsueh_appsv1; Tablespace: 
--

ALTER TABLE ONLY bibledb_tag
    ADD CONSTRAINT bibledb_tag_slug_key UNIQUE (slug);


-- Completed on 2009-12-13 00:36:23

--
-- PostgreSQL database dump complete
--

