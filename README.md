# Setup to run
Create a connection on your airflow name postgresql_conn with the information below:
- host : name of your docker container
- schema : algolia_wh
- login : algolia_user
- password : in the docker-compose.yml

Run the following then '''docker-compose up'''

You can now launch your dag