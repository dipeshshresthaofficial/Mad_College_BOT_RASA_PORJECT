# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import sqlite3
import smtplib
import numpy as np
#
#
class ActionDisplayCourse(Action):

    def name(self) -> Text:
        return "action_display_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        try:
            conn = sqlite3.connect('college2.db')

        except:
            content_text = "I can't connect with database, please wait for a second."
        user_message = str((tracker.latest_message)['text'])

        print("User message : ", user_message)
        if "UG" in user_message:
            exe_str = "Select course_name from courses where program is '{0}'".format('UG')
        elif 'PG' in user_message:
            exe_str = "Select course_name from courses where program is '{0}'".format('PG')

        try:
            content = conn.execute(exe_str)
            content_text = ''
            content_text += "We offer following courses for now:\n\n"
            for index, value in enumerate(content):
                content_text += str(index + 1) + ") " + str(value[0]) + "\n"

            content_text += "Enter item number (eg : 1 or 2 or 3 ...)"
            dispatcher.utter_message(text=content_text)

        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        return []

class ActionDisplayCourseInfo(Action):

    def name(self) -> Text:
        return "action_display_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        try:
            conn = sqlite3.connect('college2.db')

        except:
            content_text = "I can't connect with database, please wait for a second."
        user_message = str((tracker.latest_message)['text'])
        messages = []

        for event in (list(tracker.events))[:1000]:
            if event.get("event") == "user":
                messages.append(event.get("text"))

        user_message = messages[-2]
        print("All messages till now : \n",messages)
        print("user_message : ",user_message)
        program=""
        exe_str=""

        if "UG" in user_message:
            exe_str = "Select description,duration,fee,syllabus_link from courses where program is '{0}'".format('UG')
            program+="Under Graduate"
        elif 'PG' in user_message:
            exe_str = "Select description,duration,fee,syllabus_link from courses where program is '{0}'".format('PG')
            program+="Post Graduate"

        try:
            content = conn.execute(exe_str)
            content_text = ''
            user_input = str((tracker.latest_message)['text'])
            print(type(user_input))
            user_input = int(user_input)
            print(user_input)

            for index, value in enumerate(content):
                if(index+1)==user_input:
                    content_text += str(value[0]) + "\n\n"+"Total Duration: "+str(value[1])+"\n\n"+"Total Fee: "+str(value[2])+"\n\n"+"You can find the syllabus here: "+str(value[3])

            content_text+="\n\nType 'SAVE SEAT' to save seat for yourself in this course"+"\n\nType 'BYE' to exit "
            dispatcher.utter_message(text=content_text)
        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        conn.close()
        return []


class ActionEmailAdmissionDepart(Action):
    global admit_no

    def name(self) -> Text:

        return "action_email_admission_depart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("admission department informed")

        messages = []
        for event in (list(tracker.events))[:1000]:
            if event.get("event") == "user":
                messages.append(event.get("text"))

        user_message = messages[-2]
        user_email = messages[-1]
        print("All messages till now : \n",messages)
        print("user_message : ",user_message)

        admit_no = np.random.randint(1,10000,1)[0]


        fromaddr = '1nh17cs039.dipesh@gmail.com'
        toaddrs = '1nh17cs039.dipesh@gmail.com'
        msg = "Admission Alert! " +",\n\nA student with following NAME and EMAIL number has show interest in one of the course: " \
              "\n\n Admit No: "+ str(admit_no) + "\nName: " +user_message.upper()+"\nEmail: "+user_email+ "\n\nThanks,\nPlease contact him/ her as soon as possible!"
        username = '1nh17cs039.dipesh@gmail.com'
        obj = open('pass.txt')
        password = obj.read()
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        content = "Thanks the concerned department will be notified, you will receive a call/ email soon."
        dispatcher.utter_message(text=content)

        return []

class ActionEmailAdmittedStudent(Action):

    def name(self) -> Text:

        return "action_email_admitted_student"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("admission department informed")

        messages = []
        for event in (list(tracker.events))[:1000]:
            if event.get("event") == "user":
                messages.append(event.get("text"))

        user_name = messages[-2]
        user_email = messages[-1]
        print("All messages till now : \n",messages)
        print("user_message : ",user_name)

        fromaddr = '1nh17cs039.dipesh@gmail.com'
        toaddrs = user_email
        msg = "Admission Alert! " +",\n\n Thank You "+user_name.upper()+" for showing interest into our course please note the following important information: " \
               +"\n\nName: " +user_name.upper()+"\nEmail: "+user_email+ "\n\nThanks,\nYou will be contacted soon by our Admission Department\n\n Regards!"
        username = '1nh17cs039.dipesh@gmail.com'
        obj = open('pass.txt')
        password = obj.read()
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

        return []


