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


# Actor/writer/director question: "Who is Robert Downey Jr?" / "Who is Quentin Tarantino?"
# Complex Query: "How much money did the movie avatar make?" / "Which movie made more money, avatar or avengers"


def main():
    tmdb.API_KEY = "5ce7e4a66621977d06b1c0e75961699b"

    search = tmdb.Search()
    response = search.movie(query='die hard')
    id = response['results'][0]['id']
    movie = tmdb.Movies(id)
    print(movie.info())


class OmdbAction(Action):

    def name(self) -> Text:
        return "action_omdb_api_call"  # "Tell me about the movie Superman" / "Who directed the movie Superman?"

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

# {'page': 1, 'total_results': 1, 'total_pages': 1, 'results': [{'popularity': 17.647, 'known_for_department': 'Acting',
# 'name': 'Tom Hanks', 'id': 31, 'profile_path': '/xxPMucou2wRDxLrud8i2D4dsywh.jpg', 'adult': False, 'known_for':
# [{'poster_path': '/yE5d3BUhE8hCnkMUJOo1QDoOGNz.jpg', 'vote_count': 16392, 'video': False, 'media_type': 'movie',
# 'id': 13, 'adult': False, 'backdrop_path': '/wMgbnUVS9wbRGAdki8fqxKU1O0N.jpg', 'original_language': 'en',
# 'original_title': 'Forrest Gump', 'genre_ids': [35, 18, 10749], 'title': 'Forrest Gump', 'vote_average': 8.4,
# 'overview': 'A man with a low IQ has accomplished great things in his life and been present during significant
# historic events—in each case, far exceeding what anyone imagined he could do. But despite all he has achieved, his one
# true love eludes him.', 'release_date': '1994-07-06'}, {'vote_count': 11416, 'id': 862, 'video': False, 'media_type':
# 'movie', 'vote_average': 7.9, 'title': 'Toy Story', 'release_date': '1995-10-30', 'original_language': 'en',
# 'original_title': 'Toy Story', 'genre_ids': [16, 35, 10751], 'backdrop_path': '/dji4Fm0gCDVb9DQQMRvAI8YNnTz.jpg',
# 'adult': False, 'overview': "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz
# Lightyear onto the scene. Afraid of losing his place in Andy's heart, Woody plots against Buzz. But when circumstances
# separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences.", 'poster_path':
# '/rhIRbceoE9lR4veEXuwCC2wARtG.jpg'}, {'poster_path': '/mMltbSxwEdNE4Cv8QYLpzkHWTDo.jpg', 'vote_count': 9408, 'video':
# False, 'media_type': 'movie', 'id': 10193, 'adult': False, 'backdrop_path': '/y2qAjM37QgatWeG84DDtwsZuMW.jpg',
# 'original_language': 'en', 'original_title': 'Toy Story 3', 'genre_ids': [16, 35, 10751], 'title': 'Toy Story 3',
# 'vote_average': 7.8, 'overview': "Woody, Buzz, and the rest of Andy's toys haven't been played with in years. With
# Andy about to go to college, the gang find themselves accidentally left at a nefarious day care center. The toys must
# band together to escape and return home to Andy.", 'release_date': '2010-06-16'}], 'gender': 2}]}

