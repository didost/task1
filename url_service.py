from flask import Flask, Response
import requests
import time
from prometheus_client import CollectorRegistry, Gauge, generate_latest

app = Flask(__name__)

def check_url(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # in milliseconds
        is_up = response.status_code == 200
        return is_up, response_time
    except requests.exceptions.RequestException:
        return False, None

@app.route('/metrics')
def metrics():
    url1 = 'https://httpstat.us/503'
    url2 = 'https://httpstat.us/200'

    is_up_1, response_time_1 = check_url(url1)
    is_up_2, response_time_2 = check_url(url2)

    # Create a registry and add metrics to it
    registry = CollectorRegistry()
    gauge_url1_up = Gauge('url1_up', 'Check if url1 is up', registry=registry)
    gauge_url1_response_time = Gauge('url1_response_time_ms', 'Response time for url1 in ms', registry=registry)
    gauge_url2_up = Gauge('url2_up', 'Check if url2 is up', registry=registry)
    gauge_url2_response_time = Gauge('url2_response_time_ms', 'Response time for url2 in ms', registry=registry)

    # Set values for the metrics
    gauge_url1_up.set(1 if is_up_1 else 0)
    gauge_url1_response_time.set(response_time_1 if response_time_1 else 0)
    gauge_url2_up.set(1 if is_up_2 else 0)
    gauge_url2_response_time.set(response_time_2 if response_time_2 else 0)

    # Generate the metrics output in Prometheus format
    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
