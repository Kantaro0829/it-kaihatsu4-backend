CREATE DATABASE IF NOT EXISTS test;
use test;

CREATE TABLE users (
    user_id INT(8) NOT NULL,
    password VARCHAR(270) NOT  NULL,
    email varchar(30) unique,
    lang_id INT(8) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE users
  ADD PRIMARY KEY (user_id);

ALTER TABLE users
  MODIFY user_id int(8) AUTO_INCREMENT,AUTO_INCREMENT=1;

INSERT INTO users (password, email, lang_id)
        VALUES ("5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "example@gmail.com",
                1);

CREATE TABLE languages (
    lang_id INT(8) NOT NULL,
    lang_code varchar(40) unique,
    lang_name varchar(40) unique
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE languages
  ADD PRIMARY KEY (lang_id);

ALTER TABLE languages
  MODIFY lang_id int(8) AUTO_INCREMENT,AUTO_INCREMENT=1;

INSERT INTO languages (lang_code, lang_name) VALUES
        ("BG", "Bulgarian"),
        ("CS", "Czech"),
        ("DA", "Danish"),
        ("DE", "German"),
        ("EL", "Greek"),
        ("EN-GB", "English (British)"),
        ("EN-US", "English (American)"),
        ("ES", "Spanish"),
        ("ET", "Estonian"),
        ("FI", "Finnish"),
        ("FR", "French"),
        ("HU", "Hungarian"),
        ("IT", "Italian"),
        ("JA", "Japanese"),
        ("LT", "Lithuanian"),
        ("LV", "Latvian"),
        ("NL", "Dutch"),
        ("PL", "Polish"),
        ("PT-PT", "Portuguese"),
        ("PT-BR", "Portuguese (Brazilian)"),
        ("RO", "Romanian"),
        ("RU", "Russian"),
        ("SK", "Slovak"),
        ("SL", "Slovenian"),
        ("SV", "Swedish"),
        ("ZH", "Chinese");

CREATE TABLE historys (
    data_id INT(8) NOT NULL,
    user_id INT(8) NOT NULL,
    before_translation text NOT NULL,
    after_translation text NOT NULL,
    before_lang_code varchar(40) NOT NULL,
    after_lang_code varchar(40) NOT NULL,
    recoded_date date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE historys
  ADD PRIMARY KEY (data_id);

ALTER TABLE historys
  MODIFY data_id int(8) AUTO_INCREMENT,AUTO_INCREMENT=1;


INSERT INTO historys 
    (user_id, before_translation, after_translation, before_lang_code, after_lang_code, recoded_date)
        VALUES (1,
                "This is the official documentation for Python",
                "Dette er den officielle dokumentation for Python",
                "EN",
                "DA",
                "2019-04-17"
                );




        














        


