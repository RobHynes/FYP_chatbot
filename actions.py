from typing import Any, Text, Dict, List

import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import omdb
import tmdbsimple as tmdb
from datetime import datetime
import re


# Actor/writer/director question: "Who is Robert Downey Jr?" / "Who is Quentin Tarantino?"

class TmdbAction(Action):

    def name(self) -> Text:
        return "action_tmdb_api_call"  # "Tell me about the movie Superman" / "Who directed the movie Superman?"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gen_dict = {28: 'an action',
                    12: 'an adventure',
                    16: 'an animation',
                    35: 'a comedy',
                    80: 'a crime',
                    99: 'a documentary',
                    18: 'a drama',
                    10751: 'a family',
                    14: 'a fantasy',
                    36: 'a history',
                    27: 'a horror',
                    10402: 'a music',
                    9648: 'a mystery',
                    10749: 'a romance',
                    878: 'a science fiction',
                    10770: 'a tv movie',
                    53: 'a thriller',
                    10752: 'a war',
                    37: 'a western'}

        tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"
        search = tmdb.Search()

        # "Tell me about the movie Superman"
        if tracker.get_slot("title") is not None:

            title = next(tracker.get_latest_entity_values("title"))
            if tracker.get_slot("type") is not None:
                type = tracker.get_slot("type")
                if type == show:
                    response = search.tv(query=title)
                else:
                    response = search.movie(query=title)
            else:
                response = search.movie(query=title)

            id = response['results'][0]['id']
            movie = tmdb.Movies(id)
            title = response['results'][0]['title']
            g = response['results'][0]['genre_ids'][0]
            genre = gen_dict.get(g)

            credits = movie.credits()
            actor = credits['cast'][0]['name']
            release = movie.info()['release_date']
            plot = movie.info()['overview']

            crew = credits['crew']
            for person in crew:
                if person["department"] == "Directing":
                    director = person["name"]
                    break

            dispatcher.utter_message(
                title + " is " + genre + " movie starring " + actor + " and directed by " + director + ". It was released on " + release + "\nSummary: " + plot)
        else:
            dispatcher.utter_message("I don't understand your question")

        return []


class TmdbPersonAction(Action):

    def name(self) -> Text:
        return "action_person_tmdb"  # "Tell me about the movie Superman" / "Who directed the movie Superman?"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"
        search = tmdb.Search()

        if tracker.get_slot("PERSON") is not None:
            name = next(tracker.get_latest_entity_values("PERSON"))
            response = search.person(query=name)
            # id = response['results'][0]['id']
            if response['results']:
                role = response['results'][0]['known_for_department']
                if role == 'Acting':
                    role = 'an actor'
                elif role == 'Directing':
                    role = 'a director'
                elif role == 'Writing':
                    role = 'a writer'

                known_for = [response['results'][0]['known_for'][0],
                             response['results'][0]['known_for'][1],
                             response['results'][0]['known_for'][2]]
                movies = []

                for m in known_for:
                    if 'title' in m.keys():
                        movies.append(m.get('title'))
                    elif 'name' in m.keys():
                        movies.append(m.get('name'))

                name = response['results'][0]['name']

                dispatcher.utter_message(name + " is " + role + " known for " + movies[0] + ", " + movies[1] + " and " + movies[2])
            else:
                dispatcher.utter_message("I don't understand your question")
        else:
            dispatcher.utter_message("I don't understand your question")

        return []


