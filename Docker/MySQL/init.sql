DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    /*id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,MySQL内での挙動確認用*/
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ############################ブックルーム関係（ここから）############################
CREATE TABLE bookrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name NVARCHAR(50) NOT NULL,
    description NVARCHAR(1000),
    is_public BOOLEAN,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 初期値を挿入
INSERT INTO users (id, name, email, password)
VALUES ('970af84c-dd40-47ff-af23-282b72b7cca8', 'テスト', 'test@gmail.com', '37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');

INSERT INTO bookrooms (user_id, name, description, is_public, created_at, updated_at)
VALUES ('970af84c-dd40-47ff-af23-282b72b7cca8', 'ハリーポッターと賢者の石', '賢者の石について細かく話そう！',
    TRUE, '2020-1-1 0:00:00','2020-1-1 0:00:00');

INSERT INTO bookrooms (user_id, name, description, is_public, created_at, updated_at)
VALUES ('970af84c-dd40-47ff-af23-282b72b7cca8', 'ハリーポッターと秘密の部屋', '秘密の部屋について細かく話そう！',
    FALSE,'2020-1-1 0:00:00','2020-1-1 0:00:00');

INSERT INTO bookrooms (user_id, name, description, is_public, created_at, updated_at)
VALUES ('970af84c-dd40-47ff-af23-282b72b7cca8', 'ハリーポッターとアズカバンの囚人', 'アズカバンの囚人について細かく話そう！',
    TRUE, '2020-1-1 0:00:00','2020-1-1 0:00:00');



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
