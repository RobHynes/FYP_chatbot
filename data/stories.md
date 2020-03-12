## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## generic

* gen_request
    - action_tmdb_api_call

## generic long

* have_request
    - utter_what_question
* gen_request
    - action_tmdb_api_call

## Genre, Date

* genre_request{"genre":"drama","DATE":"2013"}
    - slot{"genre":"drama"}
    - slot{"DATE":"2013"}
    - action_genre_tmdb

## Role, Person

* person_request{"role":"actor","PERSON":"Matt Damon"}
    - slot{"role":"actor"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb

## Type, Title

* gen_request{"type":"movie","title":"Joker"}
    - slot{"type":"movie"}
    - slot{"title":"Joker"}
    - action_tmdb_api_call

## Person

* gen_request{"PERSON":"Matt Damon"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb

## Genre, Type, Date, complex_request

* complex_request{"genre":"action","type":"movie","DATE":"2017"}
    - slot{"genre":"action"}
    - slot{"type":"movie"}
    - slot{"DATE":"2017"}
    - action_genre_tmdb

## say hello
* greet
  - utter_greet

## New Story

* greet
    - utter_greet
* action_request{"genre":"action","type":"movie","DATE":"2015"}
    - slot{"DATE":"2015"}
    - slot{"genre":"action"}
    - slot{"type":"movie"}
    - action_genre_tmdb
    - utter_correct

## Genre, Type, Date, date_request

* date_request{"genre":"comedy","type":"show","DATE":"30th March"}
    - slot{"genre":"comedy"}
    - slot{"type":"show"}
    - slot{"DATE":"30th of March"}
    - action_date_tmdb

## help

* help
	- utter_help
