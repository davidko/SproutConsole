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

CREATE TABLE log_entries (
    id BIGINT NOT NULL AUTO_INCREMENT,
    log_type BIGINT NOT NULL,
    FOREIGN KEY (log_type) REFERENCES log_types(id),
    data FLOAT,
    text TEXT,
	date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);