class ActionFormInfo(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "form_info"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        print("required_slots(tracker: Tracker)")
        return ["NAME", "EMAIL"]
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        dispatcher.utter_message(template="utter_submit")
        return []


# Facility section

class ActionDisplayFacilities(Action):

    def name(self) -> Text:
        return "action_display_facilities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        try:
            conn = sqlite3.connect('college2.db')

        except:
            content_text = "I can't connect with database, please wait for a second."

        user_message = str((tracker.latest_message)['text'])

        print("User message : ", user_message)

        exe_str = "Select facility_name from facilities"

        try:
            content = conn.execute(exe_str)
            content_text = ''
            content_text += "NHCE has never compromised with the facility to students:\n\n"
            for index, value in enumerate(content):
                content_text += str(index + 1) + ") " + str(value[0]) + "\n"

            content_text += "Enter item number (eg : 1 or 2 or 3 ...)"
            dispatcher.utter_message(text=content_text)

        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        return []

# class ActionDisplayFacilityInfo(Action):
#
#     def name(self) -> Text:
#         return "action_display_facility_info"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         print("Inside actions")
#         try:
#             conn = sqlite3.connect('college2.db')
#
#         except:
#             content_text = "I can't connect with database, please wait for a second."
#
#         user_message = str((tracker.latest_message)['text'])
#         messages = []
#
#         for event in (list(tracker.events))[:1000]:
#             if event.get("event") == "user":
#                 messages.append(event.get("text"))
#
#         user_message = messages[-2]
#         print("All messages till now : \n",messages)
#         print("user_message : ",user_message)
#         program=""
#         exe_str=""
#
#         exe_str = "Select facility_name,description,feature,link from facilities"
#
#         try:
#             content = conn.execute(exe_str)
#             content_text = ''
#             user_input = str((tracker.latest_message)['text'])
#             print(type(user_input))
#             user_input = int(user_input)
#             print(user_input)
#
#             for index, value in enumerate(content):
#                 if(index+1)==user_input:
#                     content_text += str(value[0]) +":\n\n"+str(value[1])+ "\n"+str(value[2])+"\n\n"+"Learn More Here: "+str(value[3])
#
#             content_text+="\nType 'BYE' to exit "
#             dispatcher.utter_message(text=content_text)
#         except:
#             content_text = "Sorry system run into trouble.. Can you please check again?"
#             dispatcher.utter_message(text=content_text)
#
#         conn.close()
#         return []
#

class ActionDisplayStudentResult(Action):

    def name(self) -> Text:
        return "action_display_student_result"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("Inside actions")
        try:
            conn = sqlite3.connect('college2.db')

        except:
            content_text = "I can't connect with database, please wait for a second."

        user_message = str((tracker.latest_message)['text'])

        # getting USN slot value
        user_USN = tracker.get_slot("USN").upper()
        print(user_USN)

        exe_str = "Select student_name,sem,sec,course,cgpa,usn from students"

        try:

            content = conn.execute(exe_str)
            print('helllo check')
            content_text = ''
            content_text += "Your Result details is mentioned below:\n\n"
            for index, value in enumerate(content):
                print("hello")
                if(str(value[5]))==user_USN:
                    print("hello part 2")
                    content_text += str(index + 1) + ") Name: " + str(value[0]) + "\n" \
                    +str(index + 2) + ") USN: "+user_USN+ "\n" \
                    +str(index + 3) + ") Sem: " + str(value[1])+" "+ str(value[2])+"\n" \
                    +str(index + 4) + ") Course: "+ str(value[3])+"\n\n" \
                    +str(index + 5) + ") CGPA: "+ str(value[4])
                else:
                    content_text = "Your USN doesn't match with the Database, Please verify."


            dispatcher.utter_message(text=content_text)

        except:
            content_text = "Sorry system run into trouble.. Can you please check again?"
            dispatcher.utter_message(text=content_text)

        return []

# class action_email_payment_receipt(Action):
#
#     def name(self) -> Text:
#
#         return "action_email_payment_receipt"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         # print("admission department informed")
#
#         payment_type = tracker.get_slot("PAYMENT_TYPE")
#         user_usn = tracker.get_slot("USN").upper()
#         user_amount = tracker.get_slot("AMOUNT")
#         user_email = tracker.get_slot("EMAIL")
#
#         challan_no = np.random.randint(1,10000,1)[0]
#
#         try:
#             conn = sqlite3.connect('college2.db')
#
#         except:
#             content_text = "I can't connect with database, please wait for a second."
#
#         user_message = str((tracker.latest_message)['text'])
#
#
#
#         exe_str = "INSERT INTO payments (payment_id, amount, payment_type, student_usn) VALUES ('{0}','{1}','{2}','{3}')".format(challan_no,user_amount,payment_type,user_usn)
#
#
#         # try:
#         cur = conn.cursor()
#         cur.execute(exe_str)
#
#         conn.commit()
#         cur.close()
#         print('helllo check')
#         content_text = ''
#         content_text += "Your payment has been updated in our database, if any queries please contact Account Department:\n\n"
#
#         dispatcher.utter_message(text=content_text)
#         #
#         # except:
#         #     content_text = "Sorry system run into trouble.. Can you please check again?"
#         #     dispatcher.utter_message(text=content_text)
#
#
#         fromaddr = '1nh17cs039.dipesh@gmail.com'
#         toaddrs = user_email
#         msg = "Payment Alert! " +",\n Thank You for making your "+payment_type+" payment: " \
#               +"\n\nChallan No: "+ str(challan_no) + "\nUSN: " +str(user_usn)+"\nEmail: "+user_email+ "\n\Regards NHCE,\n Your payment has been updated!"
#         username = '1nh17cs039.dipesh@gmail.com'
#         obj = open('pass.txt')
#         password = obj.read()
#         server = smtplib.SMTP('smtp.gmail.com:587')
#         server.ehlo()
#         server.starttls()
#         server.login(username, password)
#         server.sendmail(fromaddr, toaddrs, msg)
#         server.quit()
#
#         return []