# {'page': 1, 'total_results': 137, 'total_pages': 7, 'results': [{'popularity': 19.604, 'vote_count': 2061, 'video':
# False, 'poster_path': '/rLTdj7oB9oxsYwuweeglWRzRng7.jpg', 'id': 1924, 'adult': False, 'backdrop_path':
# '/nS0rEXPbkHI449SF6R4WUQvTVxE.jpg', 'original_language': 'en', 'original_title': 'Superman', 'genre_ids':
# [28, 12, 878], 'title': 'Superman', 'vote_average': 7, 'overview': 'Mild-mannered Clark Kent works as a reporter at
# the Daily Planet alongside his crush, Lois Lane. Clark must summon his superhero alter-ego when the nefarious Lex
# Luthor launches a plan to take over the world.', 'release_date': '1978-12-13'},
#
# {'popularity': 21.626, 'vote_count':
# 2570, 'video': False, 'poster_path': '/e3aLTaD5ppxo3en0GAGceekEPAe.jpg', 'id': 1452, 'adult': False, 'backdrop_path':
# '/uAVdwu4vEx0TwuC4ewp9RqplKEV.jpg', 'original_language': 'en', 'original_title': 'Superman Returns', 'genre_ids':
# [28, 12, 878], 'title': 'Superman Returns', 'vote_average': 5.6, 'overview': 'Superman returns to discover his 5-year
# absence has allowed Lex Luthor to walk free, and that those he was closest to felt abandoned and have moved on. Luthor
# plots his ultimate revenge that could see millions killed and change the face of the planet forever, as well as
# ridding himself of the Man of Steel.', 'release_date': '2006-06-28'}, {'popularity': 13.945, 'id': 9531, 'video':
# False, 'vote_count': 931, 'vote_average': 5.4, 'title': 'Superman III', 'release_date': '1983-06-17',
# 'original_language': 'en', 'original_title': 'Superman III', 'genre_ids': [35, 878, 28, 12], 'backdrop_path':
# '/pkqkxX7tkN0QLBtOYzugtBqyu0C.jpg', 'adult': False, 'overview': 'Aiming to defeat the Man of Steel, wealthy executive
# Ross Webster hires bumbling but brilliant Gus Gorman to develop synthetic kryptonite, which yields some unexpected
# psychological effects in the third installment of the 1980s Superman franchise. Between rekindling romance with his
# high school sweetheart and saving himself, Superman must contend with a powerful supercomputer.', 'poster_path':
# '/pDjfBk3YkdvRK2VERvoHaXJdNxF.jpg'}, {'popularity': 14.14, 'vote_count': 1261, 'video': False, 'poster_path':
# '/uvxjXSfph2FD07A2jBG9NHJnl27.jpg', 'id': 8536, 'adult': False, 'backdrop_path': '/1d0bPDy0Ud7g7vZ5qnKI6HsduLE.jpg', '
# original_language': 'en', 'original_title': 'Superman II', 'genre_ids': [28, 12, 878], 'title': 'Superman II',
# 'vote_average': 6.6, 'overview': "Three escaped criminals from the planet Krypton test the Man of Steel's mettle. Led
# by General Zod, the Kryptonians take control of the White House and partner with Lex Luthor to destroy Superman and
# rule the world. But Superman, who attempts to make himself human in order to get closer to Lois, realizes he has a
# responsibility to save the planet.", 'release_date': '1980-12-04'}, {'popularity': 24.517, 'vote_count': 12616,
# 'video': False, 'poster_path': '/cGOPbv9wA5gEejkUN892JrveARt.jpg', 'id': 209112, 'adult': False, 'backdrop_path':
# '/vsjBeMPZtyB7yNsYY56XYxifaQZ.jpg', 'original_language': 'en', 'original_title': 'Batman v Superman: Dawn of Justice',
# 'genre_ids': [28, 12, 14], 'title': 'Batman v Superman: Dawn of Justice', 'vote_average': 5.8, 'overview':
# 'Fearing the actions of a god-like Super Hero left unchecked, Gotham City’s own formidable, forceful vigilante takes
# on Metropolis’s most revered, modern-day savior, while the world wrestles with what sort of hero it really needs. And
# with Batman and Superman at war with one another, a new threat quickly arises, putting mankind in greater danger than
# it’s ever known before.', 'release_date': '2016-03-23'}, {'popularity': 8.451, 'vote_count': 186, 'video': False,
# 'poster_path': '/sbGj8yQeUlIDZdffsuFv4Cy9snk.jpg', 'id': 166076, 'adult': False, 'backdrop_path':
# '/mIbwk59WP9kcRA9pprpHD2cjFxi.jpg', 'original_language': 'en', 'original_title': 'Superman: Unbound', 'genre_ids':
# [28, 12, 16], 'title': 'Superman: Unbound', 'vote_average': 6.4, 'overview': 'Based on the Geoff Johns/Gary Frank 2008
# release "Superman: Brainiac," Superman: Unbound finds the horrific force responsible for the destruction of Krypton
# (Brainiac) descending upon Earth. Brainiac has crossed the universe, collecting cities from interesting planets,
# Kandor included, and now the all-knowing, ever-evolving android has his sights fixed on Metropolis. Superman must
# summon all of his physical and intellectual resources to protect his city, the love of his life, and his newly-arrived
# cousin, Supergirl.', 'release_date': '2013-05-06'}, {'popularity': 8.68, 'vote_count': 325, 'video': False,
# 'poster_path': '/wNtrbql45NqvomsYKr3uHXgFj2D.jpg', 'id': 45162, 'adult': False, 'backdrop_path':
# '/bMNEElThWSUgzFUOn5SYU4eHYXG.jpg', 'original_language': 'en', 'original_title': 'Superman/Batman: Apocalypse',
# 'genre_ids': [28, 12, 16, 878, 10751], 'title': 'Superman/Batman: Apocalypse', 'vote_average': 7, 'overview': 'Batman
# discovers a mysterious teen-aged girl with superhuman powers and a connection to Superman. When the girl comes to the
# attention of Darkseid, the evil overlord of Apokolips, events take a decidedly dangerous turn.', 'release_date':
# '2010-09-28'}, {'popularity': 8.769, 'id': 13640, 'video': False, 'vote_count': 277, 'vote_average': 6.6, 'title':
# 'Superman: Doomsday', 'release_date': '2007-09-18', 'original_language': 'en', 'original_title': 'Superman: Doomsday',
# 'genre_ids': [28, 16, 878, 10751], 'backdrop_path': '/amXWhCkrsN7p9S6rnLCgD9fNwE6.jpg', 'adult': False, 'overview':
# 'When LexCorps accidentally unleash a murderous creature, Doomsday, Superman meets his greatest challenge as a
# champion. Based on the "The Death of Superman" storyline that appeared in DC Comics\' publications in the 1990s',
# 'poster_path': '/3of4nShmv1hBmrebOQqGlfZ9ZL0.jpg'}, {'popularity': 8.357, 'vote_count': 213, 'video': False,
# 'poster_path': '/yVPzeI4OsJtJ5g17NM3ZBYdEVRW.jpg', 'id': 56590, 'adult': False, 'backdrop_path':
# '/FTpFec420ztDa6HSpwLxGuwzis.jpg', 'original_language': 'en', 'original_title': 'All Star Superman', 'genre_ids':
# [28, 12, 16], 'title': 'All Star Superman', 'vote_average': 6.8, 'overview': 'Lex Luthor enacts his plan to rid the
# world of Superman, once and for all. Succeeding with solar radiation poisoning, the Man of Steel is slowly dying. With
# what little times remains, the Last Son of Krypton must confront the revealing of his secret identity to Lois Lane and
# face Luthor in a final battle.', 'release_date': '2011-02-22'}, {'popularity': 14.652, 'vote_count': 304, 'video':
# False, 'poster_path': '/y0uxSHaSFmt6XaBJgjkeLqe7aM.jpg', 'id': 487670, 'adult': False, 'backdrop_path':
# '/wA1eufMEvM0RdQk24gj5yaDWLjQ.jpg', 'original_language': 'en', 'original_title': 'The Death of Superman', 'genre_ids':
# [28, 16, 18, 878], 'title': 'The Death of Superman', 'vote_average': 7.3, 'overview': 'When a hulking monster arrives
# on Earth and begins a mindless rampage, the Justice League is quickly called in to stop it. But it soon becomes
# apparent that only Superman can stand against the monstrosity.', 'release_date': '2018-07-03'}, {'popularity': 9.126,
# 'vote_count': 186, 'video': False, 'poster_path': '/cilpU63HE0nsbqMytvO3Mlltotw.jpg', 'id': 103269, 'adult': False,
# 'backdrop_path': '/9fRNgX2bI6f27sxFEFuCPNYY4Lv.jpg', 'original_language': 'en', 'original_title':
# 'Superman vs. The Elite', 'genre_ids': [28, 16], 'title': 'Superman vs. The Elite', 'vote_average': 6.8, 'overview':
# 'The Man of Steel finds himself outshone by a new team of ruthless superheroes who hold his idealism in contempt.',
# 'release_date': '2012-06-12'}, {'popularity': 10.615, 'id': 22855, 'video': False, 'vote_count': 318, 'vote_average':
# 6.8, 'title': 'Superman/Batman: Public Enemies', 'release_date': '2009-09-29', 'original_language': 'en',
# 'original_title': 'Superman/Batman: Public Enemies', 'genre_ids': [16, 28, 12, 10751], 'backdrop_path':
# '/aMyEMGuW2NV3A0whuEM7VKp6M73.jpg', 'adult': False, 'overview': 'United States President Lex Luthor uses the oncoming
# trajectory of a Kryptonite meteor to frame Superman and declare a $1 billion bounty on the heads of the Man of Steel
# and his ‘partner in crime’, Batman. Heroes and villains alike launch a relentless pursuit of Superman and Batman, who
# must unite—and recruit help—to try and stave off the action-packed onslaught, stop the meteor Luthors plot.', 'poster_
# path': '/bJBZxzFHfTAOtBg8fOCCaBmh4hF.jpg'}, {'popularity': 10.477, 'id': 11411, 'video': False, 'vote_count': 636,
# 'vote_average': 4.4, 'title': 'Superman IV: The Quest for Peace', 'release_date': '1987-07-23', 'original_language':
# 'en', 'original_title': 'Superman IV: The Quest for Peace', 'genre_ids': [28, 12, 878], 'backdrop_path':
# '/spFSZBt83uruCwedMN8HR2uFklI.jpg', 'adult': False, 'overview': "With global superpowers engaged in an increasingly
# hostile arms race, Superman leads a crusade to rid the world of nuclear weapons. But Lex Luthor, recently sprung from
# jail, is declaring war on the Man of Steel and his quest to save the planet. Using a strand of Superman's hair, Luthor
# synthesizes a powerful ally known as Nuclear Man and ignites an epic battle spanning Earth and space.", 'poster_path':
# '/q1P6UHWdrtZNkmdnoprV0ILfLlr.jpg'}, {'popularity': 10.151, 'id': 630656, 'video': True, 'vote_count': 22,
# 'vote_average': 7, 'title': 'The Death and Return of Superman', 'release_date': '2019-01-13', 'original_language':
# 'en', 'original_title': 'The Death and Return of Superman', 'genre_ids': [12, 16, 28, 14], 'backdrop_path':
# '/c3BQUy9AENkdd8us6OaB8GGBHc8.jpg', 'adult': False, 'overview': 'The Death of Superman and Reign of the Supermen now
# presented as an over two-hour unabridged and seamless animated feature. Witness the no-holds-barred battle between the
# Justice League and an unstoppable alien force known only as Doomsday, a battle that only Superman can finish and will
# forever change the face of Metropolis.', 'poster_path': '/8ztnQenlJsIoVEHKsM1YugSDxRx.jpg'}, {'popularity': 7.438,
# 'id': 39440, 'video': False, 'vote_count': 80, 'vote_average': 7, 'title': 'Waiting for "Superman"', 'release_date':
# '2010-09-24', 'original_language': 'en', 'original_title': 'Waiting for "Superman"', 'genre_ids': [99],
# 'backdrop_path': '/gcyNHCiWAgL02c3EewrCFMG96ra.jpg', 'adult': False, 'overview': 'Gripping, heartbreaking, and
# ultimately hopeful, Waiting for Superman is an impassioned indictment of the American school system from An
# Inconvenient Truth director Davis Guggenheim.', 'poster_path': '/l7mRlEi4VCEH7sfgaXX1b6LzsXn.jpg'}, {'popularity':
# 6.397, 'id': 19323, 'video': False, 'vote_count': 45, 'vote_average': 5.8, 'title': 'Superman: Brainiac Attacks',
# 'release_date': '2006-06-20', 'original_language': 'en', 'original_title': 'Superman: Brainiac Attacks', 'genre_ids':
# [16, 28, 10751, 878], 'backdrop_path': '/rarv0b3OyhG2y9qltGogtlVGk6b.jpg', 'adult': False, 'overview': "Embittered by
# Superman's heroic successes and soaring popularity, Lex Luthor forms a dangerous alliance with the powerful
# computer/villain Brainiac. Using advanced weaponry and a special strain of Kryptonite harvested from the far reaches
# of outer space, Luthor specifically redesigns Brainiac to defeat the Man of Steel.", 'poster_path':
# '/7l6hhBiM0seBVnh70uQ1uLZO7qH.jpg'}, {'popularity': 6.655, 'id': 292081, 'video': False, 'vote_count': 11,
# 'vote_average': 7.8, 'title': 'Sunshine Superman', 'release_date': '2015-05-22', 'original_language': 'en',
# 'original_title': 'Sunshine Superman', 'genre_ids': [99], 'backdrop_path': '/8z4ZEMWimpCFpnsM24owu8u6V6w.jpg',
# 'adult': False, 'overview': 'Documentary portrait of Carl Boenish, the father of the BASE jumping movement, whose
# early passion for skydiving led him to ever more spectacular -and dangerous- feats of foot-launched human flight.',
# 'poster_path': '/np1wtAPrxwvmQXj5MGnn2bw5rtS.jpg'}, {'popularity': 8.85, 'id': 17074, 'video': False, 'vote_count':
# 112, 'vote_average': 7, 'title': "The Batman Superman Movie: World's Finest", 'release_date': '1998-08-18',
# 'original_language': 'en', 'original_title': "The Batman Superman Movie: World's Finest", 'genre_ids': [28, 16],
# 'backdrop_path': '/rHf1RAbfdhHIMbwhU08A4Q7Kc6e.jpg', 'adult': False, 'overview': "Joker goes to Metropolis with an
# offer and plan to kill Superman for Lex Luthor while Batman pursues the clown to Superman's turf", 'poster_path':
# '/dQxwNGQ6pQLCUE5vaI9PwIZK6UC.jpg'}, {'popularity': 2.666, 'id': 126712, 'video': False, 'vote_count': 9,
# 'vote_average': 5.1, 'title': 'Superman', 'release_date': '1948-07-15', 'original_language': 'en', 'original_title':
# 'Superman', 'genre_ids': [28, 80, 878], 'backdrop_path': '/9hPPQz7z1HaVXqsHMq9HyMIDjjP.jpg', 'adult': False,
# 'overview': "Superman comes to Earth as a child and grows up to be his home's first superhero with his first major
# challenge being to oppose The Spider Lady.", 'poster_path': '/pDi8uqSg4dfcedkU6CTHvBWdv2H.jpg'}, {'popularity': 2.075,
# 'vote_count': 10, 'video': False, 'poster_path': '/i8hliwYdzUpbc5FA6kfNbop97Ta.jpg', 'id': 145963, 'adult': False,
# 'backdrop_path': None, 'original_language': 'en', 'original_title': 'Superman: The Bulleteers', 'genre_ids':
# [28, 16, 14], 'title': 'Superman: The Bulleteers', 'vote_average': 6.2, 'overview': 'Criminals with rocket powered car
# loot and extort the city, and only Superman can stop them!', 'release_date': '1942-03-26'}]}

