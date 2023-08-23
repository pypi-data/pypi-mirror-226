# rabbitmq-email-notifier
python template for etd projects

# Using this Repository
Read the wiki in the rabbitmq-email-notifier repo for instructions on how to set up the template and badge for your repository:
https://github.com/harvard-lts/rabbitmq-email-notifier/wiki


## Local setup
    
1. Make a copy of the .env.example to .env and modify the user and password variables.

2. Start the container
    
```
docker-compose -f docker-compose-local.yml up -d --build --force-recreate
```

## Testing

1. Start the container up as described in the <b>Local Setup</b> instructions.

2. Exec into the container:

```
docker exec -it rabbitmq-email-notifier bash
```

3. Run the tests

```
pytest
```
4. Stop the container:

Start the container
    
```
docker-compose -f docker-compose-local.yml down
```

This command stops and removes all containers specified in the docker-compose-local.yml configuration. This command can be used in place of the 'stop' and 'rm' commands.

```
docker-compose -f docker-compose-local.yml down
```

### Deployment
## Dev
Dev deployment will occur using Jenkins.  To trigger the development deployment, commit and push to the 'trial' or 'main' branch.

## QA
QA is hosted on servers that contain L4 data.  Jenkins is not permitted to deploy to these servers so for QA, Jenkins will only perform the build.  To deploy:
1. Commit and push to 'main'.
2. If any IF changes happened, use ansible deploy commands from the ETD-IF project.  Otherwise, manually restart the stack on the server that hosts QA.  

## Prod
Deploying to prod requires that the code be tagged in 'main'.  That means the code should be stable and ready for a release. 
1. Create the tag and push to the repo if this hasn't been done.
2.Open Jenkins
3.Click on the "Branches" tab.
NOTE: you should see a pipeline with your new tag.  (if not, click on the "scan repository now" link in the sidebar.) 
4.Click on the green play (triangle) button to start the build
5.Follow the build progress using the blue ocean view
6.The build process should end with a green status. the docker image is now ready for deployment to prod.
7.Work with ops to deploy to prod using the ETD-IF project.

### Prerequisites to running docker locally
- Requires telemetry/jaeger docker running
- Make sure .env has JAEGER_NAME and JAEGER_SERVICE_NAME (see .env.example)
- - Note JAEGER_NAME must have local ip (if on vpn go to Cisco Icon -> Show Statistics Window -> CLient Address (IPv4)
- start jaeger docker
- `docker pull jaegertracing/all-in-one:latest` followed by
- `docker run -d --name jaeger  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411  -e COLLECTOR_OTLP_ENABLED=true  -p 6831:6831/udp  -p 6832:6832/udp  -p 5778:5778  -p 16686:16686  -p 4317:4317  -p 4318:4318  -p 14250:14250  -p 14268:14268  -p 14269:14269  -p 9411:9411  jaegertracing/all-in-one:latest`
- You can now run hello world, and do testing

### Run hello world example locally

- Clone this repo from github 
- Create the .env by copying the .example.env
`cp .env.example .env`
- Replace rabbit connect value with dev values (found in 1Password LTS-ETD)
- Replace the `CONSUME_QUEUE_NAME` and `PUBLISH_QUEUE_NAME` with a unique name for local testing (eg - add your initials to the end of the queue names)
- Start up docker  
`docker-compose -f docker-compose-local.yml up --build -d --force-recreate`

- Bring up DEV ETD Rabbit UI
- Look for `CONSUME_QUEUE_NAME` queue

- Exec into the docker container
`docker exec -it rabbitmq-email-notifier bash`
- Run invoke task python script
`python3 scripts/invoke-task.py`

- Look for `PUBLISH_QUEUE_NAME` queue, and get the message in the RabbitMQ UI
- and/or tail <NEED LOG INFO> to see activity


### Manually placing a message on the queue

- Open the queue in the RabbitMQ UI
- Click on the `CONSUME_QUEUE_NAME` queue (the name that you assigned this env value to)
- Open Publish Message
- Set a property of `content_type` to `application/json`
- Set the Payload to the following JSON content
`{"id": "da28b429-e006-49a5-ae77-da41b925bd85","task": "rabbitmq-email-notifier.tasks.send_to_base","args": [{"hello":"world"}]}`

###  Unit Testing
- exec into docker
- `> pytest tests/unit`
- Note, integration tests are run as part of github actions, not locally

### Using OpenTelemetry for tracing
This app uses OpenTelemetry (https://opentelemetry.io/) for live tracing. To see how it is implemented in the application, refer to this wiki: https://wiki.harvard.edu/confluence/display/LibraryTechServices/OpenTelemetry

### Build and publish the package

#### Prepare the distribution
* Update the version number in `setup.py`
* To publish a pre-release version, add a letter and a number after the version number e.g. `0.0.1a1`
* Remove the old `dist/` directory from the previous build if necessary

#### Build the distribution

Once inside the container, build the distribution.

`python3 setup.py sdist bdist_wheel`

A new directory `dist` will be created in the container.

#### Register for an account

[Register for an account](https://test.pypi.org/account/register/) on the test python package repository. Enable two-factor authentication for logins. [Create a token](https://test.pypi.org/manage/account/#api-tokens).

#### Upload package to the test repository

Publish the package to the test repository `testpypi` before publishing it to the production repository.

`python3 -m twine upload --repository testpypi dist/*`

#### Test the package
Open the package in the repository and view the version history.

https://test.pypi.org/project/rabbitmq-email-notifier/0.0.4/

## More information
Read the documenation for more information on building and publishing the distribution.

* [Generating distribution archives](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives)

* [Uploading the distribution archives](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)

* https://tom-christie.github.io/articles/pypi/