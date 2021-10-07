import re

from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS,MOVIE_FIELDS  # to make response pretty
from controllers.parse_request import get_request_data


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
    if 'name' not in data.keys():
        err = 'Name was not specified'
        return make_response(jsonify(err),400)
    if 'gender' not in data.keys():
        err = 'Gender was not specified'
        return make_response(jsonify(err),400)
    if 'date_of_birth' not in data.keys() or\
            not re.match(r'^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)[0-9]{2}$',data['date_of_birth']):
        err = 'Date was not specified or in wrong format'
        return make_response(jsonify(err),400)
    if len(data.keys()) > 3:
        err = 'Redundant field'
        return make_response(jsonify(err), 400)
    # use this for 200 response code
    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
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
        if 'name' not in data.keys() and 'gender' not in data.keys() and 'date_of_birth' not in data.keys():
            err = 'No data specified to change'
            return make_response(jsonify(err), 400)
        if 'date_of_birth' in data.keys() and not re.match(r'^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)[0-9]{2}$', data['date_of_birth']):
            err = 'Date in wrong format'
            return make_response(jsonify(err), 400)
        actor_new_dict={}
        if 'name' in data.keys():
            actor_new_dict['name']=data['name']
        if 'gender' in data.keys():
            actor_new_dict['gender']=data['gender']
        if 'date_of_birth' in data.keys():
            actor_new_dict['date_of_birth'] = data['date_of_birth']

        upd_record = Actor.update(row_id, **actor_new_dict)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        Actor.delete(row_id)
        msg = 'Record successfully deleted'
        return make_response(jsonify(message=msg), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    # use this for 200 response code

    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys() and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
            rel_row_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        rel_obj = Movie.query.filter_by(id=rel_row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
            rel_movie = {k: v for k, v in rel_obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id(s) does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        actor = Actor.add_relation(row_id,rel_obj)
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.movies)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'Ids must be specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
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
            err = 'Record with such id(s) does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        actor = Actor.clear_relations(row_id)# clear relations here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.movies)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'Ids must be specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###