CREATE TABLE "actors" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "character_name" varchar,
  "also_known_as" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" bool,
  "credit_only" bool,
  "archive_footage" bool,
  "uncredited" bool,
  "rumored" bool,
  "motion_capture" varchar,
  "role_position" int,
  "female" bool
);

CREATE TABLE "actresses" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "character_name" varchar,
  "also_known_as" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" bool,
  "credit_only" bool,
  "archive_footage" bool,
  "uncredited" bool,
  "rumored" bool,
  "motion_capture" varchar,
  "role_position" int,
  "female" bool
);

CREATE TABLE "cinematographers" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "type_of_cinematographer" varchar,
  "type_of_director" varchar,
  "also_known_as" varchar,
  "segment" varchar,
  "scenes_deleted" bool,
  "credit_only" bool,
  "archive_footage" bool,
  "uncredited" bool,
  "rumored" bool
);

CREATE TABLE "countries" (
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "countries_of_origin" varchar
);

CREATE TABLE "directors" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "type_of_director" varchar,
  "also_known_as" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" bool,
  "credit_only" bool,
  "archive_footage" bool,
  "uncredited" bool,
  "rumored" bool
);

CREATE TABLE "genres" (
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "genre" varchar
);

CREATE TABLE "movies" (
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "release_year" int,
  "end_year" varchar
);

CREATE TABLE "ratings" (
  "distribution" varchar,
  "amount_of_votes" int,
  "rating" float,
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool
);

CREATE TABLE "running_times" (
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "country" varchar,
  "running_times" int,
  "including_commercials" varchar,
  "amount_of_episodes" varchar,
  "season" varchar,
  "release_year" varchar,
  "end_year" varchar,
  "fps" varchar,
  "festival" varchar,
  "cut" varchar,
  "market" varchar,
  "print" varchar,
  "approximated" bool
);

CREATE TABLE "plot" (
  "show_title" varchar,
  "music_video" bool,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" bool,
  "plot" varchar,
  "written_by" varchar
);

CREATE VIEW get_known_as_actors (also_known_as)
as
SELECT DISTINCT also_known_as
FROM actors WHERE also_known_as IS NOT NULL;

CREATE VIEW get_known_as_actresses (also_known_as)
as
SELECT DISTINCT also_known_as
FROM actresses WHERE also_known_as IS NOT NULL;

CREATE VIEW get_known_as_cinematographers (also_known_as)
as
SELECT DISTINCT also_known_as
FROM cinematographers WHERE also_known_as IS NOT NULL;

CREATE VIEW get_known_as_directors (also_known_as)
as
SELECT DISTINCT also_known_as
FROM directors WHERE also_known_as IS NOT NULL;
