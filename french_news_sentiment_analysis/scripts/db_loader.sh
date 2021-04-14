# Script to load data into database while the scrapper is running concurrently
# Will load available data, then sleep until more data is found.
cd ..
while true; do
  python unzip_clean_load_single.py
  echo "Sleeping 400 seconds"
  sleep 400
done
