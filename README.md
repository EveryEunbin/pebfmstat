# pebfmstat
Counting the reservations of PARK EUN-BIN Asia Fan Meeting Tour [link](https://pebfmstat.deta.dev)

- deta (flask deployed on [Deta Cloud](https://www.deta.sh/))
- heroku (selenium deployed on Heroku with cron only for Philippines, Thailand and Singapore)

Because of the end of the Heroku free plan service, I use github action to run selenium:
- github_action (selenium)

Github action on schedule trigger may delay, I use octokit deployed on [Deta Cloud](https://www.deta.sh/) with cron job to make a RestAPI to github: 
- deta_cron_action_nodejs (octokit make POST request to github action)
