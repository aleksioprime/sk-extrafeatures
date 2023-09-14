from app import app, db
import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host=os.getenv('HOST'), port=int(os.getenv('PORT')))