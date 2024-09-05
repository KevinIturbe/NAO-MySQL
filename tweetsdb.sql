-- Se crea la base de datos
CREATE DATABASE IF NOT EXISTS TweetsDB;

USE TweetsDB;

-- Se define la tabla
CREATE TABLE Tweets (
	id BIGINT PRIMARY KEY,
    texto TEXT,
    hashtags TEXT,
    usuario VARCHAR(50),
    fecha DATETIME,
    retweets INT,
	favoritos INT
);

SELECT * FROM Tweets;


-- Se crea la tabla usuarios
CREATE TABLE Usuarios (
	usuario VARCHAR(50),
    edad INT,
    sexo VARCHAR(20),
    pais VARCHAR (20)
);
 
-- Se define la tabla Retweets
CREATE TABLE Retweets (
    tweet_id BIGINT,
    usuario_id BIGINT,
    fecha_retweet DATETIME,
    PRIMARY KEY (tweet_id, usuario_id),
    FOREIGN KEY (tweet_id) REFERENCES Tweets(id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);
 
SELECT * FROM Tweets;
SELECT * FROM usuarios;