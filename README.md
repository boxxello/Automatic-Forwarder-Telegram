# Automatic-Forwarder-Telegram
A python channel to channel forwarder bot with regex filters on the messages being sent based on [Pyrogram MTProto API framework](https://github.com/pyrogram/pyrogram).


[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Do not consider this project as a install and good to go bot.
It has got to be tweaked according to your needs.<br>


Also, don't forget to **Fork & Star the repository if you like it!**

---

** Requirements:

*** How to Install the Requirements?

**Tested Python version:** [Python 3.8+](https://www.python.org/downloads/)

**You must have pip or poetry installed. Please look up how to install them in your OS.**

Download a release of this project or clone the repository then navigate to the
folder where you placed the files on. <br>
Type `pip install -r requirements.txt` to get all the requirements installed in one go. <br>
Similar instructions applies for poetry.


---

1. Install the required packages

2. To configure this bot add the environment variables stated below. Or add them in [user_data.env](user_data.env).

3. Tweak the regexes in BotConfig.py according to your needs.

4. Run the script in terminal or deploy it into a docker container. (A [docker-compose.yml](docker-compose.yml) template can be found in the repo files) .

5. **If you are trying to install this on windows machine** you'll have to either: <br>
  - host your MongoDb database [download here for Windows users](https://www.mongodb.com/try/download/community) 
  - provide a correct connection URI string for the MongoDB db [instructions can be found here](https://www.mongodb.com/docs/manual/reference/connection-string/) 
  - deploy it with the docker MongoDB image.

6. `python -m ForwardBot` or if you want to deploy it to a docker container check [this file](Commands_to_deploy_img_docker.txt).


## Support & Maintenance Notice

By using this repo/script, you agree that the authors and contributors are under no obligation to provide support for the script and can discontinue its development, 
as and when necessary, without prior notice.
