from DbConnector import *


def convert_db():
    convert("ratings")


def convert(table):
    match (table):
        case "actors":
            insert_role(get_persons(table))  # TODO: under show_info
        case "actresses":
            insert_role(get_persons(table))
        case "cinematographers":
            insert_cinematographer(get_persons(table))
        case "countries":
            insert_countries(get_countries(table))
        case "directors":
            insert_director(get_persons(table))
        case "genres":
            insert_genres(get_genres(table))
        case "movies":
            insert_showinfo(get_showinfo(table))
            insert_show(get_show(table))
            insert_episode(get_episode(table))
        case "plot":
            insert_plot(get_plot(table))
        case "ratings":
            insert_rating(get_rating(table))
        case "running-times":
            print()


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
                command = "DROP TABLE temp"
                cur.execute(command)
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


def get_persons(table):
    print("Getting " + table + " from staging")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                if table == "actors":
                    cur.execute("SELECT DISTINCT * from actors")
                    data = cur.fetchmany(100)
                if table == "actresses":
                    cur.execute("SELECT DISTINCT * from actresses")
                    data = cur.fetchmany(100)
                if table == "cinematographers":
                    cur.execute("SELECT DISTINCT * from cinematographers")
                    data = cur.fetchmany(100)
                if table == "directors":
                    cur.execute("SELECT DISTINCT * from directors")
                    data = cur.fetchmany(100)
                return data
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


def get_plot():
    print("Getting plot")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM plot")
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


def get_countries():
    print("Getting countries")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT countries_of_origin FROM countries")
                data = cur.fetchall()
                return data

    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def get_genres():
    print("Getting genres")
    try:
        conn = connect("staging")
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM genres")
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


def insert_plot(plot):
    print("Inserting plot")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        show_title varchar,
                        music_video varchar,
                        release_date varchar,
                        type_of_show varchar,
                        episode_title varchar,
                        season_number int,
                        episode_number int,
                        suspended varchar,
                        plot varchar,
                        written_by varchar
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, plot, written_by) VALUES %s",
                               plot)

                cur.execute("SELECT plot, written_by FROM temp")
                data = cur.fetchall()

                execute_values(cur,
                               "INSERT INTO genre (genre_name) VALUES %s",
                               data)

                command = """
                          SELECT show_info.show_info_id, plot.plot_id
                          FROM temp
                          LEFT JOIN show_info
                          ON temp.show_title = show_info.show_title
                          AND temp.release_date = show_info.release_date
                          JOIN plot
                          ON temp.plot = plot.plot
                          AND temp.written_by = plot.written_by
                          """
                cur.execute(command)
                link_table = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO show_info_plot (show_info_id, genre_id) VALUES %s",
                               link_table)
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


