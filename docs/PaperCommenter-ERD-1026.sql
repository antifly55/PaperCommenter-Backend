CREATE TABLE `Paper` (
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

CREATE TABLE `Comment` (
	`id`	int	NOT NULL,
	`paper_id`	int	NOT NULL,
	`user_id`	int	NOT NULL,
	`username`	varchar(255)	NOT NULL,
	`content`	varchar(65535)	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`modify_datetime`	datetime	NULL,
	`like_count`	int	NOT NULL
);

CREATE TABLE `User` (
	`id`	int	NOT NULL,
	`username`	varchar(255)	NOT NULL,
	`hashed_password`	varchar(255)	NOT NULL,
	`email`	varchar(255)	NOT NULL,
	`message`	varchar(255)	NOT NULL,
	`image_url`	varchar(255)	NOT NULL
);

CREATE TABLE `PaperLike` (
	`paper_id`	int	NOT NULL,
	`user_id`	int	NOT NULL
);

CREATE TABLE `CommentLike` (
	`comment_id`	int	NOT NULL,
	`user_id`	int	NOT NULL
);

ALTER TABLE `Paper` ADD CONSTRAINT `PK_PAPER` PRIMARY KEY (
	`id`,
	`user_id`
);

ALTER TABLE `Comment` ADD CONSTRAINT `PK_COMMENT` PRIMARY KEY (
	`id`,
	`paper_id`,
	`user_id`
);

ALTER TABLE `User` ADD CONSTRAINT `PK_USER` PRIMARY KEY (
	`id`
);

ALTER TABLE `PaperLike` ADD CONSTRAINT `PK_PAPERLIKE` PRIMARY KEY (
	`paper_id`,
	`user_id`
);

ALTER TABLE `CommentLike` ADD CONSTRAINT `PK_COMMENTLIKE` PRIMARY KEY (
	`comment_id`,
	`user_id`
);

ALTER TABLE `Paper` ADD CONSTRAINT `FK_User_TO_Paper_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`id`
);

ALTER TABLE `Comment` ADD CONSTRAINT `FK_Paper_TO_Comment_1` FOREIGN KEY (
	`paper_id`
)
REFERENCES `Paper` (
	`id`
);

ALTER TABLE `Comment` ADD CONSTRAINT `FK_User_TO_Comment_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`id`
);

ALTER TABLE `PaperLike` ADD CONSTRAINT `FK_Paper_TO_PaperLike_1` FOREIGN KEY (
	`paper_id`
)
REFERENCES `Paper` (
	`id`
);

ALTER TABLE `PaperLike` ADD CONSTRAINT `FK_User_TO_PaperLike_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`id`
);

ALTER TABLE `CommentLike` ADD CONSTRAINT `FK_Comment_TO_CommentLike_1` FOREIGN KEY (
	`comment_id`
)
REFERENCES `Comment` (
	`id`
);

ALTER TABLE `CommentLike` ADD CONSTRAINT `FK_User_TO_CommentLike_1` FOREIGN KEY (
	`user_id`
)
REFERENCES `User` (
	`id`
);

