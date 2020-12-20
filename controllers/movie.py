from flask import jsonify, make_response

from ast import literal_eval

from models import Movie, Actor
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mv = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mv)
    return make_response(jsonify(movies), 200)

def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400) 

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 

def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    all_values = True
    for i in MOVIE_FIELDS:
        if i not in data.keys() and i != 'id':
            all_values = False
    if all_values:
    # use this for 200 response code
        if 'id' in data.keys():
            try:
                row_id = int(data['id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)
            
        try:
            year = int(data['year'])
            #data['year'] = year
        except:
            err = 'Incorrect year format'
            return make_response(jsonify(error=err), 400)
        
        #if not str(data['name']).replace(' ', '').isalpha() or str(data['genre']).replace(' ', '').isalpha():
        #    err = 'Name and genre must be strings'
        #    return make_response(jsonify(error=err), 400)
        
        try:
            new_record = Movie.create(**data)
            new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}      
        except:
            err = 'Smth goes wrong while creating Movie'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(new_movie), 200)
    
    else:
        err = 'Not all values specified'
        return make_response(jsonify(error=err), 400)

def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        if 'year' in data.keys():
            try:
                year = int(data['year'])
       #         data['year'] = year
            except:
                err = 'Incorrect year format'
                return make_response(jsonify(error=err), 400)
            
       # if 'name' in data.keys() and not str(data['name']).replace(' ', '').isalpha():
       #     err = 'Name must be string'
       #     return make_response(jsonify(error=err), 400)
        
       # if 'genre' in data.keys() and not str(data['genre']).replace(' ', '').isalpha():
       #     err = 'Genre must be string'
       #     return make_response(jsonify(error=err), 400)
        
        # use this for 200 response code
        upd_record = Movie.update(row_id, **data)
        try:
            upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        except:   
            err = 'Smth goes wrong while updating'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(upd_movie), 200)
    
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        # use this for 200 response code
        obj = Movie.delete(row_id)
        
        if obj == 0:
            err = 'Smth goes wrong while deleting'
            return make_response(jsonify(error=err), 400)
        
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
            relation_row_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    
        rel_obj = Actor.query.get(relation_row_id)
        
        if rel_obl is None:
            err = 'Record with such id does not exist (actor)'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        movie = Movie.add_relation(row_id, rel_obj) 
        try:# add relation here
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
        except:
            err = 'Record with such id does not exist (movie)'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    
    # use this for 200 response code
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        movie = Movie.clear_relations(row_id)    # clear relations here
        
        try:
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)