def insert_role(role):
    print("Inserting role")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        nick_name varchar,
                        last_name varchar,
                        first_name varchar,
                        show_title varchar,
                        music_video varchar,
                        release_date varchar,
                        type_of_show varchar,
                        episode_title varchar,
                        season_number int,
                        episode_number int,
                        suspended bool,
                        character_name varchar,
                        also_known_as varchar,
                        segment varchar,
                        voice_actor varchar,
                        scenes_deleted varchar,
                        credit_only varchar,
                        archive_footage varchar,
                        uncredited varchar,
                        rumored varchar,
                        motion_capture varchar,
                        role_position int,
                        female bool
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (nick_name, last_name, first_name, show_title, music_video, "
                               "release_date, type_of_show, episode_title, season_number, episode_number, suspended, "
                               "character_name, also_known_as, segment, voice_actor, scenes_deleted, credit_only, "
                               "archive_footage, uncredited, rumored, motion_capture, role_position, female) VALUES "
                               "%s",
                               role)
                command = """
                          SELECT show_info.show_info_id, temp.nick_name, temp.last_name, temp.first_name, temp.character_name, temp.segment, temp.voice_actor, temp.scenes_deleted, temp.credit_only, temp.archive_footage, temp.uncredited, temp.rumored, temp.motion_capture, temp.role_position, temp.female
                          FROM temp
                          LEFT JOIN show_info
                          ON temp.show_title = show_info.show_title
                          AND temp.release_date = show_info.release_date
                          """
                cur.execute(command)
                data = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO role (show_info_id, nick_name, last_name, first_name, character_name, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored, motion_capture, role_position, female) VALUES %s",
                               data)
                command = "DROP TABLE temp"
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_director(director):
    print("Inserting director")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        nick_name varchar,
                        last_name varchar,
                        first_name varchar,
                        show_title varchar,
                        music_video varchar,
                        release_date varchar,
                        type_of_show varchar,
                        episode_title varchar,
                        season_number int,
                        episode_number int,
                        suspended varchar,
                        type_of_director varchar,
                        video varchar,
                        also_known_as varchar,
                        segment varchar,
                        voice_actor varchar,
                        scenes_deleted varchar,
                        credit_only varchar,
                        archive_footage varchar,
                        uncredited varchar,
                        rumored varchar
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (nick_name, last_name, first_name, show_title, music_video, "
                               "release_date, type_of_show, episode_title, season_number, episode_number, suspended, "
                               "type_of_director, video, also_known_as, segment, voice_actor, scenes_deleted, "
                               "credit_only, archive_footage, uncredited, rumored) VALUES "
                               "%s",
                               director)
                cur.execute(
                    "SELECT nick_name, last_name, first_name, type_of_director, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored from temp")
                temp = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO director (nick_name, last_name, first_name, type_of_director, segment, voice_actor, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                               temp)

                command = """
                          SELECT show_info.show_info_id, director.director_id
                          FROM temp
                          LEFT JOIN show_info
                          ON temp.show_title = show_info.show_title
                          AND temp.release_date = show_info.release_date
                          JOIN director
                          ON temp.first_name = director.first_name
                          AND temp.last_name = director.last_name
                          AND temp.nick_name = director.nick_name
                          """
                cur.execute(command)
                data = cur.fetchall()

                execute_values(cur,
                               "INSERT INTO show_info_director (show_info_id, director_id) VALUES %s",
                               data)

                command = "DROP TABLE temp"
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_cinematographer(cinematographer):
    print("Inserting cinematographer")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        nick_name varchar,
                        last_name varchar,
                        first_name varchar,
                        show_title varchar,
                        music_video varchar,
                        release_date varchar,
                        type_of_show varchar,
                        episode_title varchar,
                        season_number int,
                        episode_number int,
                        suspended varchar,
                        type_of_cinematographer varchar,
                        type_of_director varchar,
                        video varchar,
                        also_known_as varchar,
                        segment varchar,
                        scenes_deleted varchar,
                        credit_only varchar,
                        archive_footage varchar,
                        uncredited varchar,
                        rumored varchar
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (nick_name, last_name, first_name, show_title, music_video, "
                               "release_date, type_of_show, episode_title, season_number, episode_number, suspended, "
                               "type_of_cinematographer, type_of_director, video, also_known_as, segment, scenes_deleted, "
                               "credit_only, archive_footage, uncredited, rumored) VALUES %s",
                               cinematographer)
                cur.execute(
                    "SELECT nick_name, last_name,first_name, type_of_cinematographer,type_of_director, segment, scenes_deleted, credit_only, archive_footage,uncredited, rumored from temp")
                temp = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO cinematographer (nick_name, last_name, first_name, type_of_cinematographer, type_of_director, segment, scenes_deleted, credit_only, archive_footage, uncredited, rumored) VALUES %s",
                               temp)

                command = """
                          SELECT show_info.show_info_id, cinematographer.cinematographer_id
                          FROM temp
                          LEFT JOIN show_info
                          ON temp.show_title = show_info.show_title
                          AND temp.release_date = show_info.release_date
                          JOIN cinematographer
                          ON temp.first_name = cinematographer.first_name
                          AND temp.last_name = cinematographer.last_name
                          AND temp.nick_name = cinematographer.nick_name
                          """
                cur.execute(command)
                data = cur.fetchall()

                execute_values(cur,
                               "INSERT INTO show_info_cinematographer (show_info_id, cinematographer_id) VALUES %s",
                               data)
                command = "DROP TABLE temp"
                cur.execute(command)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_known_as(knownAs):
    print("Inserting known_as")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                execute_values(cur,
                               "INSERT INTO also_known_as (also_known_as) VALUES %s RETURNING also_known_as_id;",
                               knownAs)
                test = cur.fetchall()
                # command = "INSERT INTO {} (nick_name, last_name, first_name) VALUES %s"
                # cur.execute_values(sql.SQL(command).format(sql.Literal(AsIs(table))), person)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_countries(countries):
    print("Inserting countries")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        show_title varchar,
                        music_video varchar,
                        release_date varchar,
                        type_of_show varchar,
                        episode_title varchar,
                        season_number int,
                        episode_number int,
                        suspended varchar,
                        countries_of_origin varchar
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, countries_of_origin) VALUES %s",
                               countries)

                cur.execute("SELECT DISTINCT countries_of_origin FROM temp")
                data = cur.fetchall()

                execute_values(cur,
                               "INSERT INTO country (countries_of_origin) VALUES %s",
                               data)

                command = """
                          SELECT show_info.show_info_id, country.country_id
                          FROM temp
                          LEFT JOIN show_info
                          ON temp.show_title = show_info.show_title
                          AND temp.release_date = show_info.release_date
                          JOIN country
                          ON temp.countries_of_origin = country.countries_of_origin
                          """
                cur.execute(command)
                link_table = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO show_info_country (show_info_id, country_id) VALUES %s",
                               link_table)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()


def insert_genres(genres):
    print("Inserting genres")

    try:
        conn = connect("final")
        with conn:
            with conn.cursor() as cur:
                command = (
                    """
                    CREATE TABLE temp (
                        show_title varchar,
                        music_video varchar,
                        release_date varchar,
                        type_of_show varchar,
                        episode_title varchar,
                        season_number int,
                        episode_number int,
                        suspended varchar,
                        genre varchar
                    )
                    """
                )
                cur.execute(command)
                execute_values(cur,
                               "INSERT INTO temp (show_title, music_video, release_date, type_of_show, episode_title, season_number, episode_number, suspended, genre) VALUES %s",
                               genres)

                cur.execute("SELECT DISTINCT genre FROM temp")
                data = cur.fetchall()

                execute_values(cur,
                               "INSERT INTO genre (genre_name) VALUES %s",
                               data)

                command = """
                          SELECT show_info.show_info_id, genre.genre_id
                          FROM temp
                          LEFT JOIN show_info
                          ON temp.show_title = show_info.show_title
                          AND temp.release_date = show_info.release_date
                          JOIN genre
                          ON temp.genre = genre.genre
                          """
                cur.execute(command)
                link_table = cur.fetchall()
                execute_values(cur,
                               "INSERT INTO show_info_genre (show_info_id, genre_id) VALUES %s",
                               link_table)
                print("did it")
    except Exception as err:
        raise err
    finally:
        if conn:
            conn.close()
