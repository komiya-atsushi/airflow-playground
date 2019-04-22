DOCKER = docker
AIRFLOW = pipenv run airflow

SLACK_WEBHOOK_TOKEN =
DOCKER_STACK_NAME_MYSQL = airflow-playground-mysql

export AIRFLOW_HOME=$(PWD)
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=mysql://root:root@0.0.0.0:3306/airflow


.PHONY: clean \
	start-mysql stop-mysql \
	init-airflow start-webserver stop-webserver run-sched
	uler

clean:
	rm -rf logs/
	rm airflow.cfg airflow.db unittests.cfg

start-mysql:
	mkdir -p tmp/mysql
	$(DOCKER) stack deploy -c docker/stack/mysql.yml $(DOCKER_STACK_NAME_MYSQL)

stop-mysql:
	$(DOCKER) stack rm $(DOCKER_STACK_NAME_MYSQL)

init-airflow: start-mysql
	$(AIRFLOW) initdb
	$(AIRFLOW) resetdb -y
	$(AIRFLOW) connections -a \
		--conn_id slack \
		--conn_type http \
		--conn_host "https://hooks.slack.com/services" \
		--conn_extra '{"webhook_token":"$(SLACK_WEBHOOK_TOKEN)"}'

start-webserver:
	nohup $(AIRFLOW) webserver >$(PWD)/logs/webserver-stdout.log 2>$(PWD)/logs/webserver-stderr.log &

stop-webserver:
	kill $$(cat airflow-webserver.pid)

run-scheduler:
	$(AIRFLOW) scheduler
