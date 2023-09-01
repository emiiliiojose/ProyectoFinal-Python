drop table passwords;
drop table categorias;
drop table fernet_keys;
drop table users;

select * from users;
select * from categorias;
select * from fernet_keys;
select * from passwords;

drop table categorias;
drop table fernet_keys;
drop table passwords;
drop table users;

-- Creación tabla de categroías
CREATE TABLE categorias
(
    categoria_id serial NOT NULL,
    categoria_nombre text NOT NULL,
    categoria_descripcion text NOT NULL,
    CONSTRAINT categorias_pkey PRIMARY KEY (categoria_id)
)

-- Creación tabla de usuarios
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Creación tabla de fernet keys
CREATE TABLE fernet_keys (
    fernet_key_id SERIAL PRIMARY KEY,
    password_id INTEGER NOT NULL REFERENCES passwords(password_id) ON DELETE CASCADE,
    fernet_key TEXT NOT NULL
);

-- Creación tabla de passwords
CREATE TABLE passwords (
    password_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    website_name TEXT NOT NULL,
    --username TEXT NOT NULL,
	categoria_id INTEGER NOT NULL REFERENCES categorias(categoria_id) ON DELETE CASCADE,
	url TEXT NOT NULL,
	notas TEXT NOT NULL,
    encrypted_password TEXT NOT NULL,
	favorito boolean NOT NULL
);