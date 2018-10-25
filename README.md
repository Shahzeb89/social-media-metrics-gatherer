# social-media-metrics-gatherer
Gathers important metrics about selected posts from YouTube, Facebook and Twitter using Twitter API, Facebook Graph API and web <br>
scrping using BS4

### API access
Twitter API can be accessed by creating a Twitter app which will give you access to `consumer key`, `consumer_secret`, `access_token` <br>
and `access_secret`

Facebook API can be accessed by creating a long-term token, this token can then be appended to `access_token`.

### On Input
1. Input file needs to be named `input.csv`.
2. Input file needs to contain the `link` column, with urls for the required Facebook, Twitter, YouTube posts.
