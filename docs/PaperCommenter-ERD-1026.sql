CREATE TABLE `PAPER` (
	`id`	int	NOT NULL,
	`user_id`	int	NOT NULL,
	`slug`	varchar(255)	NOT NULL,
	`title`	varchar(255)	NOT NULL,
	`authors`	varchar(255)	NOT NULL,
	`publish_year`	smallint	NOT NULL,
	`publisher`	varchar(255)	NOT NULL,
	`site_url`	varchar(65535)	NOT NULL,
	`paper_url`	varchar(65535)	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`modify_datetime`	datetime	NULL,
	`like_count`	int	NOT NULL,
	`comment_count`	int	NOT NULL
);

CREATE TABLE `COMMENT` (
	`id`	int	NOT NULL,
	`paper_id`	int	NOT NULL,
	`user_id`	int	NOT NULL,
	`username`	varchar(255)	NOT NULL,
	`content`	varchar(65535)	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`modify_datetime`	datetime	NULL,
	`like_count`	int	NOT NULL
);

CREATE TABLE `USER` (
	`id`	int	NOT NULL,
	`username`	varchar(255)	NOT NULL,
	`hashed_password`	varchar(255)	NOT NULL,
	`email`	varchar(255)	NOT NULL,
	`message`	varchar(255)	NOT NULL,
	`image_url`	varchar(255)	NOT NULL
);

CREATE TABLE `PAPER_LIKE` (
	`paper_id`	int	NOT NULL,
	`user_id`	int	NOT NULL
);

CREATE TABLE `COMMENT_LIKE` (
	`comment_id`	int	NOT NULL,
	`user_id`	int	NOT NULL
);

ALTER TABLE `PAPER` ADD CONSTRAINT `PK_PAPER` PRIMARY KEY (
	`id`,
	`user_id`
);

ALTER TABLE `COMMENT` ADD CONSTRAINT `PK_COMMENT` PRIMARY KEY (
	`id`,
	`paper_id`,
	`user_id`
);

ALTER TABLE `USER` ADD CONSTRAINT `PK_USER` PRIMARY KEY (
	`id`
);

ALTER TABLE `PAPER_LIKE` ADD CONSTRAINT `PK_PAPER_LIKE` PRIMARY KEY (
	`paper_id`,
	`user_id`
);

ALTER TABLE `COMMENT_LIKE` ADD CONSTRAINT `PK_COMMENT_LIKE` PRIMARY KEY (
	`comment_id`,
	`user_id`
);

ALTER TABLE `PAPER` ADD CONSTRAINT `FK_USER_TO_PAPER_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `USER` (
	`id`
);

ALTER TABLE `COMMENT` ADD CONSTRAINT `FK_PAPER_TO_COMMENT_1` FOREIGN KEY (
	`paper_id`
)
REFERENCES `PAPER` (
	`id`
);

ALTER TABLE `COMMENT` ADD CONSTRAINT `FK_USER_TO_COMMENT_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `USER` (
	`id`
);

ALTER TABLE `PAPER_LIKE` ADD CONSTRAINT `FK_PAPER_TO_PAPER_LIKE_1` FOREIGN KEY (
	`paper_id`
)
REFERENCES `PAPER` (
	`id`
);

ALTER TABLE `PAPER_LIKE` ADD CONSTRAINT `FK_USER_TO_PAPER_LIKE_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `USER` (
	`id`
);

ALTER TABLE `COMMENT_LIKE` ADD CONSTRAINT `FK_COMMENT_TO_COMMENT_LIKE_1` FOREIGN KEY (
	`comment_id`
)
REFERENCES `COMMENT` (
	`id`
);

ALTER TABLE `COMMENT_LIKE` ADD CONSTRAINT `FK_USER_TO_COMMENT_LIKE_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `USER` (
	`id`
);

