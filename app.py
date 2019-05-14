import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'songbook'
app.config["MONGO_URI"] = 'mongodb+srv://cockneypirate:r00tUser@myfirstcluster-gzncr.mongodb.net/songbook?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')
@app.route('/songs')
def get_songs():
    return render_template("songs.html", categories=mongo.db.categories.find())
    
@app.route('/add_song')
def add_song():
    return render_template("add_song.html", categories=mongo.db.categories.find())


@app.route('/insert_song', methods=['POST'])
def insert_song():
    insert = mongo.db.categories
    insert.insert_one(request.form.to_dict())
    return redirect(url_for('get_songs'))
    
    
                           
@app.route('/view_song/<categories_id>')
def view_song(categories_id):
    the_task =  mongo.db.categories.find_one({"_id": ObjectId(categories_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('view_song.html', task=the_task,
                           categories=all_categories)



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)