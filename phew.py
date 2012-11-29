from random import randrange
from time import sleep
from settings import *
from rest import *



def autoScan():
    """
    Automatically scan QR codes between tokens
    """
    while (True):
        # Loop from 1st till second last token
        for i in range(0, len(tokens)-1):
            # Loop for from next till last
            for j in range(i+1, len(tokens)):
                new_qr_key = refreshToken(tokens[j])
                sleep(randrange(10))
                scanToken(tokens[i], new_qr_key)
                sleep(randrange(10))
            sleep(randrange(20))

        # Sleep for 1 hour
        t = 60*60
        print "Sleeping for " + str(t/60) + " minutes.."
        next = datetime.now() + timedelta(0,t)
        print "Next meetup at " + next.strftime('%H:%M')
        sleep(t)

        # Update everybody location
        for i in range(0, len(tokens)):
            updateLocation(tokens[i])
            sleep(randrange(10))


def message(token_pos, phewtick_id, message):
    """
    Send a message from user (token_pos in settings.tokens) to user (phewtick_id)
    """
    sendMessage(tokens[token_pos], phewtick_id, message)


def generateUsers():
    writeAllUsersInTimelineForAllTokens()
    all = readAllUsersForAllTokens()
    for id, user in all.iteritems():
        print id + "\t - " + user['name']



if __name__ == "__main__":
    autoScan()
