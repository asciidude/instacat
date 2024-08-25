# InstaCat
InstaCat is an Instagram chatbot that sends images of cats when "cat" is detected in DMs.

Due to the lack of flexibility in terms of events with InstagrAPI, I had to implement my own "event handler" that detects incoming messages within a range of ±10 seconds. This system works fine and the bot will only handle one message at a time, with an additional sleep method being called every 2 1/2 seconds to ensure the Inbox API is not being spammed.

Honestly, this project was extremely tedious to work with and took a total of 3 hours and 45 minutes to complete. Even now, I am not sure if it will properly handle *all* errors, but regardless I'm not going to continue working on this. It's entire intention was a silly project, and that it did well.

#### You should run this program on a quality, not shared proxy and use a different account for Instagram.

## Dependencies
- instagrapi
- RedDownloader

## Logging in
In your main.py file, change "username" and "password" to your username and password for Instagram.

## Enabling/Disabling Downloads
To enable/disable image downloads (eg. if you're simply restarting or do daily restarts) you can change the `downloading` variable to "disabled". To re-enable it, change it to `False`.

**It is automatically disabled by default.**

### License
This project is licensed under MIT.
