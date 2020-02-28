# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import omdb
import tmdbsimple as tmdb


def main():
    tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"

    search = tmdb.Search()
    response = search.movie(query='die hard')
    id = response['results'][0]['id']
    movie = tmdb.Movies(id)
    print(movie.info())


class OmdbAction(Action):

    def name(self) -> Text:
        return "action_omdb_api_call"

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
            response = search.movie(query=title)
            id = response['results'][0]['id']
            movie = tmdb.Movies(id)
            title = response['results'][0]['title']
            g = response['results'][0]['genre_ids'][0]
            genre = gen_dict.get(g)

            credits = movie.credits()
            crew = credits['crew']
            actor = credits['cast'][0]['name']
            release = movie.info()['release_date']
            plot = movie.info()['overview']
            dispatcher.utter_message(
                title + " is " + genre + " movie starring " + actor + ". It was released " + release + "\nSummary: " + plot)
        # elif tracker.get_slot("role") is not None: # a person
        #     role = next(tracker.get_latest_entity_values("role"))
        #     response = search.person(query=role)
        #     id = response['results'][0]['id']
        #     # person = tmdb.People(id)
        #     name = person.info()
        #     dispatcher.utter_message(name)
        else:
            dispatcher.utter_message("I don't understand your question")

        return []


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
            response = search.movie(query=title)
            id = response['results'][0]['id']
            movie = tmdb.Movies(id)
            title = response['results'][0]['title']
            g = response['results'][0]['genre_ids'][0]
            genre = gen_dict.get(g)

            credits = movie.credits()
            crew = credits['crew']
            actor = credits['cast'][0]['name']
            release = movie.info()['release_date']
            plot = movie.info()['overview']
            dispatcher.utter_message(
                title + " is " + genre + " movie starring " + actor + ". It was released " + release + "\nSummary: " + plot)
        # elif tracker.get_slot("role") is not None: # a person
        #     role = next(tracker.get_latest_entity_values("role"))
        #     response = search.person(query=role)
        #     id = response['results'][0]['id']
        #     # person = tmdb.People(id)
        #     name = person.info()
        #     dispatcher.utter_message(name)
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
            id = response['results'][0]['id']
            role = response['results'][0]['known_for_department']
            if role == 'Acting':
                role = 'an actor'
            elif role == 'Directing':
                role = 'a director'
            elif role == 'Writing':
                role = 'a writer'
            movies = [response['results'][0]['known_for'][0]['title'],
                      response['results'][0]['known_for'][1]['title'],
                      response['results'][0]['known_for'][2]['title']]

            name = response['results'][0]['name']

            if tracker.get_slot("type") is not None:
                dispatcher.utter_message(name + " is known for " + movies[0] + ", " + movies[1] + " and " + movies[2])
            else:
                dispatcher.utter_message(
                    name + " is " + role + " known for " + movies[0] + ", " + movies[1] + " and " + movies[2])
        else:
            dispatcher.utter_message("I don't understand your question")

        return []


class TmdbDateAction(Action):

    def name(self) -> Text:
        return "action_date_tmdb"  # "Tell me about the movie Superman" / "Who directed the movie Superman?"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"
        search = tmdb.Search()

        if tracker.get_slot("DATE") is not None:
            date = next(tracker.get_latest_entity_values("DATE"))
            if tracker.get_slot("title") is not None:
                title = next(tracker.get_latest_entity_values("title"))
                response = search.movie(query=title)
                id = response['results'][0]['id']
                movie = tmdb.Movies(id)
                title = response['results'][0]['title']
                dispatcher.utter_message()
        else:
            dispatcher.utter_message("I don't understand your question")
        return []


main()

