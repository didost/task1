from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Function to fetch the status of a URL
def fetch_url_status(url):
    try:
        response = requests.get(url)
        return {'url': url, 'status_code': response.status_code, 'reason': response.reason}
    except requests.exceptions.RequestException as e:
        return {'url': url, 'error': str(e)}

# Route to query the two URLs
@app.route('/query', methods=['GET'])
def query_urls():
    url1 = 'https://httpstat.us/503'
    url2 = 'https://httpstat.us/200'

    result1 = fetch_url_status(url1)
    result2 = fetch_url_status(url2)

    return jsonify({'result1': result1, 'result2': result2})

if __name__ == '__main__':
    app.run(debug=True)
