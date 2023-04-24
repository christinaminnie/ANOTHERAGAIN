from adoption_site import db


class AbstractBaseModel(db.Model):
    __abstract__ = True