class TmdbDateAction(Action):

    def name(self) -> Text:
        return "action_date_tmdb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"
        discover = tmdb.Discover()

        is_year = False
        movies = []

        if tracker.get_slot("DATE") is not None:  # what movies released on x date
            date = next(tracker.get_latest_entity_values("DATE"))

            date = date.replace("the ", "")
            date = date.replace("of ", "")
            p = re.compile(
                '\\s*[0-9]{1,2}st')  # matches 1 or 2 digits from 1 to 9 followed by st, occuring anywhere in string
            if p.search(date) is not None:
                sub = p.search(date).group()
                date = p.sub("", date)
                sub = sub.replace('st', ' ')
                print(sub)
                date = sub.lstrip() + date
            else:
                date = date.replace("nd", "")
                date = date.replace("rd", "")
                date = date.replace("th", "")

            print(date)

            try:
                date_object = datetime.strptime(date, '%d %B %Y').date()
                is_year = False
                print("1")
            except ValueError:
                try:
                    date_object = datetime.strptime(date, '%B %d %Y').date()
                    is_year = False
                    print("2")
                except ValueError:
                    try:
                        date_object = datetime.strptime(date, '%Y').date()
                        is_year = True
                        print("3")
                    except ValueError:
                        print(date)
                        dispatcher.utter_message("I don't understand your question")
                        dispatcher.utter_message(
                            'If you are asking about a date, try it in the format of "1st January 2020" or "January 1st 2020"')
                        print("4")
                        return []

            if is_year:
                release = date_object.strftime("%Y")
                response = discover.movie(primary_release_year=release)
            else:
                release = date_object.strftime("%B %d %Y")
                response = discover.movie(primary_release_date_gte=release, primary_release_date_lte=release)

            if response['results']:
                for i in range(0, 3):
                    movies.append(response['results'][i]['title'])
                    if len(movies) == 3:
                        break

            titles = ""

            if len(movies) == 0:
                dispatcher.utter_message("No movies were released on that day")
                return[]
            elif len(movies) == 1:
                titles = movies[0]
            elif len(movies) == 2:
                titles = movies[0] + " and " + movies[1]
            else:
                titles = movies[0] + " , " + movies[1] + " and " + movies[2]

            if tracker.get_slot("genre") is not None:
                genre = next(tracker.get_latest_entity_values("genre"))
                if is_year:
                    dispatcher.utter_message("The most popular " + genre + " movies from that year were " + titles)
                else:
                    dispatcher.utter_message("The most popular " + genre + " movies from that date were " + titles)
            else:
                if is_year:
                    dispatcher.utter_message("The most popular movies from that year were " + titles)
                else:
                    dispatcher.utter_message("The most popular movies from that date were " + titles)

        elif tracker.get_slot("title") is not None:  # what date did x movie release
            title = next(tracker.get_latest_entity_values("title"))
            response = search.movie(query=title)
            movie_id = response['results'][0]['id']
            movie = tmdb.Movies(movie_id)
            title = response['results'][0]['title']
            release = movie.info()['release_date']
            dispatcher.utter_message(title + "was released on " + release)
        else:
            dispatcher.utter_message("I don't understand your question")
        return []


class TmdbRoleAction(Action):

    def name(self) -> Text:
        return "action_role_tmdb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"
        search = tmdb.Search()
        # movie_credits = None

        if tracker.get_slot("action") is not None:

            action = next(tracker.get_latest_entity_values("action"))

            if tracker.get_slot("title") is not None:
                title = next(tracker.get_latest_entity_values("title"))
                response = search.movie(query=title)
                movieID = response['results'][0]['id']
                movie = tmdb.Movies(movieID)
                title = response['results'][0]['title']

                movie_credits = movie.credits()
                crew = movie_credits['crew']

                if action == 'starred':
                    action = 'starred in'
                    name = movie_credits['cast'][0]['name']

                elif action == 'directed':
                    for person in crew:
                        if person["department"] == "Directing":
                            name = person["name"]
                            break

                elif action == 'wrote':
                    for person in crew:
                        if person["department"] == "Writing":
                            name = person["name"]
                            break

                dispatcher.utter_message(name + " " + action + " " + title)  # Who stars in X? PERSON stars in X

            elif tracker.get_slot("PERSON") is not None:
                name = next(tracker.get_latest_entity_values("PERSON"))
                response = search.person(query=name)
                role = response['results'][0]['known_for_department']

                movies = [response['results'][0]['known_for'][0]['title'],
                          response['results'][0]['known_for'][1]['title'],
                          response['results'][0]['known_for'][2]['title']]

                if action == 'starred':
                    action = 'starring in'
                elif action == 'directed':
                    action = 'directing'
                elif action == 'wrote':
                    action = 'writing'

                # what movies has PERSON starred in? they have starred in xyz
                dispatcher.utter_message(
                    name + " is known for " + action + " " + movies[0] + ", " + movies[1] + " and " + movies[2])
        else:
            dispatcher.utter_message("I don't understand your question")
        return []


