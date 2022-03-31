CREATE TABLE "person" (
  "person_id" SERIAL PRIMARY KEY,
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar
);

CREATE TABLE "also_known_as" (
  "also_known_as_id" SERIAL PRIMARY KEY,
  "also_known_as" varchar
);

CREATE TABLE "person_also_known_as" (
  "person_id" int,
  "also_known_as_id" int
);

CREATE TABLE "role" (
  "role_id" SERIAL PRIMARY KEY,
  "show_info_id" int,
  "character_name" varchar,
  "segment" varchar,
  "role_position" int,
  "scenes_deleted" bool,
  "voice_actor" varchar,
  "motion_capture" bool,
  "female" bool
);

CREATE TABLE "cinematographer" (
  "cinematographer_id" SERIAL PRIMARY KEY,
  "uncredited" bool,
  "credit_only" bool,
  "archive_footage" bool,
  "rumored" bool
);

CREATE TABLE "director" (
  "director_id" SERIAL PRIMARY KEY,
  "collaborating" bool
);

CREATE TABLE "show_info" (
  "show_info_id" SERIAL PRIMARY KEY,
  "show_title" varchar,
  "release_date" varchar,
  "release_year" date,
  "type_of_show" varchar,
  "suspended" bool
);

CREATE TABLE "episode" (
  "episode_id" SERIAL PRIMARY KEY,
  "show_id" int,
  "episode_name" varchar,
  "season_number" int,
  "episode_number" int
);

CREATE TABLE "show" (
  "show_id" SERIAL PRIMARY KEY,
  "end_year" int
);

CREATE TABLE "country" (
  "country_id" SERIAL PRIMARY KEY,
  "country_name" varchar
);

CREATE TABLE "genre" (
  "genre_id" SERIAL PRIMARY KEY,
  "genre_name" varchar
);

CREATE TABLE "running_time" (
  "running_time_id" SERIAL PRIMARY KEY,
  "country_id" int,
  "running_time" int,
  "approximated" bool,
  "including_commercials" bool,
  "amount_of_parts" int,
  "amount_of_episodes" int,
  "fps" int,
  "festival" varchar,
  "cut" varchar,
  "market" varchar,
  "print" varchar
);

CREATE TABLE "rating" (
  "rating_id" SERIAL PRIMARY KEY,
  "show_info_id" int,
  "distribution" varchar,
  "amount_of_votes" int,
  "rating" float
);

CREATE TABLE "plot" (
  "plot_id" SERIAL PRIMARY KEY,
  "plot" varchar,
  "written_by" varchar
);

CREATE TABLE "show_info_country" (
  "show_info_id" int,
  "country_id" int,
  PRIMARY KEY ("show_info_id", "country_id")
);

CREATE TABLE "show_info_genre" (
  "show_info_id" int,
  "genre_id" int,
  PRIMARY KEY ("show_info_id", "genre_id")
);

CREATE TABLE "show_info_running_time" (
  "show_info_id" int,
  "running_time_id" int,
  PRIMARY KEY ("show_info_id", "running_time_id")
);

CREATE TABLE "show_info_cinematographer" (
  "show_info_id" int,
  "cinematographer_id" int,
  PRIMARY KEY ("show_info_id", "cinematographer_id")
);

CREATE TABLE "show_info_director" (
  "show_info_id" int,
  "director_id" int,
  PRIMARY KEY ("show_info_id", "director_id")
);

CREATE TABLE "show_info_plot" (
  "show_info_id" int,
  "plot_id" int,
  PRIMARY KEY ("show_info_id", "plot_id")
);

ALTER TABLE "person_also_known_as" ADD FOREIGN KEY ("person_id") REFERENCES "person" ("person_id");

ALTER TABLE "person_also_known_as" ADD FOREIGN KEY ("also_known_as_id") REFERENCES "also_known_as" ("also_known_as_id");

ALTER TABLE "role" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

AlTER TABLE "rating" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "episode" ADD FOREIGN KEY ("show_id") REFERENCES "show" ("show_id");

ALTER TABLE "running_time" ADD FOREIGN KEY ("country_id") REFERENCES "country" ("country_id");

ALTER TABLE "show_info_country" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_country" ADD FOREIGN KEY ("country_id") REFERENCES "country" ("country_id");

ALTER TABLE "show_info_genre" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_genre" ADD FOREIGN KEY ("genre_id") REFERENCES "genre" ("genre_id");

ALTER TABLE "show_info_running_time" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_running_time" ADD FOREIGN KEY ("running_time_id") REFERENCES "running_time" ("running_time_id");

ALTER TABLE "show_info_cinematographer" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_cinematographer" ADD FOREIGN KEY ("cinematographer_id") REFERENCES "cinematographer" ("cinematographer_id");

ALTER TABLE "show_info_director" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_director" ADD FOREIGN KEY ("director_id") REFERENCES "director" ("director_id");

ALTER TABLE "show_info_plot" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_plot" ADD FOREIGN KEY ("plot_id") REFERENCES "plot" ("plot_id");

