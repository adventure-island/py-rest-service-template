# """
# This module defines NDB datastore models.
# """

# from google.cloud import ndb


# class User(ndb.Model):
#     id = ndb.StringProperty(required=True)
#     user_type = ndb.StringProperty(required=True)
#     name = ndb.StringProperty(required=True)
#     dob = ndb.DateProperty(required=True)
#     password = ndb.StringProperty(required=True)
#     email = ndb.StringProperty()
#     dt_added = ndb.DateTimeProperty()
