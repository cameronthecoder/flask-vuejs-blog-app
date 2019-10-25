CREATE TABLE posts (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    title VARCHAR(80) NOT NULL,
    author_id MEDIUMINT NOT NULL,
    slug VARCHAR(80) NOT NULL,
    body TEXT NOT NULL,
    draft BOOLEAN DEFAULT false,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX auth_id (author_id),
    FOREIGN KEY (author_id)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=INNODB;