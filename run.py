# run.py
import os

from app import app


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    #Cloud
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    #Local
    app.run(host="0.0.0.0", port=5000)
    DEBUG = True
