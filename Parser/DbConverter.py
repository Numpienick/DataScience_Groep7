from DbConnector import *
from Parser.classes.Plot import Plot


def convert_db():
    convert("ratings")
    convert("plot")
    # add_indices()


def convert(table):
    table.insert_table(table.get_table())


def add_indices():
    print("Creating indices")
    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = "CREATE INDEX idx_rating ON rating(rating);"
                cur.execute(command)
                command = "CREATE INDEX idx_person_last_name ON person(last_name);"
                cur.execute(command)
                command = "CREATE INDEX idx_show_info_show_title ON show_info(show_title);"
                cur.execute(command)
                print("Finished creating indices")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_rating(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "SELECT distribution, amount_of_votes, rating, show_title, release_date, episode_title, season_number, episode_number FROM {}"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_rating(ratings):
    print("Inserting rating")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE "temp" (
                        "distribution" varchar,
                        "amount_of_votes" int,
                        "rating" float,
                        "show_title" varchar,
                        "release_date" varchar,
                        "episode_title" varchar,
                        "season_number" int,
                        "episode_number" int
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (distribution, amount_of_votes, rating, show_title, release_date, episode_title, season_number, episode_number) VALUES %s",
                               ratings)
                # command = """
                #               SELECT DISTINCT show.show_info_id, temp.distribution, temp.amount_of_votes, temp.rating
                #               FROM temp
                #               LEFT JOIN show
                #               ON temp.show_title = show.show_title
                #               AND temp.release_date = show.release_date
                #           """
                # cur.execute(command)
                # data = cur.fetchmany(100)
                # execute_values(cur,
                #                "INSERT INTO rating (show_info_id, distribution, amount_of_votes, rating) VALUES %s",
                #                data)
                # command = """
                #               SELECT DISTINCT episode.show_info_id, temp.distribution, temp.amount_of_votes, temp.rating
                #               FROM temp
                #               LEFT JOIN episode
                #               ON temp.show_title = episode.show_title
                #               AND temp.release_date = episode.release_date
                #               AND temp.episode_title = episode.episode_name
                #               AND temp.season_number = episode.season_number
                #               AND temp.episode_number = episode.episode_number
                #           """
                # cur.execute(command)
                # data = cur.fetchmany(100)
                # execute_values(cur,
                #                "INSERT INTO rating (show_info_id, distribution, amount_of_votes, rating) VALUES %s",
                #                data)
                command = """
                              SELECT show_info.show_info_id, temp.distribution, temp.amount_of_votes, temp.rating
                              FROM temp
                              LEFT JOIN show_info
                              ON temp.show_title = show_info.show_title
                              AND temp.release_date = show_info.release_date 
                          """
                cur.execute(command)
                data = cur.fetchmany(100)
                execute_values(cur,
                               "INSERT INTO rating (show_info_id, distribution, amount_of_votes, rating) VALUES %s",
                               data)

                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_show(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                command = "SELECT show_title, release_date, release_year, type_of_show, suspended, end_year FROM {} WHERE end_year IS NOT NULL AND release_date <> '????'"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_show(show):
    print("Inserting show")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO show (show_title, release_date, release_year, type_of_show, suspended, end_year) VALUES %s",
                               show)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_episode(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                command = "SELECT show_title, release_date, release_year, type_of_show, suspended, episode_title, season_number, episode_number FROM {} WHERE (end_year IS NULL) AND (release_date IS NOT NULL) AND ((episode_title IS NOT NULL OR season_number IS NOT NULL) OR episode_number IS NOT NULL)"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_episode(episode):
    print("Inserting episode")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        show_title varchar,
                        release_date varchar,
                        release_year varchar,
                        type_of_show varchar,
                        "suspended" bool,
                        "episode_name" varchar,
                        "season_number" int,
                        "episode_number" int
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (show_title, release_date, release_year, type_of_show, suspended, episode_name, season_number, episode_number) VALUES %s",
                               episode)
                command = """
                          SELECT temp.show_title, temp.release_date, temp.release_year, temp.type_of_show, temp.suspended, show.show_id, temp.episode_name, temp.season_number, temp.episode_number 
                          FROM temp
                          LEFT JOIN show
                          ON temp.show_title = show.show_title
                          AND temp.release_date = show.release_date
                          """
                cur.execute(command)
                data = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO episode (show_title, release_date, release_year, type_of_show, suspended, show_id, episode_name, season_number, episode_number) VALUES %s",
                               data)
                command = "DROP TABLE temp"
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_showinfo(table):
    print("Getting " + table)
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                command = "UPDATE movies SET release_year = null WHERE release_year = '????'"
                cur.execute(command)
                command = "UPDATE movies SET suspended = true WHERE suspended is not NULL "
                cur.execute(command)
                command = "UPDATE movies SET suspended = false WHERE suspended is NULL "
                cur.execute(command)
                command = "SELECT show_title, release_date, release_year, type_of_show, suspended FROM {} WHERE episode_title is NULL AND season_number is NULL AND episode_number is NULL AND end_year is NULL"
                cur.execute(sql.SQL(command).format(sql.Literal(AsIs(table))))
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_showinfo(show_info):
    print("Inserting show_info")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO show_info (show_title, release_date, release_year, type_of_show, suspended) VALUES %s",
                               show_info)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_known_as(table):
    print("Getting " + table + " from staging")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                if table == "actors":
                    cur.execute("SELECT * from get_known_as_actors")
                    data = cur.fetchall()
                    return data
                if table == "actresses":
                    cur.execute("SELECT * from get_known_as_actresses")
                    data = cur.fetchall()
                    return data
                if table == "cinematographers":
                    cur.execute("SELECT * from get_known_as_cinematographers")
                    data = cur.fetchall()
                    return data
                if table == "directors":
                    cur.execute("SELECT * from get_known_as_directors")
                    data = cur.fetchall()
                    return data
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_ratings():
    print("Getting ratings")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT distribution, amount_of_votes, rating FROM ratings")
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_ratings(ratings):
    print("Inserting ratings")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur, "INSERT INTO rating (distribution, amount_of_votes, rating) VALUES %s", ratings)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()

    """
    Inserts person (actor, actress, director or cinematographer) to final db from staging db

    :param person: is the list of tuples to be inserted
    :param type: is the type of person, can be either: actors, actresses, cinematographers or directors
    """


def insert_person(person, type):
    print("Inserting role")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                # TODO: show_info_id
                if type == "actors" or type == "actresses":
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, character_name, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored, motion_capture, role_position) VALUES %s",
                                   person)
                if type == "cinematographers":
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, type_of_cinematographer, segment, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                                   person)
                if type == "directors":
                    execute_values(cur,
                                   "INSERT INTO role (show_info_id, nick_name, last_name, first_name, type_of_director, character_name, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                                   person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_known_as(known_as):
    print("Inserting known_as")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO also_known_as (also_known_as) VALUES %s RETURNING also_known_as_id;",
                               known_as)
                test = cur.fetchall()
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()
