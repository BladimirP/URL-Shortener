--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: URLs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."URLs" (
    id integer NOT NULL,
    original_url character varying NOT NULL,
    short_url character varying NOT NULL,
    click_count integer,
    activation_date timestamp without time zone,
    expiration_date timestamp without time zone
);


ALTER TABLE public."URLs" OWNER TO postgres;

--
-- Name: URLs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."URLs_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."URLs_id_seq" OWNER TO postgres;

--
-- Name: URLs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."URLs_id_seq" OWNED BY public."URLs".id;


--
-- Name: URLs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."URLs" ALTER COLUMN id SET DEFAULT nextval('public."URLs_id_seq"'::regclass);


--
-- Data for Name: URLs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."URLs" (id, original_url, short_url, click_count, activation_date, expiration_date) FROM stdin;
7	https://www.google.com/	http://localhost:8000/google-4211bc6f	0	2025-03-26 00:15:09.571187	2025-03-29 00:15:09.571189
6	https://www.google.com/	http://localhost:8000/google-4211bc6e	2	2025-03-30 00:15:09.571187	2025-04-02 00:15:09.571189
\.


--
-- Name: URLs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."URLs_id_seq"', 7, true);


--
-- Name: URLs URLs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."URLs"
    ADD CONSTRAINT "URLs_pkey" PRIMARY KEY (id);


--
-- Name: ix_URLs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "ix_URLs_id" ON public."URLs" USING btree (id);


--
-- PostgreSQL database dump complete
--

