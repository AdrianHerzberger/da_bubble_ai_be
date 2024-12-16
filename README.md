# Install requirement:
pip install --no-cache-dir -r requirements.txt

# Deploy both containers Elasticsearch container:
docker run -d -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.0

docker-compose up -d

# activate venv 
.\venv\Scripts\activate

# Run Da Bubble app:
python run.py


# Run unittests:
python -m unittest