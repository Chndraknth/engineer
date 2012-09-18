"""This is the database. All models are defined here.
"""

from django.db import models
from datetime import datetime
from django.utils.timezone import utc
# Create your models here.

class Participant(models.Model):
    """Class that holds the details of each participant.
    Here, id (P_ID) is generated automatically by django and we can 
    use the same.
    """
    slug = models.CharField("Slug", \
                            max_length = 32, \
                            blank = False, \
                            primary_key = True, \
                            )
    name = models.CharField("Name", \
                            max_length = 512, \
                            blank = False, \
                            )
    email = models.EmailField("Email")
    fb_id = models.CharField("Fb ID", \
                            max_length = 128, \
                            )
    events = models.ManyToManyField("Round", \
                                    )
    def __unicode__(self):
        return self.name

class Committee(models.Model):
    """Class that holds details of each committee.
    """
    name = models.CharField("Committee Name", \
                            max_length = 128, \
                            blank = False, \
                            )
    def __unicode__(self):
        return self.name


class Event(models.Model):
    """Class that holds details of each event.
    Rounds have a foreignkey into this.
    Prizes too.
    """
    name = models.CharField("Event Name", \
                            max_length = 512, \
                            blank = False, \
                            )
    description = models.TextField("Event Description", 
                                    blank = True \
                                    )
    committee = models.ForeignKey('Committee', \
                                    default = None, \
                                    related_name = "committee", \
                                    )
    def __unicode__(self):
        return self.name
    
class Round(models.Model):
    """
    Class that holds the details of each round, including
    where the round is going to be held, when and so on.
    """
    event = models.ForeignKey('Event', \
                                default = None, \
                                related_name = "round", \
                                )
    number = models.CharField(
                            "Round Number", \
                            max_length = 8, \
                            blank = False, \
                            )
    name = models.CharField("Round Name", \
                            max_length = 128, \
                            blank = False, \
                            )
    venue = models.CharField("Venue", \
                            max_length = 128, \
                            blank = True, \
                            )
    description = models.TextField("Description", \
                            blank = True, \
                            max_length = 512, \
                            )
    coordinator = models.CharField("Coordinator", \
                            max_length = 128, \
                            blank = True, \
                            )
    phone = models.CharField("Phone", \
                            max_length = 128, \
                            blank = True, \
                            )
    start_time = models.DateTimeField("Start Time", \
                            default = datetime.utcnow()\
                                .replace(tzinfo = utc)
                            )
    def __unicode__(self):
        return self.event.__unicode__()+", "+self.name
