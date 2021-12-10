from google.cloud import dialogflow
import requests
import datetime
import nlp
from nlp.api.nlp_server import Dialogflow_session, _send_command
from nlp.api.summarize import Summarize

OPERATIONS = ["read","unread","delete","spam",'forward','star']
summarizer = Summarize()

def _get_name_from_sender(sender:str) -> str:
    if isinstance(sender, list):
        sender = sender[0]  # select the first sender if sender is a list
    email_addr_start_idx = sender.find('<')
    name = sender[:email_addr_start_idx]
    return name.strip()

df_session = Dialogflow_session(session_id=5678)
while True:
    user_text = input("Enter user text: ")
    # print("user text: ", user_text)
    if user_text == "quit":
        break
    action, email_ids, args, bot_text = df_session.parse_command_dialogflow(user_text)
    bot_response_dict = {
        "bot_text_start": None,  # the response should start with this string
        "from": None,  # sender name without email addr, e.g. Changyuan Qiu
        # "to": None,  # recipient name without email addr, e.g. Changyuan Qiu
        "subject": None,  # title
        "time": None,  # send time
        "summary": None,  # summary of the email
        "body": None,  # whole body of the email
        "bot_text_end": None,
        # the response should end with this string, e.g. Do you want to know more about this email?
    }

    bot_response_dict["bot_text_start"] = bot_text
    action_type = action.split('.')[0]
    command = action.split('.')[1]  # e.g. read, unread, spam...

    # send command to backend only when the action is a "command" type and command is in OPERATIONS (operations on an email)
    if action_type == "command":
        if command in OPERATIONS:  # send command to backend only when command is in OPERATIONS (operations on an email)
            for email_id in email_ids:
                _send_command(command, email_id, args)

        elif command == "speak_summary":  # read the email out for the user
            sender_name = _get_name_from_sender(df_session.query_email_dict["from"])
            # recipient_name = _get_name_from_sender(df_session.query_email_dict["to"])
            subject = df_session.query_email_dict["subject"]
            time = df_session.query_email_dict["time"]
            email_body = df_session.query_email_dict["body"]

            meta = {'title': subject, 'author': sender_name}
            summary = summarizer.summarize(email_body, meta=meta)  # todo: set the summary args

            bot_response_dict["from"] = sender_name
            # bot_response_dict["to"] = recipient_name
            bot_response_dict["subject"] = subject
            bot_response_dict["time"] = time
            bot_response_dict["summary"] = summary
            bot_response_dict["bot_text_end"] = " Do you want to know more about this email?"

        elif command == "speak_whole":  # read the email out for the user
            sender_name = _get_name_from_sender(df_session.query_email_dict["from"])
            # recipient_name = _get_name_from_sender(df_session.query_email_dict["to"])
            subject = df_session.query_email_dict["subject"]
            time = df_session.query_email_dict["time"]
            email_body = df_session.query_email_dict["body"]
            bot_response_dict["from"] = sender_name
            # bot_response_dict["to"] = recipient_name
            bot_response_dict["subject"] = subject
            bot_response_dict["time"] = time
            bot_response_dict["body"] = email_body

    print("action: ", action)
    print("email ids: ", email_ids)
    print("args: ", args)
    print("bot text: ", str(bot_response_dict))
    print('-' * 20)