# print(movie.info())
# {'adult': False, 'backdrop_path': '/eg049B1TJdWuKuyKowNmhZxNToc.jpg', 'belongs_to_collection': {'id': 1570,
# 'name': 'Die Hard Collection', 'poster_path': '/xhnb5lVfwE7NHycdPNdIxHx7kZi.jpg', 'backdrop_path':
# '/5kHVblr87FUScuab1PVSsK692IL.jpg'}, 'budget': 28000000, 'genres': [{'id': 28, 'name': 'Action'}, {'id': 53, 'name':
# 'Thriller'}], 'homepage': 'https://www.foxmovies.com/movies/die-hard', 'id': 562, 'imdb_id': 'tt0095016',
# 'original_language': 'en', 'original_title': 'Die Hard', 'overview': "NYPD cop John McClane's plan to reconcile with
# his estranged wife is thrown for a serious loop when, minutes after he arrives at her office, the entire building is
# overtaken by a group of terrorists. With little help from the LAPD, wisecracking McClane sets out to single-handedly
# rescue the hostages and bring the bad guys down.", 'popularity': 20.978, 'poster_path':
# '/fiXHtnQpQiGVkMtyYnEfQ6Gtfx8.jpg', 'production_companies': [{'id': 1073, 'logo_path': None, 'name': 'Gordon Company',
# 'origin_country': ''}, {'id': 1885, 'logo_path': '/xlvoOZr4s1PygosrwZyolIFe5xs.png', 'name': 'Silver Pictures',
# 'origin_country': 'US'}, {'id': 25, 'logo_path': '/qZCc1lty5FzX30aOCVRBLzaVmcp.png', 'name': '20th Century Fox',
# 'origin_country': 'US'}], 'production_countries': [{'iso_3166_1': 'US', 'name': 'United States of America'}],
# 'release_date': '1988-07-15', 'revenue': 140767956, 'runtime': 131, 'spoken_languages': [{'iso_639_1': 'en', 'name':
# 'English'}, {'iso_639_1': 'de', 'name': 'Deutsch'}, {'iso_639_1': 'it', 'name': 'Italiano'}], 'status': 'Released',
# 'tagline': '40 Stories. Twelve Terrorists. One Cop.', 'title': 'Die Hard', 'video': False, 'vote_average': 7.7,
# 'vote_count': 6868}