class TmdbGenreAction(Action):  # tell me about action movies from 2018

    def name(self) -> Text:
        return "action_genre_tmdb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"
        discover = tmdb.Discover()

        gen_dict = {28: 'action',
                    12: 'adventure',
                    16: 'animation',
                    35: 'comedy',
                    80: 'crime',
                    99: 'documentary',
                    18: 'drama',
                    10751: 'family',
                    14: 'fantasy',
                    36: 'history',
                    27: 'horror',
                    10402: 'music',
                    9648: 'mystery',
                    10749: 'romance',
                    878: 'science fiction',
                    10770: 'tv movie',
                    53: 'thriller',
                    10752: 'war',
                    37: 'western'}

        is_year = None
        movies = []

        if tracker.get_slot("genre") is not None:  # tell me about action movies from 2018 -> get the genre and year (not full date)

            genre = next(tracker.get_latest_entity_values("genre"))
            genreID = list(gen_dict.keys())[list(gen_dict.values()).index(genre)]

            if tracker.get_slot("DATE") is not None:
                date = next(tracker.get_latest_entity_values("DATE"))

                p = re.compile(
                    '\\s[0-9]{1,2}st')  # matches 1 or 2 digits from 1 to 9 followed by st, occuring anywhere in string
                if p.search(date) is not None:
                    sub = p.search(date).group()
                    date = p.sub("", date)
                    sub = sub.replace('st', ' ')
                    date = sub.lstrip() + date
                else:
                    date = date.replace("nd", "")
                    date = date.replace("rd", "")
                    date = date.replace("th", "")

                try:
                    date_object = datetime.strptime(date, '%d %B %Y').date()
                    is_year = False
                except ValueError:
                    try:
                        date_object = datetime.strptime(date, '%B %d %Y').date()
                        is_year = False
                    except ValueError:
                        try:
                            date_object = datetime.strptime(date, '%Y').date()
                            is_year = True
                        except ValueError:
                            dispatcher.utter_message("I don't understand your question")
                            dispatcher.utter_message(
                                'If you are asking about a date, try it in the format of "1st of January 2020" or "January 1st 2020"')
                            return []

                if is_year:
                    release = date_object.strftime("%Y")
                    response = discover.movie(primary_release_year=release, with_genres=genreID)
                else:
                    release = date_object.strftime("%B %d %Y")
                    response = discover.movie(primary_release_date_gte=release,
                                              primary_release_date_lte=release, with_genres=genreID)

                if response['results']:
                    for i in range(0, 3):
                        movies.append(response['results'][i]['title'])
                        if len(movies) == 3:
                            break

                titles = ""

                if len(movies) == 0:
                    dispatcher.utter_message("No " + genre + " movies were released on that day")
                elif len(movies) == 1:
                    titles = movies[0]
                elif len(movies) == 2:
                    titles = movies[0] + " and " + movies[1]
                else:
                    titles = movies[0] + " , " + movies[1] + " and " + movies[2]

                # the most popular GENRE movies released IN YEAR/ ON JANUARY 1ST YEAR/ ON
                if is_year:
                    dispatcher.utter_message("The most popular " + genre + " movies from that year were " + titles)
                else:
                    dispatcher.utter_message("The most popular " + genre + " movies from that date were " + titles)

        else:  # genre, date, type
            dispatcher.utter_message("I don't understand your question")  # tell me about action movies from 2018
        return []

