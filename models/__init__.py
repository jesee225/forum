from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReprMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def update(cls, model_id, form):
        m = cls.query.get(model_id)
        m._update(form)
        m.save()

    @classmethod
    def remove(cls, model_id):
        m = cls.query.get(model_id)
        m.delete()
