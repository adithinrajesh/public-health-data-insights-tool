from app import create_app
import logging

# Force Werkzeug to show the URL
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

app = create_app()

if __name__ == "__main__":
    print("Flask starting... Visit http://127.0.0.1:5000")
    app.run(debug=True)
