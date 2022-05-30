To run the bot clone this repositry:
`git pull https://tesla33IO/tt_exchange_tracker.git`
set needed variables in `Dockerfile` (bot token and db token)
after that run `docker-compose up`

Bot token you can get from the BotFather
Db token you can get on mongodb.com:
**1.** Create database `exchange_tracker` in collections
**2.** Create collection `users`
**3.** Then click `Connect` in `Database deployments` and select `Connect your application`, select python version 3.4 or later and copy connection string
