# airflow-playground

## How to use

```bash
# Run MySQL container
make start-mysql

# If your Slack webhook is https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX,
# then WEBHOOK_TOKEN is /T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
export WEBHOOK_TOKEN=___PUT_YOUR_WEBHOOK_TOKEN_HERE___

# Initialize airflow
make init-airflow SLACK_WEBHOOK_TOKEN=${WEBHOOK_TOKEN}

# Run Airflow webserver as background process 
make start-webserver

# Run Airflow scheduler
make run-scheduler

# Stop Airflow webserver process
make stop-webserver

# Stop MySQL container
make stop-mysql
```
