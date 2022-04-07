CREATE TABLE "person" (
  "person_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "nick_name" varchar,
  "last_name" varchar,
  "first_name" varchar NOT NULL
);

CREATE TABLE "also_known_as" (
  "also_known_as_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "also_known_as" varchar UNIQUE NOT NULL
);

CREATE TABLE "person_also_known_as" (
  "person_id" int NOT NULL,
  "also_known_as_id" int NOT NULL,
  PRIMARY KEY ("person_id", "also_known_as_id")
);

CREATE TABLE "role" (
  "role_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "show_info_id" int NOT NULL,
  "character_name" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" varchar,
  "credit_only" varchar,
  "archive_footage" varchar,
  "uncredited" varchar,
  "rumored" varchar,
  "motion_capture" varchar,
  "role_position" int,
  "female" bool NOT NULL
) inherits ("person");

CREATE TABLE "cinematographer" (
  "cinematographer_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "type_of_cinematographer" varchar,
  "type_of_director" varchar,
  "segment" varchar,
  "scenes_deleted" varchar,
  "credit_only" bool,
  "archive_footage" bool,
  "uncredited" bool,
  "rumored" bool
) inherits ("person");

CREATE TABLE "director" (
  "director_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "type_of_director" varchar,
  "segment" varchar,
  "voice_actor" varchar,
  "scenes_deleted" varchar,
  "credit_only" varchar,
  "archive_footage" varchar,
  "uncredited" varchar,
  "rumored" varchar
) inherits ("person");

CREATE TABLE "show_info" (
  "show_info_id" SERIAL UNIQUE PRIMARY KEY,
  "rating_id" int NOT NULL,
  "show_title" varchar NOT NULL,
  "release_date" varchar,
  "release_year" int,
  "type_of_show" varchar,
  "suspended" bool
);

CREATE TABLE "episode" (
  "episode_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "show_id" int NOT NULL,
  "episode_name" varchar,
  "season_number" int,
  "episode_number" int
) inherits ("show_info");

CREATE TABLE "show" (
  "show_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "end_year" varchar
) inherits ("show_info");

CREATE TABLE "country" (
  "country_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "country_name" varchar NOT NULL
);

CREATE TABLE "genre" (
  "genre_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "genre_name" varchar NOT NULL
);

CREATE TABLE "running_times" (
  "running_times_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "country_id" int,
  "running_times" int NOT NULL,
  "including_commercials" bool,
  "amount_of_episodes" int,
  "fps" int,
  "festival" varchar,
  "cut" varchar,
  "market" varchar,
  "print" varchar,
  "approximated" bool
);

CREATE TABLE "rating" (
  "rating_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "distribution" varchar,
  "amount_of_votes" int,
  "rating" float
);

CREATE TABLE "plot" (
  "plot_id" SERIAL UNIQUE PRIMARY KEY NOT NULL,
  "plot" varchar NOT NULL,
  "written_by" varchar
);

CREATE TABLE "show_info_country" (
  "show_info_id" int NOT NULL,
  "country_id" int NOT NULL,
  PRIMARY KEY ("show_info_id", "country_id")
);

CREATE TABLE "show_info_genre" (
  "show_info_id" int NOT NULL,
  "genre_id" int NOT NULL,
  PRIMARY KEY ("show_info_id", "genre_id")
);

CREATE TABLE "show_info_running_times" (
  "show_info_id" int NOT NULL,
  "running_times_id" int NOT NULL,
  PRIMARY KEY ("show_info_id", "running_times_id")
);

CREATE TABLE "show_info_cinematographer" (
  "show_info_id" int NOT NULL,
  "cinematographer_id" int NOT NULL,
  PRIMARY KEY ("show_info_id", "cinematographer_id")
);

CREATE TABLE "show_info_director" (
  "show_info_id" int NOT NULL,
  "director_id" int NOT NULL,
  PRIMARY KEY ("show_info_id", "director_id")
);

CREATE TABLE "show_info_plot" (
  "show_info_id" int NOT NULL,
  "plot_id" int NOT NULL,
  PRIMARY KEY ("show_info_id", "plot_id")
);

ALTER TABLE "person_also_known_as" ADD FOREIGN KEY ("person_id") REFERENCES "person" ("person_id");

ALTER TABLE "person_also_known_as" ADD FOREIGN KEY ("also_known_as_id") REFERENCES "also_known_as" ("also_known_as_id");

ALTER TABLE "role" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info" ADD FOREIGN KEY ("rating_id") REFERENCES "rating" ("rating_id");

ALTER TABLE "episode" ADD FOREIGN KEY ("show_id") REFERENCES "show" ("show_id");

ALTER TABLE "running_times" ADD FOREIGN KEY ("country_id") REFERENCES "country" ("country_id");

ALTER TABLE "show_info_country" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_country" ADD FOREIGN KEY ("country_id") REFERENCES "country" ("country_id");

ALTER TABLE "show_info_genre" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_genre" ADD FOREIGN KEY ("genre_id") REFERENCES "genre" ("genre_id");

ALTER TABLE "show_info_running_times" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_running_times" ADD FOREIGN KEY ("running_times_id") REFERENCES "running_times" ("running_times_id");

ALTER TABLE "show_info_cinematographer" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_cinematographer" ADD FOREIGN KEY ("cinematographer_id") REFERENCES "cinematographer" ("cinematographer_id");

ALTER TABLE "show_info_director" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_director" ADD FOREIGN KEY ("director_id") REFERENCES "director" ("director_id");

ALTER TABLE "show_info_plot" ADD FOREIGN KEY ("show_info_id") REFERENCES "show_info" ("show_info_id");

ALTER TABLE "show_info_plot" ADD FOREIGN KEY ("plot_id") REFERENCES "plot" ("plot_id");


COMMENT ON TABLE "person" IS 'Master of role, cinematographer and director';

COMMENT ON TABLE "role" IS 'Detail of person';

COMMENT ON TABLE "cinematographer" IS 'Detail of person';

COMMENT ON TABLE "director" IS 'Detail of person';

COMMENT ON TABLE "show_info" IS 'Master of show and episode';

COMMENT ON TABLE "episode" IS 'Detail of show_info';

COMMENT ON TABLE "show" IS 'Detail of show_info';

CREATE VIEW movie_rating_actrice_count
AS
SELECT show_info.show_title, rating.rating, COUNT(role.female) AS total_female_roles
    FROM ONLY show_info
INNER JOIN rating
    ON show_info.rating_id = rating.rating_id
INNER JOIN role
    ON show_info.show_info_id = role.show_info_id
    WHERE role.female = true AND rating.rating IS NOT NULL
GROUP BY show_info.show_title, rating.rating