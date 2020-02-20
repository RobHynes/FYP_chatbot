## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## generic

* gen_request
    - action_omdb_api_call
    - utter_correct

## generic long

* have_request
    - utter_what_question
* gen_request
    - action_omdb_api_call
    - utter_correct

## Confirm Correct

* gen_request
    - action_omdb_api_call
    - utter_correct
* confirm
	- utter_any_more_questions
* gen_request

## Genre, Year

* gen_request{"genre":"drama","year":"2013"}
    - slot{"genre":"drama"}
    - slot{"year":"2013"}
    - action_tmdb_api_call
    - utter_correct

## Genre, Type, Date

* gen_request{"genre":"comedy","type":"show","DATE":"30th of March"}
    - slot{"genre":"comedy"}
    - slot{"type":"show"}
    - slot{"DATE":"30th of March"}
    - action_tmdb_api_call
    - utter_correct

## Role, Person

* gen_request{"role":"actor","PERSON":"Matt Damon"}
    - slot{"role":"actor"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb
    - utter_correct

## Type, Title

* gen_request{"type":"movie","title":"Joker"}
    - slot{"type":"movie"}
    - slot{"title":"Joker"}
    - action_omdb_api_call
    - utter_correct
* confirm

## Person

* gen_request{"PERSON":"Matt Damon"}
    - slot{"PERSON":"Matt Damon"}
    - action_person_tmdb
    - utter_correct

## Deny

* gen_request
    - action_omdb_api_call
    - utter_correct
* deny
	- utter_don't_understand

## Deny short

	- utter_correct
* deny
	- utter_don't_understand

## Confirm short

    - utter_correct
* confirm
	- utter_any_more_questions
* gen_request
