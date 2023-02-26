from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash, session
from flask_app import app

class Show:
    db = "tv_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.network = data["network"]
        self.date_made = data["date_made"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db).query_db(query)
        shows = []
        for row in results:
            shows.append(row)
        return shows
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM shows WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM shows WHERE name=%(name)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO shows (name, network, date_made, description, user_id) VALUES (%(name)s, %(network)s, %(date_made)s, %(description)s, %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET name=%(name)s, network=%(network)s, date_made=%(date_made)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM shows WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_show(show):
        is_valid = True
        show_in_db = Show.get_by_name(show)
        if show_in_db:
            flash("A Show with that name already exists")
            is_valid = False
        if len(show["name"]) < 3:
            flash("Name must be at least three characters")
            is_valid = False
        if len(show["network"]) < 3:
            flash("Network must be at least three characters")
            is_valid = False
        if len(show["description"]) < 3:
            flash("Description must be at least three characters")
            is_valid = False
        if not show["date_made"]:
            flash("Date cannot be blank")
            is_valid = False

        return is_valid
