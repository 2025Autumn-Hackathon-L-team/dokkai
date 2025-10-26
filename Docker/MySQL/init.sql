DROP DATABASE chatapp;

CREATE DATABASE IF NOT EXISTS chatapp;

USE chatapp;

CREATE TABLE bookrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name NVARCHAR(50) NOT NULL,
    description NVARCHAR(1000),
    is_public BOOLEAN,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- FOREIGN KEY (user_id) REFERENCES users(uid) ON DELETE CASCADE
INSERT INTO
    bookrooms(
        user_id,
        name,
        description,
        is_public
    )
VALUES
    (
        '970af84c-dd40-47ff-af23-282b72b7cca8',
        'ハリーポッターと賢者の石',
        '賢者の石について細かく話そう！',
        TRUE
    );

INSERT INTO
    bookrooms(
        user_id,
        name,
        description,
        is_public
    )
VALUES
    (
        '970af84c-dd40-47ff-af23-282b72b7cca8',
        'ハリーポッターと秘密の部屋',
        '秘密の部屋について細かく話そう！',
        FALSE
    );
INSERT INTO
    bookrooms(
        user_id,
        name,
        description,
        is_public
    )
VALUES
    (
        '970af84c-dd40-47ff-af23-282b72b7cca8',
        'ハリーポッターとアズカバンの囚人',
        'アズカバンの囚人について細かく話そう！',
        TRUE
    );