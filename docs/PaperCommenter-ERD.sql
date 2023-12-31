﻿CREATE TABLE `PAPER` (
	`id`	int	UNSIGNED	NOT NULL	AUTO_INCREMENT PRIMARY KEY,
	`user_id`	int	UNSIGNED	NOT NULL,
	`hashed_slug`	int	UNSIGNED	NOT NULL,
	`slug`	nvarchar(255)	NOT NULL	UNIQUE KEY,
	`title`	nvarchar(255)	NOT NULL	UNIQUE KEY,
	`authors`	nvarchar(255)	NOT NULL,
	`publish_year`	smallint	NOT NULL,
	`publisher`	nvarchar(255)	NOT NULL,
	`site_url`	nvarchar(10000)	NOT NULL,
	`paper_url`	nvarchar(10000)	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`modify_datetime`	datetime	NULL,
	`like_count`	int	UNSIGNED	NOT NULL,
	`comment_count`	int	UNSIGNED	NOT NULL,
	`rating_count`	int	UNSIGNED	NOT NULL,
	`rating_average`	float	NOT NULL
);

CREATE TABLE `COMMENT` (
	`id`	int	UNSIGNED	NOT NULL	AUTO_INCREMENT	PRIMARY KEY,
	`paper_id`	int	UNSIGNED	NOT NULL,
	`user_id`	int	UNSIGNED	NOT NULL,
	`hashed_identifier`	int	UNSIGNED	NOT NULL,
	`username`	nvarchar(255)	NOT NULL,
	`content`	nvarchar(10000)	NOT NULL,
	`create_datetime`	datetime	NOT NULL,
	`modify_datetime`	datetime	NULL,
	`like_count`	int	UNSIGNED	NOT NULL,
	UNIQUE KEY	combination (`user_id`, `create_datetime`)
);

CREATE TABLE `USER` (
	`id`	int	UNSIGNED	NOT NULL	AUTO_INCREMENT	PRIMARY KEY,
	`hashed_username`	int	UNSIGNED	NOT NULL,
	`username`	nvarchar(255)	NOT NULL	UNIQUE KEY,
	`hashed_password`	varchar(255)	NOT NULL,
	`email`	nvarchar(255)	NOT NULL,
	`message`	nvarchar(255)	NOT NULL,
	`image_url`	nvarchar(255)	NOT NULL
);

CREATE TABLE `PAPER_LIKE` (
	`paper_id`	int	UNSIGNED	NOT NULL,
	`user_id`	int	UNSIGNED	NOT NULL,
	UNIQUE KEY	combination (`paper_id`, `user_id`)
);

CREATE TABLE `PAPER_RATING` (
	`paper_id`	int	UNSIGNED	NOT NULL,
	`user_id`	int	UNSIGNED	NOT NULL,
	`rating`	int	NOT NULL,
	UNIQUE KEY	combination (`paper_id`, `user_id`)
);

CREATE TABLE `COMMENT_LIKE` (
	`comment_id`	int	UNSIGNED	NOT NULL,
	`user_id`	int	UNSIGNED	NOT NULL,
	UNIQUE KEY	combination (`comment_id`, `user_id`)
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

ALTER TABLE `PAPER_RATING` ADD CONSTRAINT `FK_PAPER_TO_PAPER_RATING_1` FOREIGN KEY (
	`paper_id`
)
REFERENCES `PAPER` (
	`id`
);

ALTER TABLE `PAPER_RATING` ADD CONSTRAINT `FK_USER_TO_PAPER_RATING_1` FOREIGN KEY (
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


CREATE INDEX `PAPER_IDX_HASHED_SLUG` ON `PAPER` (`hashed_slug`);

CREATE INDEX `COMMENT_IDX_HASHED_IDENTIFIER` ON `COMMENT` (`hashed_identifier`); 

CREATE INDEX `USER_IDX_HASHED_USERNAME` ON `USER` (`hashed_username`); 


SET GLOBAL event_scheduler = ON;

CREATE EVENT IF NOT EXISTS `PaperLikeCountUpdate`
    ON SCHEDULE
        EVERY 1 MINUTE STARTS NOW()
    ON COMPLETION NOT PRESERVE
    ENABLE
    DO
    UPDATE paper as A
	INNER JOIN (SELECT paper_id, count(*) as cnt FROM paper_like GROUP BY paper_id) as B
	ON B.paper_id=A.id
	SET A.like_count=B.cnt
	WHERE B.paper_id=A.id;

CREATE EVENT IF NOT EXISTS `PaperCommentCountUpdate`
    ON SCHEDULE
        EVERY 1 MINUTE STARTS NOW()
    ON COMPLETION NOT PRESERVE
    ENABLE
    DO
    UPDATE paper as A
	INNER JOIN (SELECT paper_id, count(*) as cnt FROM comment GROUP BY paper_id) as B
	ON B.paper_id=A.id
	SET A.comment_count=B.cnt
	WHERE B.paper_id=A.id;

CREATE EVENT IF NOT EXISTS `PaperRatingCountUpdate`
    ON SCHEDULE
        EVERY 1 MINUTE STARTS NOW()
    ON COMPLETION NOT PRESERVE
    ENABLE
    DO
    UPDATE paper as A
	INNER JOIN (SELECT paper_id, count(*) as cnt FROM paper_rating GROUP BY paper_id) as B
	ON B.paper_id=A.id
	SET A.rating_count=B.cnt
	WHERE B.paper_id=A.id;

CREATE EVENT IF NOT EXISTS `PaperRatingAverageUpdate`
    ON SCHEDULE
        EVERY 1 MINUTE STARTS NOW()
    ON COMPLETION NOT PRESERVE
    ENABLE
    DO
    UPDATE paper as A
	INNER JOIN (SELECT paper_id, IF(count(paper_id)=0, 0, avg(rating)) as average FROM paper_rating GROUP BY paper_id) as B
	ON B.paper_id=A.id
	SET A.rating_average=B.average
	WHERE B.paper_id=A.id;

CREATE EVENT IF NOT EXISTS `CommentLikeCountUpdate`
    ON SCHEDULE
        EVERY 1 MINUTE STARTS NOW()
    ON COMPLETION NOT PRESERVE
    ENABLE
    DO
    UPDATE comment as A
	INNER JOIN (SELECT comment_id, count(*) as cnt FROM comment_like GROUP BY comment_id) as B
	ON B.comment_id=A.id
	SET A.like_count=B.cnt
	WHERE B.comment_id=A.id;

-- drop index: username, slug, title
-- 우선 각종 id나 unique 제약 조건을 위한 index는 모두 유지
