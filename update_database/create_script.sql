DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;

CREATE TABLE source (
  source_id      integer NOT NULL PRIMARY KEY,
  article_doi    text NOT NULL,
  pmid           integer,
  pubchem_id     text,
  patent_number  text,
  authors        text,
  institution    text
) WITH (
    OIDS = TRUE
  );

ALTER TABLE source
  OWNER TO "data";

insert into source values (-1, 'Unknown source', NULL, '', '', '', '');


CREATE TABLE ligand (
  ligand_id    integer NOT NULL PRIMARY KEY,
  inchi        text NOT NULL,
  inchi_key    text NOT NULL,
  inchi_bdb    text,
  inchi_chembl text,
  smiles       text,
  no_metal     boolean
) WITH (
    OIDS = TRUE
  );

ALTER TABLE ligand
  OWNER TO "data";







CREATE TABLE receptor (
  receptor_id         integer NOT NULL PRIMARY KEY,
  uniprot_id          text NOT NULL,
  uniprot_name        text NOT NULL,
  uniprot_short_name  text NOT NULL,
  trivial_names       text,
  full_names          text,
  short_nr            text,
  chembl_number       text
) WITH (
    OIDS = TRUE
  );

ALTER TABLE receptor
  OWNER TO "data";









CREATE TABLE activity (
  activity_id      integer NOT NULL PRIMARY KEY,
  source_id        integer NOT NULL,
  receptor_id      integer NOT NULL,
  ligand_id        integer NOT NULL,
  "type"           text NULL,
  relation         varchar(10) NULL,
  "value"          float NULL,
  unit             varchar(20) NULL,
  p_chembl         float,
  confidence_score integer,
  ph               float,
  temperature      text,
  source_db        text NOT NULL,

  CONSTRAINT activity_source
    FOREIGN KEY (source_id)
    REFERENCES source(source_id), 
  CONSTRAINT activity_ligand
    FOREIGN KEY (ligand_id)
    REFERENCES ligand(ligand_id),
  CONSTRAINT activity_receptor
    FOREIGN KEY (receptor_id)
    REFERENCES receptor(receptor_id)
) WITH (
    OIDS = TRUE
  );

ALTER TABLE activity
  OWNER TO "data";
