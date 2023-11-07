# Standard Library imports

# Core Flask imports

# Third-party imports
from mongoengine import signals

# App imports
from app.models import User


signals.pre_save.connect(User.pre_save, sender=User)