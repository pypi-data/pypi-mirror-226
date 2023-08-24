# HOUSES Client
A Python Client SDK for the [Mayo Clinic HOUSES API](https://www.mayo.edu/research/centers-programs/mayo-clinic-houses-program/overview)

# Requirements
Python 3.9+

# Installation
```shell script
pip install houses-client
```

# Example Usage
```python
from houses_client import client

#Create a client passing in your API client id and client secret
client = client.HousesClient(api_endpoint="https://houses.konfidential.io", 
  client_id="my oidc client id", 
  client_secret="my oidc client secret",
  log_level="INFO")

# Submit batch request reading from myinput.csv and writing results to myoutput.csv
client.batch("myinput.csv", "myoutput.csv")
```

# Build
```shell script
pyton3 -m pip install --upgrade build
```
```shell script
python3 -m build
```
