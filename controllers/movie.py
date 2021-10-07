from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS,ACTOR_FIELDS
from controllers.parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
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
    if 'name' not in data.keys():
        err = 'Name was not specified'
        return make_response(jsonify(err),400)
    if 'year' not in data.keys() or int(data['year'])>2020:
        err = 'Year was not specified or in wrong format'
        return make_response(jsonify(err),400)
    if 'genre' not in data.keys():
        err = 'genre was not specified'
        return make_response(jsonify(err),400)
    if len(data.keys())>3:
        err = 'Redundant field'
        return make_response(jsonify(err),400)
    # use this for 200 response code
    new_record = Movie.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_actor), 200)


def update_movie():
    """
    Update movie record by id
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
        if 'name' not in data.keys() and 'year' not in data.keys() and 'genre' not in data.keys():
            err = 'No data specified'
            return make_response(jsonify(err), 400)
        movie_new_dict={}
        if 'name' in data.keys():
            movie_new_dict['name']=data['name']
        if 'year' in data.keys():
            movie_new_dict['year']=data['year']
        if 'genre' in data.keys():
            movie_new_dict['genre'] = data['genre']
    # use this for 200 response code
        upd_record = Movie.update(row_id,**movie_new_dict)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_actor), 200)
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

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        Movie.delete(row_id)
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
    if 'id' in data.keys() and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
            rel_row_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        obj = Movie.query.filter_by(id=row_id).first()
        rel_obj = Actor.query.filter_by(id=rel_row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
            rel_actor = {k: v for k, v in rel_obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id(s) does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        movie = Movie.add_relation(row_id,rel_obj)
        movie_dict = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movie_dict['actors'] = str(movie.actors)
        return make_response(jsonify(movie_dict), 200)
    else:
        err = 'Ids must be specified'
        return make_response(jsonify(error=err), 400)


def movie_clear_relations():
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

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id(s) does not exist'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        movie = Movie.clear_relations(row_id)# clear relations here
        movie_dict = {k: v for k, v in movie.__dict__.items() if k in ACTOR_FIELDS}
        movie_dict['filmography'] = str(movie.actors)
        return make_response(jsonify(movie_dict), 200)
    else:
        err = 'Ids must be specified'
        return make_response(jsonify(error=err), 400)