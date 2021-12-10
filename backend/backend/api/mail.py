import flask
from flask import request
import backend
import backend.ezgmail as ezgmail
import json
import os

@backend.app.route('/', methods=["GET"])
def index():
    return "helloworld"


@backend.app.route('/api/email/', methods=["GET"])
def email():
    email_id = request.args.get("id", default=-1, type=int)
    message_dict = _email_to_dict(email_id)
    if message_dict:
        message_dict["success"] = True
        return flask.jsonify(message_dict)
    else:
        return flask.jsonify({
            'success': False,
            "error": "IndexError"
        }), 400


@backend.app.route("/api/command/", methods=["GET"])
def command():
    req_dict = request.get_json(force=True)  # directly a dict
    print(req_dict)
    try:
        response = _command(
            req_dict["id"], req_dict["command"], req_dict["args"])
    except Exception as e:
        return flask.jsonify({
            'success': False,
            'error': str(e)
        }), 400
    return flask.jsonify({
        'success': True,
        'response': response
    })


def _email_to_dict(message):
    message_dict = {
        "id": message.id,
        "from": message.sender,
        "to": message.recipient.split(","),
        "subject": message.subject,
        "time": message.timestamp,
        "body": message.body
    }
    return message_dict


def _command(email_id, command, args={}):
    """Parse and execute the command.

    List of current avaliable commands:
    1. `read`
    2. `unread`
    3. `spam`
    4. `delete`
    5. `search`
        - `query`: a string, see details @ https://support.google.com/mail/answer/7190?hl=en
    6. `show`
    7. `prev`
    8. `next`
    9. `latest`
    TODO:
    1. `forward` to a list of users with/without new content
    2. `reply`
    """
    response = None
    labeling = ["read", "unread", "spam", "delete", "star", "forward"]
    if command in labeling:
        # Simple labeling & No response
        m = ezgmail.get(email_id)  # Absolute index from previous query
        if command == 'read':
            m.markAsRead()
        elif command == 'unread':
            m.markAsUnread()
        elif command == 'spam':
            m.markAsSpam()
        elif command == 'delete':
            m.trash()
        elif command == 'star':
            m.star()
        elif command == 'forward':
            namedict = json.load(open(os.path.join(os.path.dirname(__file__), "namedict.json")))
            emailadd = None
            if args["recipient"] in namedict:
                emailadd=namedict[args["recipient"]]
            else:
                emailadd = "hangrui@umich.edu"
            m.forward(emailadd)  # We can add additional forward message
    else:
        # Query (for now)
        if command == "search":
            query = args["query"]
            m = ezgmail.searchMessages(query)
        elif command == "show":
            m = ezgmail.get(email_id)
        elif command == "prev":
            prev_email_id = _prev(email_id)
            if prev_email_id is None:
                raise IndexError("Already first message.")
            m = ezgmail.get(prev_email_id)
        elif command == "next":
            next_email_id = _next(email_id)
            if next_email_id is None:
                raise IndexError("Already last message.")
            m = ezgmail.get(next_email_id)
        elif command == "latest":
            id_list = ezgmail.getIdList()
            if id_list:
                lastest_email_id = id_list[0]
            else:
                raise IndexError("No message at all.")
            m = ezgmail.get(lastest_email_id)
        if isinstance(m, list):
            email_list = m
        else:
            email_list = [m]
        response = [_email_to_dict(email) for email in email_list]
    return response


def _prev(email_id):
    """Return the previous message id."""
    id_list = ezgmail.getIdList()
    inv_dict = {v: i for i, v in enumerate(id_list)}
    cur_id = inv_dict.get(email_id, None)
    if cur_id is not None and cur_id > 0:
        return id_list[cur_id - 1]
    return None

def _next(email_id):
    """Return the next message id."""
    id_list = ezgmail.getIdList()
    inv_dict = {v: i for i, v in enumerate(id_list)}
    cur_id = inv_dict.get(email_id, None)
    if cur_id is not None and cur_id < len(id_list) - 1:
        return id_list[cur_id + 1]
    return None

