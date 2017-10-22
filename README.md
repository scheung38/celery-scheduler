# Celery Scheduler

A Docker implementation of Celery running on Flask, managed with supervisord.

## Overview

This is a scheduler application powered by [Celery](http://docs.celeryproject.org/en/latest/index.html) running on a minimal python web framework, [Flask](http://flask.pocoo.org/).

The application is process-managed by [Supervisord](http://supervisord.org/) which takes care of managing celery task workers, celerybeat and Redis as the message broker.

The deployment of the application is handled through [Docker](https://www.docker.com/what-docker) which isolates the application environment. It allows the application to run the same, whether locally, in staging or when deployed within a server.

## Running this setup

This setup is built for deployment with Docker.

Deployment with Docker is recommended for consistency of application environment.

1. Clone the repository
```bash
cd ~
git clone https://github.com/channeng/celery-scheduler.git
cd celery-scheduler
```

2. Install Docker
	- [Mac or Windows](https://docs.docker.com/engine/installation/)
	- [Ubuntu server](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
		- To install docker in Ubuntu, you may run the install script:
		```bash
		sudo bash scripts/startup/ubuntu_docker_setup.sh
		```
2. Build docker image
	```bash
	docker build -t celery-scheduler .
	```
3. (Optional) Stop any containers running on existing docker image
	```bash
	docker stop $(docker ps -f ancestor=celery-scheduler --format "{{.ID}}")
	```
3. Run supervisord with docker container
	```bash
	docker run -p 3020:80 -d celery-scheduler /usr/bin/supervisord --nodaemon
	```
Note: You may also choose to run this setup without Docker however no script is provided. Setup instructions can be interpreted from the given Dockerfile.

## Checking successful deployment
- Enter bash terminal of running Docker container
	```bash
	docker exec -i -t $(docker ps -f ancestor=celery-scheduler --format "{{.ID}}") /bin/bash
	```
- Check all required processes are running: 
	```bash
	ps aux
	```

	You shoud see something like the following:
	```
	USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
	root         1  0.0  2.5  56492 12728 ?        Ss   Oct21   0:05 /usr/bin/python /usr/bin/supervisord --nodaemon
	root         7  0.0  0.5  31468  2616 ?        Sl   Oct21   0:30 /home/ubuntu/caramel/redis-3.2.1/src/redis-server *:6379
	root         8  0.0  8.3  98060 41404 ?        S    Oct21   0:00 /home/ubuntu/.virtualenvs/celery_env/bin/python2.7 /home/ubuntu/.virtualenvs/celery_env/bin/celery beat -A ap
	root         9  0.1  8.4  91652 41900 ?        S    Oct21   0:42 /home/ubuntu/.virtualenvs/celery_env/bin/python2.7 /home/ubuntu/.virtualenvs/celery_env/bin/celery worker -A
	root        20  0.0  9.3  99540 46820 ?        S    Oct21   0:00 /home/ubuntu/.virtualenvs/celery_env/bin/python2.7 /home/ubuntu/.virtualenvs/celery_env/bin/celery worker -A
	```
- Retrieve logs and run test
	```bash
	tail /var/log/redis/redis.log
	tail /var/log/celery/beat.log
	tail /var/log/celery/worker.log
	tail /var/log/supervisor/supervisord.log
	source /home/ubuntu/.virtualenvs/celery_env/bin/activate
	python manage.py test
	```

- If successfully deployed, supervisor logs should display:
	```bash
	INFO success: redis entered RUNNING state, process has stayed up for > than 10 seconds (startsecs)
	INFO success: celerybeat entered RUNNING state, process has stayed up for > than 10 seconds (startsecs)
	INFO success: celery entered RUNNING state, process has stayed up for > than 10 seconds (startsecs)
	```

### Termination

```bash
supervisorctl stop all
```

## Adding tasks to Celery

- Task scripts should be written and stored in app/tasks
- Update `celeryconfig.py` for new tasks and trigger times

## Running adhoc tasks

- Update `manage.py` for a manager command for the task to run on trigger
- Run: ```python manage.py <manager_command>```

## Update to apps in Docker -- Rebuild docker image
```bash
docker build -t docker_app </path/to/project_dir>
```

## Contributing
Feel free to submit Pull Requests.
For any other enquiries, you may contact me at channeng@gmail.com.

