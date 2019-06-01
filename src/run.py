from src.app import app
import os

print("dekh le andhi ldki: ".upper(),os.environ['PYTHONPATH'])

if 'PYTHONPATH' in os.environ:
    oldEnvVar = os.environ['PYTHONPATH']
else:
    oldEnvVar = ""

oldEnvVar += ":."
os.environ['PYTHONPATH'] = oldEnvVar

port = 5000
if 'PORT' in os.environ:
    port = os.environ['PORT']

__author__ = 'ishween'

app.run(debug=app.config['DEBUG'], port=port,host='0.0.0.0')
