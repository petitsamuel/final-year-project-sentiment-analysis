echo "Starting DB, this may take a while the first time as it will download mysql docker images and initialise the database"
docker-compose up -d
echo "Waiting on Database to be running and initialised."
sleep 2
status=$(docker inspect --format='{{.State.Health.Status}}' fr_news_db)
while [ "$status" != "healthy" ]; do
    echo "Waiting on Database to be running and initialised -- current status: $status"
    sleep 2
    status=$(docker inspect --format='{{.State.Health.Status}}' fr_news_db)
done
echo "Database container up and running."
