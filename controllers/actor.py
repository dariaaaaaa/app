from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models import Actor, Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT     # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """  
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200) 

  
def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400) 

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    if all(key in data.keys() for key in ACTOR_FIELDS[1:]):
    # use this for 200 response code
            
        try:
            date = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
            #data['date_of_birth'] = date
        except:
            err = 'Incorrect date format'
            return make_response(jsonify(error=err), 400)
        
        #if not str(data['name']).replace(' ', '').isalpha() or str(data['gender']).replace(' ', '').isalpha():
        #    err = 'Name and gender must be strings'
        #    return make_response(jsonify(error=err), 400)
        
        
        try:
            new_record = Actor.create(**data)
            new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
            return make_response(jsonify(new_actor), 200)
        except:
            err = 'Smth goes wrong while creating Actor'
            return make_response(jsonify(error=err), 400)
        
    else:
        err = 'Not all values specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys() and all(key in ACTOR_FIELDS for key in data.keys()):
        
        try:
            row_id = int(data['id'])
            del data['id']
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        
        if 'date_of_birth' in data.keys():
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
                
            except:
                err = 'Incorrect date format'
                return make_response(jsonify(error=err), 400)
            
      #  if 'name' in data.keys() and not str(data['name']).replace(' ', '').isalpha():
      #      err = 'Name must be string'
      #      return make_response(jsonify(error=err), 400)
        
      #  if 'gender' in data.keys() and not str(data['gender']).replace(' ', '').isalpha():
      #      err = 'Gender must be string'
      #      return make_response(jsonify(error=err), 400)
        
        # use this for 200 response code
        upd_record = Actor.update(row_id, **data)
        try:
            upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        except:   
            err = 'Smth goes wrong while updating'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(upd_actor), 200)
    
    else:
        err = 'Not valid data'
        return make_response(jsonify(error=err), 400)
        
            
    ### END CODE HERE ###

def delete_actor():
    """
    Delete actor by id
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
        obj = Actor.delete(row_id)
        
        if obj == 0:
            err = 'Smth goes wrong while deleting'
            return make_response(jsonify(error=err), 400)
        
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400) 
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
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
    
        rel_obj = Movie.query.get(relation_row_id)
        
        if rel_obj is None:
            err = 'Record with such id does not exist (movie)'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        actor = Actor.add_relation(row_id, rel_obj) 
        try:# add relation here
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
        except:
            err = 'Record with such id does not exist (actor)'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
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
        
        actor = Actor.clear_relations(row_id)    # clear relations here
        
        try:
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###
