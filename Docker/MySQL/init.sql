DROP DATABASE chatapp;

DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';

CREATE DATABASE chatapp;

USE chatapp;

GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

-- TODO M_iconsテーブルができたら、外部キー制約を入れる
CREATE TABLE users (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    iconid VARCHAR(255),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ############################ブックルーム関係（ここから）############################
CREATE TABLE bookrooms (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    is_public BOOLEAN,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE tags (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- 初期値を挿入
-- users を2人分入れてから
INSERT INTO
    users (id, name, email, password)
VALUES
    (
        '970af84c-dd40-47ff-af23-282b72b7cca8',
        'テストA',
        'testA@gmail.com',
        'dummy'
    ),
    (
        '11111111-2222-3333-4444-555555555555',
        'テストB',
        'testB@gmail.com',
        'dummy'
    );

-- bookrooms
INSERT INTO
    bookrooms (
        user_id,
        name,
        description,
        is_public,
        created_at,
        updated_at
    )
VALUES
    (
        '970af84c-dd40-47ff-af23-282b72b7cca8',
        'ハリーポッターと賢者の石',
        '賢者の石について細かく話そう！',
        TRUE,
        '2020-01-01 00:00:00',
        '2020-01-01 00:00:00'
    ),
    (
        '11111111-2222-3333-4444-555555555555',
        'ハリーポッターと秘密の部屋',
        '秘密の部屋について細かく話そう！',
        FALSE,
        '2020-01-01 00:00:00',
        '2020-01-01 00:00:00'
    ),
    (
        '11111111-2222-3333-4444-555555555555',
        'ハリーポッターとアズカバンの囚人',
        'アズカバンの囚人について細かく話そう！',
        TRUE,
        '2020-01-01 00:00:00',
        '2020-01-01 00:00:00'
    );

-- tagデータ
INSERT INTO
    tags (name)
VALUES
    ('恋愛'),
    ('SF'),
    ('日本文学'),
    ('ミステリー');

-- ############################ブックルーム関係（ここまで）############################
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    bookroom_id INT NOT NULL,
    content VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (bookroom_id) REFERENCES bookrooms(id) ON DELETE CASCADE
);

-- ###########################メッセージ関係（ここまで）############################