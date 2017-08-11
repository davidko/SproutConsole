DROP DATABASE IF EXISTS sproutlocker;

create database sproutlocker;

use sproutlocker;

CREATE TABLE log_types(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO log_types (id, name) VALUES
    (1, 'Ph'),
    (2, 'EC'),
    (3, 'text');

CREATE TABLE hosts(
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE log_entries (
    id BIGINT NOT NULL AUTO_INCREMENT,
    host BIGINT NOT NULL,
    FOREIGN KEY (host) REFERENCES hosts(id),
    log_type BIGINT NOT NULL,
    FOREIGN KEY (log_type) REFERENCES log_types(id),
    data FLOAT,
    text TEXT,
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);
