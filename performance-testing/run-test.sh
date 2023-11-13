echo "--------------------------------------------------------------------------------------"
echo "Performance Testing"
echo "--------------------------------------------------------------------------------------"

#Choose what endpoint to test, pay attention to change de TEST_TYPE to stress ou load
#If you wanto to run in another environment, add the config in utils/data.js

#Reporting to Influxdb and Grafana Locally

docker-compose run --rm k6 run /scripts/get_all_users.js -e ENV=local -e TEST_TYPE=stress -e K6_OUT=influxdb=http://influxdb:8086/k6
# docker-compose run --rm k6 run /scripts/create_booking.js -e ENV=local -e TEST_TYPE=load -e K6_OUT=influxdb=http://influxdb:8086/k6

#Report to k6 Grafana Cloud

# docker-compose run --rm k6 login cloud -t <API_TOKEN>
# docker-compose run --rm k6 run --out cloud /scripts/get_all_users.js -e ENV=local -e TEST_TYPE=stress -e K6_CLOUD_TOKEN=<API_TOKEN>
# docker-compose run --rm k6 run --out cloud /scripts/create_booking.js -e ENV=local -e TEST_TYPE=load -e K6_CLOUD_TOKEN=<API_TOKEN>
