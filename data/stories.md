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

## Genre, Year

* genre_request{"genre":"drama","DATE":"2013"}
    - slot{"genre":"drama"}
    - slot{"DATE":"2013"}
    - action_genre_tmdb
    - utter_correct

## Genre, Type, Date, date_request

* date_request{"genre":"comedy","type":"show","DATE":"30th of March"}
    - slot{"genre":"comedy"}
    - slot{"type":"show"}
    - slot{"DATE":"30th of March"}
    - action_date_tmdb
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

* person_request{"PERSON":"Matt Damon"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb
    - utter_correct

## Deny

* gen_request
    - action_tmdb_api_call
    - utter_correct
* deny
	- utter_dont_understand

## Type, Action, Person

* action_request{"type":"movie","action":"starred","PERSON":"Brad Pitt"}
  - slot{"type":"movie"}
  - slot{"action":"starred"}
  - slot{"PERSON":"Brad Pitt"}
  - action_role_tmdb
  - utter_correct

## Genre, Type, Date, complex_request

* complex_request{"genre":"action","type":"movie","DATE":"2017"}
    - slot{"genre":"action"}
    - slot{"type":"movie"}
    - slot{"DATE":"2017"}
    - action_genre_tmdb
    - utter_correct
