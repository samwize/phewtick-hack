Phewtick Hack
=============

This is a python script to automatically call Phewtick RESTful APIs. 

Automatically earns you money!


What is Phewtick?
------------------

[Phewtick](http://www.techinasia.com/phewtick-mobile-app/) is an app that let you earn money when you meetup with friends! 

To earn, your friend must be nearby, then you scan his/her QR code, and both of you will get a random number of points (which is pegged to real money). On average, you earn a few cents per meetup.. 

You also need to wait 1 hour before you can 'meetup' with the same friend again.

To cash out, you need to accumulate ~$30, which means you need ~1000 meetups before you can get the money.



Why create this hack?
----------------------

The story goes like this..

My colleagues and I all use Phewtick, and is intrigued with this app 'idea' and 'business model'. We are active users of Phewtick, and the first thing we did as we arrive in office is to 'meetup'.

And we meetup almost every hour..

As a [convert hacker](http://linked.in/junda), whose work is in [providing awesome API](http://developer.hoiio.com), I thought I should take a look at Phewtick internals.



What is this hack?
----------------------

Using mitmproxy to sniff it's HTTP traffic, I learnt it's API endpoints and protocols. 

Then I wrote some python codes to help automate the scanning.

Just the scanning. 

We are not really cheating. We are indeed meeting up everyday in the office :)


Usage
--------

Clone the project and rename the `settings-sample.py` to `settings.py`

	git clone https://github.com/samwize/phewtick-hack.git
	mv phewtick-hack/settings-sample.py phewtick-hack/settings.py

Open `settings.py` and enter your token, and your friends' tokens. To more tokens, the denser your network.

Read the next section on how you can retrieve your token.

Run the script:

	cd phewtick-hack
	python phew.py

The script will automate refreshing of QR code and scanning it for everyone. Then it will sleep for around 1 hour before repeating again.

Cheers (if you manage to cash out..)


Retrieving tokens
-----------------

It is a bit more tedious to get the token. It involves sniffing the HTPP traffic as you run your Phewtick app. 

You could use any software to sniff the http traffic.

For me, I use [mitmproxy](http://mitmproxy.org/). Here is a guide on [how to use mitmproxy](http://blog.just2us.com/2012/05/sniff-iphone-http-traffic-using-mitmproxy/).

This is how my mitmproxy looks:

![mitmproxy screenshot](https://raw.github.com/samwize/phewtick-hack/master/mitmproxy.png)

What you need here is the `token` (which is purposefully blurred in the screenshot). Copy that and add to `settings.py` `tokens` array.

Tip: You could ask all your friends to connect to your proxy and sniff their tokens.

