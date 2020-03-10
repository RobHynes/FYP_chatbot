## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## generic

* gen_request
    - action_tmdb_api_call
    - utter_correct

## generic long

* have_request
    - utter_what_question
* gen_request
    - action_tmdb_api_call
    - utter_correct

## Confirm Correct

* gen_request
    - action_tmdb_api_call
    - utter_correct
* confirm
	- utter_any_more_questions
* gen_request

## Genre, Date

* genre_request{"genre":"drama","DATE":"2013"}
    - slot{"genre":"drama"}
    - slot{"DATE":"2013"}
    - action_genre_tmdb

## Genre, Type, Date, date_request

* date_request{"genre":"comedy","type":"show","DATE":"30th March"}
    - slot{"genre":"comedy"}
    - slot{"type":"show"}
    - slot{"DATE":"30th March"}
    - action_tmdb_api_call
    - utter_correct

## Role, Person

* person_request{"role":"actor","PERSON":"Matt Damon"}
    - slot{"role":"actor"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb
    - utter_correct

## Type, Title

* gen_request{"type":"movie","title":"Joker"}
    - slot{"type":"movie"}
    - slot{"title":"Joker"}
    - action_tmdb_api_call
    - utter_correct
* confirm

## Person

* gen_request{"PERSON":"Matt Damon"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb
    - utter_correct

## Deny

* gen_request
    - action_tmdb_api_call
    - utter_correct
* deny
	- utter_dont_understand

## Genre, Type, Date, complex_request

* complex_request{"genre":"action","type":"movie","DATE":"2017"}
    - slot{"genre":"action"}
    - slot{"type":"movie"}
    - slot{"DATE":"2017"}
    - action_genre_tmdb
    - utter_correct

## say hello
* greet
  - utter_greet
