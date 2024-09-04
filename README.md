# Big Data Final Project

The purpose of this readme is to get the application running as a local version, using docker images for rabbitMQ and mongoDB. If you are feeling ambitious you can go to cloudAMPQ and mongoDB and get your own URIs for a rabbitMQ channel and a mongoDB cluster and place them in an .env file at the top level repo with the variables MONGO_URI and CLOUDAMPQ_URI to make the make the application cloud based. I have also commented throughout the code where you would need to make simple changes if you decide to try and run a cloud based version. The commands here are for powershell on Windows, you may have to adjust based on your OS.

## Run docker images 

1. Make sure docker is open on desktop

2. Run rabbitMQ in docker
    ```
    docker run -d --hostname rmq --name rabbit-server -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
    ```
3. run MongoDB in docker
    ```
    docker run -d -p 27017:27017 --name m1 mongo
    ```

## Run the backend

1.  Run the reciever in its own terminal.

    ```
    python .\backend\mainReciever.py
    ```

## Run the frontend (main web App)

1.  Run app.py with waitress in a separate terminal.

    ```
    cd ./frontend/website ; waitress-serve --call 'app:create_app'
    ```

## Check out the application
Go to http://localhost:8080 to initate the application It may take a few seconds to process the data so waiting a few seconds and refreshing the page may be required. You can view the plain text metrics at http://localhost:8080/metrics. You will see the jobs and messages printing in the terminal and you can view the rabbitMQ management dashboard form local host 5672. The deployed version is here: https://frontend-t3sb.onrender.com

## API Key FYI

The API key used to call balance sheet data from https://financialmodelingprep.com/ is hardcoded in the code. I know this is not good practice but it is included for convenince and it is free so I am not overly concerned with financial risks. It is limited to 250 calls per day, so if you keep clearing the persistence layer and re-requesting data the API may lock you out, but the app is designed to only make 30 calls on run, so this is unlikely and even if it does happen you can create your own API key for free as well.