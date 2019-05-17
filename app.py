import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'songbook'
app.config["MONGO_URI"] = 'mongodb+srv://cockneypirate:r00tUser@myfirstcluster-gzncr.mongodb.net/songbook?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')
@app.route('/song_list')
def song_list():
    filter1 = request.args.get('filter1')
    filter2 = request.args.get('filter2')
    query={}
    if filter1 == "explicit1":
        query["explicit_lyrics"]="yes"
    if filter1 == "explicit2":
        query["explicit_lyrics"]="no"
    if filter2 == "original1":
        query["original_song"]="yes"
    if filter2 == "original2":
        query["original_song"]="no"
    songs=mongo.db.songs.find(query)
    return render_template("songs.html", songs=list(songs), filter1=filter1, filter2=filter2)
    
@app.route('/add_song')
def add_song():
    return render_template("add_song.html", songs=mongo.db.songs.find())


@app.route('/insert_song', methods=['POST'])
def insert_song():
    insert = mongo.db.songs
    insert.insert_one(request.form.to_dict())
    return redirect(url_for('song_list'))
    
    
                           
@app.route('/view_song/<song_id>')
def view_song(song_id):
    select_song =  mongo.db.songs.find_one({"_id": ObjectId(song_id)})
    all_songs =  mongo.db.songs.find()
    return render_template('view_song.html', song=select_song,
                           songs=all_songs)
                           
@app.route('/edit_song/<song_id>')
def edit_song(song_id):
    select_song =  mongo.db.songs.find_one({"_id": ObjectId(song_id)})
    all_songs =  mongo.db.songs.find()
    return render_template('edit_song.html', song=select_song,
                           songs=all_songs)

@app.route('/update_song/<song_id>', methods=["POST"])
def update_song(song_id):
    song = mongo.db.songs
    song.update({'_id': ObjectId(song_id)},
    {
        'song_name':request.form.get('song_name'),
        'song_writer':request.form.get('song_writer'),
        'song_lyrics':request.form.get('song_lyrics'),
        'artist_name':request.form.get('artist_name'),
        'original_song':request.form.get('original_song'),
        'explicit_lyrics':request.form.get('explicit_lyrics')
    })
    return redirect(url_for('song_list'))
    
@app.route('/delete_song/<song_id>')
def delete_song(song_id):
    mongo.db.songs.remove({'_id': ObjectId(song_id)})
    return redirect(url_for('song_list'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)