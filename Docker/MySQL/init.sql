DROP DATABASE chatapp;

DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';

CREATE DATABASE chatapp
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE chatapp;

GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    id VARCHAR(255)  NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    iconid INT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ############################ブックルーム関係（ここから）############################
CREATE TABLE bookrooms (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    is_public BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY (name, is_public, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE tags (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE bookroom_tag (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bookroom_id INT NOT NULL,
    tag_id INT NOT NULL,
    UNIQUE KEY (bookroom_id, tag_id),
    FOREIGN KEY (bookroom_id) REFERENCES bookrooms(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
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
    ),
    (
        '970af84c-dd40-47ff-af23-282b72b7cca8',
        'ハリーポッターと炎のゴブレット',
        'ゴブレットの意味を教えて',
        FALSE,
        '2020-01-01 00:00:00',
        '2020-01-01 00:00:00'
    );

-- tagデータ
INSERT INTO
    tags (name)
VALUES
    ('文学・小説'),
    ('ビジネス'),
    ('歴史'),
    ('科学'),
    ('コミック'),
    ('暮らし'),
    ('料理'),
    ('単行本'),
    ('文庫本'),
    ('雑誌'),
    ('受賞作'),
    ('新刊'),
    ('翻訳'),
    ('イラスト多め');

-- ブックルームタグ初期データ
INSERT INTO
    bookroom_tag (bookroom_id, tag_id)
VALUES
(1, 1), (1, 2), (1,3), (1, 4), (1, 5),
(2, 6), (2, 7), (2,8),
(3, 1), (3, 3), (3,5), (3, 7);


-- ############################ブックルーム関係（ここまで）############################
CREATE TABLE messages (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    bookroom_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (bookroom_id) REFERENCES bookrooms(id) ON DELETE CASCADE
);

-- ###########################メッセージ関係（ここまで）############################
CREATE TABLE reactions (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    reaction_type VARCHAR(255) NOT NULL,
    reaction_name VARCHAR(255) NOT NULL
); 
-- ###########################リアクションマスタ（ここまで）############################
CREATE TABLE message_reaction(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    message_id INT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    reaction_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_reaction (message_id, user_id),
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reaction_id) REFERENCES reactions(id)
); 
-- ###########################リアクション・メッセージ トランザクション（ここまで）############################
-- リアクション初期値の導入
INSERT INTO reactions (reaction_type, reaction_name) VALUES
('👍', 'like'),
('💖', 'heart'),
('😢', 'cry'),
('🙏', 'thanks');
-- リアクション初期値の導入(ここまで)
CREATE TABLE icons(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    icon_name VARCHAR(255) NOT NULL ,
    icon_image VARCHAR(255) NOT NULL
);
-- アイコンマスタ（ここまで）
INSERT INTO icons (icon_name, icon_image) VALUES
('book', '/static/img/icons/icon1_book.png'),
('rabbit', '/static/img/icons/icon2_rabbit.png'),
('coffee', '/static/img/icons/icon3_withcoffe.png'),
('animals', '/static/img/icons/icon4_animals.png'),
('readbookwomen', '/static/img/icons/icon5_readbookwomen.png'),
('human', '/static/img/icons/icon6_human.png'),
('dog', '/static/img/icons/icon7_dog.png'),
('cutegirl', '/static/img/icons/icon8_cutegirl.png'),
('readbook', '/static/img/icons/icon9_readbook.png'),
('cat', '/static/img/icons/icon10_cat.png'),
('ringo', '/static/img/icons/icon11_ringo.png'),
('simplegirl', '/static/img/icons/icon12_simplegirl.png'),
('book&coffee', '/static/img/icons/icon13_book&coffee.png'),
('lake', '/static/img/icons/icon14_lake.png'),
('sky', '/static/img/icons/icon15_sky.png'),
('sea', '/static/img/icons/icon16_sea.png'),
('gentleman', '/static/img/icons/icon17_gentleman.png'),
('mountain', '/static/img/icons/icon18_mountain.png'),
('mummy', '/static/img/icons/icon19_mummy.png'),
('bird', '/static/img/icons/icon20_bird.png'),
('balloon', '/static/img/icons/icon21_balloon.png'),
('constellation', '/static/img/icons/icon22_constellation.png'),
('dog2', '/static/img/icons/icon23_dog2.png'),
('blackcat', '/static/img/icons/icon24_blackcat.png'),
('backviewgirl', '/static/img/icons/icon25_backviewgirl.png'),
('flowers', '/static/img/icons/icon26_flowers.png'),
('panda', '/static/img/icons/icon27_panda.png'),
('sloth', '/static/img/icons/icon28_sloth.png'),
('yellowbooks', '/static/img/icons/icon29_yellowbooks.png'),
('crocodile', '/static/img/icons/icon30_crocodile.png'),
('child', '/static/img/icons/icon31_child.png'),
('flowers&book', '/static/img/icons/icon32_flowers&book.png'),
('santa', '/static/img/icons/icon33_santa.png'),
('firework', '/static/img/icons/icon34_firework.png'),
('cherryblossoms', '/static/img/icons/icon35_cherryblossoms.png'),
('cat2', '/static/img/icons/icon36_cat2.png');
-- アイコンサンプル画像（ここまで）
ALTER TABLE users
ADD CONSTRAINT fk_users_iconid
FOREIGN KEY (iconid)
    REFERENCES icons(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE;
-- ユーザーテーブルに外部キー制約を追加(ここまで)