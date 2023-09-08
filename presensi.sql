--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: Courses; Type: TABLE; Schema: public; Owner: owner
--

CREATE TABLE public."Courses" (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_updated timestamp with time zone,
    course_name character varying(50),
    start_time timestamp without time zone,
    duration_in_minutes integer NOT NULL,
    lecturer_id integer,
    room_id integer,
    secret_key character varying(32),
    lecture_number integer
);


ALTER TABLE public."Courses" OWNER TO owner;

--
-- Name: Courses_id_seq; Type: SEQUENCE; Schema: public; Owner: owner
--

CREATE SEQUENCE public."Courses_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Courses_id_seq" OWNER TO owner;

--
-- Name: Courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: owner
--

ALTER SEQUENCE public."Courses_id_seq" OWNED BY public."Courses".id;


--
-- Name: Logs; Type: TABLE; Schema: public; Owner: owner
--

CREATE TABLE public."Logs" (
    id integer NOT NULL,
    date_created timestamp with time zone,
    course_id integer,
    user_id integer,
    log_time timestamp without time zone,
    approved_time timestamp without time zone,
    approver_id integer
);


ALTER TABLE public."Logs" OWNER TO owner;

--
-- Name: Logs_id_seq; Type: SEQUENCE; Schema: public; Owner: owner
--

CREATE SEQUENCE public."Logs_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Logs_id_seq" OWNER TO owner;

--
-- Name: Logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: owner
--

ALTER SEQUENCE public."Logs_id_seq" OWNED BY public."Logs".id;


--
-- Name: Participants; Type: TABLE; Schema: public; Owner: owner
--

CREATE TABLE public."Participants" (
    id integer NOT NULL,
    course_id integer,
    user_id integer
);


ALTER TABLE public."Participants" OWNER TO owner;

--
-- Name: Participants_id_seq; Type: SEQUENCE; Schema: public; Owner: owner
--

CREATE SEQUENCE public."Participants_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Participants_id_seq" OWNER TO owner;

--
-- Name: Participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: owner
--

ALTER SEQUENCE public."Participants_id_seq" OWNED BY public."Participants".id;


--
-- Name: Rooms; Type: TABLE; Schema: public; Owner: owner
--

CREATE TABLE public."Rooms" (
    id integer NOT NULL,
    status character varying(255) DEFAULT 'draft'::character varying NOT NULL,
    date_created timestamp with time zone,
    date_updated timestamp with time zone,
    room_name character varying(50),
    building character varying(50),
    floor character varying(20),
    capacity integer
);


ALTER TABLE public."Rooms" OWNER TO owner;

--
-- Name: Rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: owner
--

CREATE SEQUENCE public."Rooms_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Rooms_id_seq" OWNER TO owner;

--
-- Name: Rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: owner
--

ALTER SEQUENCE public."Rooms_id_seq" OWNED BY public."Rooms".id;


--
-- Name: Users; Type: TABLE; Schema: public; Owner: owner
--

CREATE TABLE public."Users" (
    id integer NOT NULL,
    status character varying(255) DEFAULT 'draft'::character varying NOT NULL,
    date_created timestamp with time zone,
    date_updated timestamp with time zone,
    name character varying(50),
    username character varying(20),
    password character varying(72),
    role character varying(10),
    secret_key character varying(32)
);


ALTER TABLE public."Users" OWNER TO owner;

--
-- Name: Users_id_seq; Type: SEQUENCE; Schema: public; Owner: owner
--

CREATE SEQUENCE public."Users_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Users_id_seq" OWNER TO owner;

--
-- Name: Users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: owner
--

ALTER SEQUENCE public."Users_id_seq" OWNED BY public."Users".id;


--
-- Name: Courses id; Type: DEFAULT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Courses" ALTER COLUMN id SET DEFAULT nextval('public."Courses_id_seq"'::regclass);


--
-- Name: Logs id; Type: DEFAULT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Logs" ALTER COLUMN id SET DEFAULT nextval('public."Logs_id_seq"'::regclass);


--
-- Name: Participants id; Type: DEFAULT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Participants" ALTER COLUMN id SET DEFAULT nextval('public."Participants_id_seq"'::regclass);


--
-- Name: Rooms id; Type: DEFAULT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Rooms" ALTER COLUMN id SET DEFAULT nextval('public."Rooms_id_seq"'::regclass);


--
-- Name: Users id; Type: DEFAULT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Users" ALTER COLUMN id SET DEFAULT nextval('public."Users_id_seq"'::regclass);


--
-- Data for Name: Courses; Type: TABLE DATA; Schema: public; Owner: owner
--

COPY public."Courses" (id, date_created, date_updated, course_name, start_time, duration_in_minutes, lecturer_id, room_id, secret_key, lecture_number) FROM stdin;
\.


--
-- Data for Name: Logs; Type: TABLE DATA; Schema: public; Owner: owner
--

COPY public."Logs" (id, date_created, course_id, user_id, log_time, approved_time, approver_id) FROM stdin;
\.


--
-- Data for Name: Participants; Type: TABLE DATA; Schema: public; Owner: owner
--

COPY public."Participants" (id, course_id, user_id) FROM stdin;
\.


--
-- Data for Name: Rooms; Type: TABLE DATA; Schema: public; Owner: owner
--

COPY public."Rooms" (id, status, date_created, date_updated, room_name, building, floor, capacity) FROM stdin;
\.


--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: owner
--

COPY public."Users" (id, status, date_created, date_updated, name, username, password, role, secret_key) FROM stdin;
2	published	2022-06-30 18:46:56.263+07	2022-06-30 21:23:56.669+07	Test Two	test2	123	1	1
1	published	2022-06-30 18:36:35.495+07	2022-06-30 22:10:18.051+07	Test	test	123	1	1
3	draft	2022-06-30 22:45:39.514+07	\N	Test Three	test3	\N	\N	\N
\.


--
-- Name: Courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: owner
--

SELECT pg_catalog.setval('public."Courses_id_seq"', 1, false);


--
-- Name: Logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: owner
--

SELECT pg_catalog.setval('public."Logs_id_seq"', 1, false);


--
-- Name: Participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: owner
--

SELECT pg_catalog.setval('public."Participants_id_seq"', 1, false);


--
-- Name: Rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: owner
--

SELECT pg_catalog.setval('public."Rooms_id_seq"', 1, false);


--
-- Name: Users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: owner
--

SELECT pg_catalog.setval('public."Users_id_seq"', 3, true);


--
-- Name: Courses Courses_pkey; Type: CONSTRAINT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Courses"
    ADD CONSTRAINT "Courses_pkey" PRIMARY KEY (id);


--
-- Name: Logs Logs_pkey; Type: CONSTRAINT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Logs"
    ADD CONSTRAINT "Logs_pkey" PRIMARY KEY (id);


--
-- Name: Participants Participants_pkey; Type: CONSTRAINT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Participants"
    ADD CONSTRAINT "Participants_pkey" PRIMARY KEY (id);


--
-- Name: Rooms Rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Rooms"
    ADD CONSTRAINT "Rooms_pkey" PRIMARY KEY (id);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: owner
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

