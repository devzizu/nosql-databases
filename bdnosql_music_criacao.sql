
drop table musica;
drop table review;
drop table titulo;
drop table suporte;
drop table autor;
drop table genero;
drop table editora;

CREATE TABLE autor
 (
     id_autor int NOT NULL ENABLE,
     nome VARCHAR2(200 byte) NOT NULL ENABLE,
     CONSTRAINT AUTOR_PK PRIMARY KEY (id_autor)
 );
 
 CREATE TABLE editora
 (
     id_editora int NOT NULL ENABLE,
     nome VARCHAR2(200 byte) NOT NULL ENABLE,
     CONSTRAINT EDITORA_PK PRIMARY KEY (id_editora)
 );
 
 CREATE TABLE genero
 (
     id_genero NUMBER(1, 0) NOT NULL ENABLE,
     nome VARCHAR2(200 byte) NOT NULL ENABLE,
     CONSTRAINT GENERO_PK PRIMARY KEY (id_genero)
 );

CREATE TABLE suporte
 (
     id_suporte int NOT NULL ENABLE,
     nome VARCHAR2(200 byte) NOT NULL ENABLE,
     CONSTRAINT SUPORTE_PK PRIMARY KEY (id_suporte)
 );
 
CREATE TABLE titulo
 (
     id_titulo int NOT NULL ENABLE,
     titulo VARCHAR2(200 byte) NOT NULL ENABLE,
     preco NUMBER(8, 2) NOT NULL ENABLE,
     dta_compra DATE NOT NULL,     
     id_editora int,
     id_suporte int,
     id_genero NUMBER(1, 0),
     id_autor int,
     CONSTRAINT TITULO_TITULO_EDITORA_FK FOREIGN KEY (id_editora) REFERENCES editora(id_editora) enable,
     CONSTRAINT TITULO_SUPORTE_FK FOREIGN KEY (id_suporte) REFERENCES suporte(id_suporte) enable,
     CONSTRAINT TITULO_GENERO_FK FOREIGN KEY (id_genero) REFERENCES genero(id_genero) enable,
     CONSTRAINT TITULO_AUTOR_FK FOREIGN KEY (id_autor) REFERENCES autor(id_autor) enable,
     CONSTRAINT TITULO_TITULO_PK PRIMARY KEY (id_titulo)     
 );

CREATE TABLE musica
 (
     id_musica int NOT NULL ENABLE,
     nome_musica VARCHAR2(200 byte) NOT NULL ENABLE,
     id_autor int,
     id_titulo int,
     CONSTRAINT MUSICA_AUTOR_FK FOREIGN KEY (id_autor) REFERENCES autor(id_autor),
     CONSTRAINT MUSICA_TITULO_FK FOREIGN KEY (id_titulo) REFERENCES titulo(id_titulo),
     CONSTRAINT MUSICA_PK PRIMARY KEY (id_musica)     
 );
 
 CREATE TABLE review
 (
     id_review int NOT NULL ENABLE,
     id_titulo int,
     CONSTRAINT REVIEW_TITULO_FK FOREIGN KEY (id_titulo) REFERENCES titulo(id_titulo),
     dta_review DATE NOT NULL ENABLE,
     conteudo VARCHAR2(200 byte) NOT NULL ENABLE,
     CONSTRAINT REVIEW_PK PRIMARY KEY (id_review)     
 );
