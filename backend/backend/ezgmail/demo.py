import ezgmail


def print_my_email_address():
    """
    Print my email address.
    """
    print(f"My email address: {ezgmail.EMAIL_ADDRESS}")


def search(query, maxResults=25):
    """
    Search for my emails based on query (same as that in the Gmail search box, support operatives).
    """
    threads = ezgmail.search(query, maxResults)
    print(f"{len(threads)} results found")
    print("sample result")
    print("-----------------------------------------------------")
    msg = threads[0].messages[0]
    print("sender:", msg.sender)
    print("recipient:", msg.recipient)
    print("subject:", msg.subject)
    print("body:", msg.body)
    print("timestamp:", msg.timestamp)
    print("-----------------------------------------------------")


def send(recipient, subject, body, attachments=None, cc=None):
    """
    Send an email.
    """
    ezgmail.send(recipient, subject, body, attachments, cc)


def unread(maxResults=25):
    """
    Retrieve most recent unread emails.
    """
    unreadthreads = ezgmail.unread(maxResults)
    print(f"{len(unreadthreads)} unread emails")
    print("sample unread result")
    print("-----------------------------------------------------")
    msg = unreadthreads[0].messages[0]
    print("sender:", msg.sender)
    print("recipient:", msg.recipient)
    print("subject:", msg.subject)
    print("body:", msg.body)
    print("timestamp:", msg.timestamp)
    print("-----------------------------------------------------")
    return unreadthreads


def recent(maxResults=25):
    """
    Retrieve most recent emails.
    """
    recentThreads = ezgmail.recent(maxResults)
    print(f"{len(recentThreads)} recent emails")
    print("sample recent result")
    print("-----------------------------------------------------")
    msg = recentThreads[0].messages[0]
    print("sender:", msg.sender)
    print("recipient:", msg.recipient)
    print("subject:", msg.subject)
    print("body:", msg.body)
    print("timestamp:", msg.timestamp)
    print("-----------------------------------------------------")
    return recentThreads


def delete(GmailThreadObject):
    """
    Move an email to trash.
    """
    GmailThreadObject.trash()


def MardAsRead(GmailThreadObject):
    """
    Mark one or more emails as read.
    """
    GmailThreadObject.markAsRead()


def MardAsUnread(GmailThreadObject):
    """
    Mark one or more emails as unread.
    """
    GmailThreadObject.markAsUnread()


def DownloadAttachments(GmailThreadObject, path):
    """
    Download all attachments in one email.
    """
    GmailThreadObject.downloadAllAttachments(path)


def Reply(GmailThreadObject, body, attachments=None, cc=None, bcc=None, mimeSubtype="plain"):
    """
    Reply.
    """
    GmailThreadObject.reply(body, attachments, cc, bcc, mimeSubtype)


def Forward(GmailThreadObject, recipient, body=None, attachments=None, cc=None, bcc=None):
    """
    Forward an email.
    """
    GmailThreadObject.forward(recipient, body, attachments, cc, bcc)


if __name__ == '__main__':
    search('subject:test ezgmail')
    send('xinyu_lu@sjtu.edu.cn', 'test ezgmail send one',
         'Hi,\nHere is the testing message for sending.\nSincerely,\nSandy')
    unreadThreads = unread()
    recentThreads = recent()
    delete(recentThreads[0])
    MardAsRead(unreadThreads[0])
    Forward(recentThreads[0], "ruiyuli@umich.edu", "hey I am testing. Iris")
    MardAsUnread(recentThreads[0])
    DownloadAttachments(recentThreads[0], '.')