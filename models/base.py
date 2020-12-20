from core import db


def commit(obj):
    """
    Function for convenient commit
    """
    db.session.add(obj)
   #print(db.session.query(obj.__class__).all())
    db.session.commit()
   #print(db.session.query(obj.__class__).all())
    db.session.refresh(obj)
   #print(db.session.query(obj.__class__).all())
    return obj


class Model(object):
    @classmethod
    def create(cls, **kwargs):
        """
        Create new record

        cls: class
        kwargs: dict with object parameters
        """
        obj = cls(**kwargs)
        return commit(obj)

    @classmethod
    def update(cls, row_id, **kwargs):
        """
        Update record by id

        cls: class
        row_id: record id
        kwargs: dict with object parameters
        """
        obj = cls.query.filter_by(id=row_id).first()
        if obj:
            if cls.__name__ == 'Actor':
                if 'name' in kwargs.keys():
                    obj.name = kwargs['name']
                if 'gender' in kwargs.keys():
                    obj.gender = kwargs['gender']
                if 'date_of_birth' in kwargs.keys():
                    obj.date_of_birth = kwargs['date_of_birth']
            elif cls.__name__ == 'Movie':
                if 'name' in kwargs.keys():
                    obj.name = kwargs['name']
                if 'genre' in kwargs.keys():
                    obj.genre = kwargs['genre']
                if 'year' in kwargs.keys():
                    obj.year = kwargs['year']


            db.session.flush()


            return commit(obj)
    
    @classmethod
    def delete(cls, row_id):
        """
        Delete record by id

        cls: class
        row_id: record id
        return: int (1 if deleted else 0)
        """
        try:
            db.session.delete(cls.query.filter_by(id=row_id).first())
            db.session.commit()
            return 1
        except:
            return 0

    
    @classmethod
    def add_relation(cls, row_id, rel_obj):  
        """
        Add relation to object

        cls: class
        row_id: record id
        rel_obj: related object
        """      
        obj = cls.query.filter_by(id=row_id).first()
        if obj:
            if cls.__name__ == 'Actor':
                obj.filmography.append(rel_obj)
            elif cls.__name__ == 'Movie':
                obj.cast.append(rel_obj)
            return commit(obj)
            
    @classmethod
    def remove_relation(cls, row_id, rel_obj):
        """
        Remove certain relation

        cls: class
        row_id: record id
        rel_obj: related object
        """
        obj = cls.query.filter_by(id=row_id).first()
        
        if obj:
            if cls.__name__ == 'Actor':
                obj.filmography.remove(rel_obj)
            elif cls.__name__ == 'Movie' :
                obj.cast.remove(rel_obj)
            return commit(obj)

    @classmethod
    def clear_relations(cls, row_id):
        """
        Remove all relations by id

        cls: class
        row_id: record id
        """
        obj = cls.query.filter_by(id=row_id).first()
        if obj:
            if cls.__name__ == 'Actor':
                obj.filmography = []
            elif cls.__name__ == 'Movie' :
                obj.cast = []
            
            return commit(obj)

    