CREATE TYPE usertype AS ENUM
    ('STAFF', 'CUSTOMER');

CREATE TABLE IF NOT EXISTS users
(
    id uuid NOT NULL,
    name character varying(190) COLLATE pg_catalog."default",
    email character varying(190) COLLATE pg_catalog."default",
    dob date,
    password character varying(190) COLLATE pg_catalog."default",
    user_type usertype,
    dt_added timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)