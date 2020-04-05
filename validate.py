def validate_movie(movie):
    if movie.title == '' or movie.release_date == '':
        return False
    else:
        return True


def validate_actor(actor):
    if actor.name == '' or actor.gender == '' or actor.age == '':
        return False
    else:
        return True
