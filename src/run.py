import sys

sys.path.append(".")
from src.app import app
import cloudinary.api
from src.config import PORT, CN_CLOUD_NAME, CN_API_SECRET, CN_API_KEY

__author__ = 'ishween'

cloudinary.config(
    cloud_name=CN_CLOUD_NAME,
    api_key=CN_API_KEY,
    api_secret=CN_API_SECRET
)

app.run(debug=app.config['DEBUG'], port=PORT, host='0.0.0.0')
