CREATE TABLE users (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(15) NOT NULL UNIQUE,
    password CHAR(60) BINARY NOT NULL,
    role enum('Administrator', 'Moderator'),
    active BOOLEAN DEFAULT true,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT NOW() ON UPDATE NOW(),
    PRIMARY KEY (id)
);