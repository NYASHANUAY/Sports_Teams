from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.user import User


DATABASE = "sports_db"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Team:
    def __init__(self, data):
        self.id = data['id']
        self.sport = data['sport']
        self.city = data['city']
        self.date = data['date']
        self.roaster = data['roaster']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def addTeam(cls, data):
        query = """
                    INSERT INTO teams (sport, city, date, roaster, user_id)
                    VALUES (%(sport)s, %(city)s, %(date)s, %(roaster)s,  %(user_id)s);
                    """

        id = connectToMySQL(DATABASE).query_db(query, data)

        if (id):
            print('successfully added team to database')
            return id
        else:
            print("Didn't add to database")
            return False

    @classmethod
    def getAllTeams(cls):
        query = "SELECT * FROM teams JOIN users ON users.id = teams.user_id;"

        results = connectToMySQL(DATABASE).query_db(query)
        teams = []
        for row in results:
            team = Team(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],

            }
            user = User(user_data)
            team.user = user
            teams.append(team)

        return teams

    @classmethod
    def update(cls, data):
        query = "UPDATE teams SET sport =%(sport)s, city= %(city)s, date=%(date)s, roaster=%(roaster)s WHERE id= %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validateTeam(data):
        is_valid = True
        # Validates name
        if len(data['sport']) == 0:
            flash('Sport field must not be empty', 'sport')
            is_valid = False

        # Validates event
        if len(data['city']) == 0:
            flash('City field must not be empty', 'city')
            is_valid = False

        # Validates date_made
        if not data["date"]:
            flash('Must set Date', 'date')
            is_valid = False

        if not data["roaster"]:
            flash('Must set Roaster', 'roaster')
            is_valid = False

        return is_valid

    @classmethod
    def delete(cls, team_id):
        query = "DELETE FROM teams WHERE id = %(team_id)s;"
        data = {
            "team_id": team_id,
        }

        connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def editTeam(cls, data):
        query = "UPDATE teams SET sport = %(sport)s, city = %(city)s, date = %(date)s, roaster= %(roaster)s WHERE id = %(id)s;"

        connectToMySQL(DATABASE).query_db(query, data)

        return

    @classmethod
    def getTeam(cls, user_id):
        query = "SELECT * FROM teams WHERE id = %(user_id)s;"

        data = {
            'user_id': user_id
        }

        results = connectToMySQL(DATABASE).query_db(query, data)

        if (results):
            teams = cls(results[0])
            return teams
        else:
            return False
