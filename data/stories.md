## Enroll Course Story
* greet
  - utter_greet
* user_wants_to_enroll
  - utter_display_programs
* user_choose_program
  - action_display_course
* user_choose_course
  - action_display_course_info
* user_choose_save_seat
  - utter_save_seat
  - form_info
  - form{"name": "form_info"}
  - form{"name": null}
  - action_email_admission_depart
  - action_email_admitted_student
  - utter_goto_home
* user_choose_home
  - utter_greet


## College information Story
* greet
  - utter_greet
* user_wants_college_info
  - utter_display_college_info
  - utter_campus_life
* user_choose_campuslife
  - action_display_facilities
  - utter_goto_home
* user_choose_home
  - utter_greet



## goodbye
* goodbye
  - utter_goodbye

<!-- ## form Testing path
* network_issue
  - form_info
  - form{"name": "form_info"}
  - form{"name": null} -->


## Display Result for NHCE students
* greet
  - utter_greet
* user_choose_result
  - utter_ask_if_new_student
* user_choose_no
  - utter_ask_USN
* user_gave_USN
  - action_display_student_result
  - utter_goto_home
* user_choose_home
  - utter_greet

## Result for New students
* greet
  - utter_greet
* user_choose_result
  - utter_ask_if_new_student
* user_choose_yes
  - utter_display_eresult_link
  - utter_goto_home
* user_choose_home
  - utter_greet


<!-- ## Payment feature
* greet
  - utter_greet
* user_choose_payment
  - utter_ask_PAYMENT_TYPE
* user_choose_PAYMENT_TYPE
  - utter_ask_EMAIL
* user_gave_EMAIL
  -utter_ask_USN
* user_gave_USN
  - utter_ask_AMOUNT
* user_entered_AMOUNT
  - utter_ask_NAME
* user_gave_NAME
  - action_email_payment_receipt
  - utter_goto_home
* user_choose_home
  - utter_greet -->

<!--
## College Facilites
* greet
  - utter_greet
* user_choose_campuslife
  - action_display_facilities
* user_choose_any_facility
  - action_display_facility_info
  - utter_restart
* user_choose_restart -->
