# Script to load data into database while the scrapper is running concurrently
# Will load available data, then sleep until more data is found.
cd ..
while true; do
  python load_data_into_db.py
  echo "Sleeping 400 seconds"
  sleep 400
done
