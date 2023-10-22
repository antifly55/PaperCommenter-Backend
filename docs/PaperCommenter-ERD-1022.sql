CREATE TABLE `Paper` (
	`id`	int	NOT NULL,
	`user_id`	int	NOT NULL,
	`title`	varchar(256)	NOT NULL,
	`abstract`	text	NOT NULL,
	`year`	int	NOT NULL,
	`publisher`	varchar(256)	NOT NULL,
	`url`	varchar(1024)	NOT NULL,
	`content`	longtext	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`modify_datetime`	datetime	NULL,
	`Field`	int	NOT NULL,
	`Field2`	int	NOT NULL,
	`username`	varchar(64)	NOT NULL
);

CREATE TABLE `Comment` (
	`id`	int	NOT NULL,
	`paper_id`	int	NOT NULL,
	`user_id`	int	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`Field2`	datetime	NULL,
	`like_count`	int	NOT NULL
);

CREATE TABLE `User` (
	`id`	int	NOT NULL,
	`username`	varchar(64)	NOT NULL,
	`password_sha256`	varchar(256)	NOT NULL,
	`email`	varchar(256)	NOT NULL,
	`message`	varchar(512)	NULL,
	`image_url`	varchar(1024)	NULL
);

CREATE TABLE `Author` (
	`id`	int	NOT NULL,
	`name`	varchar(64)	NOT NULL,
	`url`	varchar(1024)	NULL
);

CREATE TABLE `Paper_Author` (
	`paper_id`	int	NOT NULL,
	`author_id`	int	NOT NULL
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

ALTER TABLE `Author` ADD CONSTRAINT `PK_AUTHOR` PRIMARY KEY (
	`id`
);

ALTER TABLE `Paper_Author` ADD CONSTRAINT `PK_PAPER_AUTHOR` PRIMARY KEY (
	`paper_id`,
	`author_id`
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

ALTER TABLE `Paper_Author` ADD CONSTRAINT `FK_Paper_TO_Paper_Author_1` FOREIGN KEY (
	`paper_id`
)
REFERENCES `Paper` (
	`id`
);

ALTER TABLE `Paper_Author` ADD CONSTRAINT `FK_Author_TO_Paper_Author_1` FOREIGN KEY (
	`author_id`
)
REFERENCES `Author` (
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

