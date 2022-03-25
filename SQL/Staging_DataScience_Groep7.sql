CREATE TABLE "actors" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "music_video" varchar,
  "show_title" varchar,
  "release_date" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "type_of_show" varchar,
  "scenes_deleted" varchar,
  "voice_actor" varchar,
  "credit_only" varchar,
  "archive_footage" varchar,
  "also_known_as" varchar,
  "uncredited" varchar,
  "suspended" varchar,
  "rumored" varchar,
  "character_name" varchar,
  "segment" varchar,
  "motion_capture" varchar,
  "role_position" int
);

CREATE TABLE "actresses" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "music_video" varchar,
  "show_title" varchar,
  "release_date" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "type_of_show" varchar,
  "scenes_deleted" varchar,
  "voice_actor" varchar,
  "credit_only" varchar,
  "archive_footage" varchar,
  "also_known_as" varchar,
  "uncredited" varchar,
  "suspended" varchar,
  "rumored" varchar,
  "character_name" varchar,
  "segment" varchar,
  "motion_capture" varchar,
  "role_position" int
);

CREATE TABLE "cinematographers" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "type_of_cinematographer" varchar,
  "video" varchar,
  "also_known_as" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" varchar,
  "credit_only" varchar,
  "archived_footage" varchar,
  "uncredited" varchar,
  "rumored" varchar,
  "motion_capture" varchar
);

CREATE TABLE "countries" (
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "countries_of_origin" varchar
);

CREATE TABLE "directors" (
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar,
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "type_of_director" varchar,
  "video" varchar,
  "also_known_as" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" varchar,
  "credit_only" varchar,
  "archived_footage" varchar,
  "uncredited" varchar,
  "rumored" varchar,
  "motion_capture" varchar
);

CREATE TABLE "genres" (
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "genre" varchar
);

CREATE TABLE "movies" (
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "release_year" varchar,
  "end_year" varchar
);

CREATE TABLE "ratings" (
  "distribution" varchar,
  "amount_of_votes" int,
  "rating" float,
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar
);

CREATE TABLE "running_time" (
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "country" varchar,
  "running_time" int,
  "including_commercials" varchar,
  "amount_of_episodes" varchar,
  "amount_of_parts" int,
  "season" varchar,
  "release_year" varchar,
  "end_year" varchar,
  "fps" varchar,
  "festival" varchar,
  "cut" varchar,
  "market" varchar,
  "print" varchar,
  "approximated" varchar

);

CREATE TABLE "plot" (
  "show_title" varchar,
  "music_video" varchar,
  "release_date" varchar,
  "type_of_show" varchar,
  "episode_title" varchar,
  "season_number" int,
  "episode_number" int,
  "suspended" varchar,
  "plot" varchar,
  "written_by" varchar
);
