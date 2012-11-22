"""This is the database. All models are defined here.
"""

from django.db import models
from datetime import datetime
from django.utils.timezone import utc
# Create your models here.

class Participant(models.Model):
    """Class that holds the details of each participant.
    """

    slug = models.SlugField(
        "Slug",
        max_length = 32,
        blank = False
    )
    name = models.CharField("Name",
        max_length = 512,
        blank = False,
    )
    college_id = models.ForeignKey(
        "College",
        blank = False
    )

    roll_no = models.CharField(
        "Roll Number",
        max_length = 512,
        blank = False
    )

    email = models.EmailField("Email")

    fb_id = models.CharField(
        "Facebook",
        max_length = 128,
    )
    events = models.ManyToManyField(
        "Round",
        through = "Participation",
        blank = True,
    )

    def __unicode__(self):
        return self.name

class College(models.Model):
    name = models.CharField(
        "Name",
        max_length = 512,
        blank = False
    )
    address = models.TextField(
        "Address",
        blank = False
    )

    city = models.TextField(
        "City",
        max_length = 512,
        blank = False
    )
    def __unicode__(self):
        return self.name


class Committee(models.Model):
    """
        Class that holds details of each committee.
    """
    name = models.CharField(
        "Name",
        max_length = 128,
        blank = False,
    )

    contact = models.CharField(
        "Contact",
        max_length = 128,
        blank = True
    )

    def __unicode__(self):
        return self.name


class Event(models.Model):
    """Class that holds details of each event.
    Rounds have a foreignkey into this.
    Prizes too.
    """
    name = models.CharField(
        "Name",
        max_length = 512,
        blank = False,
    )
    description = models.TextField(
        "Description",
        blank = True
    )

    committee = models.ForeignKey(
        'Committee',
        default = None,
        related_name = "committee",
    )
    start_date = models.DateTimeField(
        "Start Time",
        default = datetime.utcnow().replace(tzinfo=utc),
        blank = True
    )
    rounds = models.IntegerField(
        "No. of Rounds",
        default = 1,
        blank = False
    )


    def __unicode__(self):
        return self.name

class Round(models.Model):
    """
    Class that holds the details of each round, including
    where the round is going to be held, when and so on.
    """
    event = models.ForeignKey('Event',
        default = None,
        related_name = "round",
    )
    number = models.CharField(
        "Number",
        max_length = 8,
        blank = False,
    )
    name = models.CharField(
        "Name",
        max_length = 128,
        blank = False,
    )
    venue = models.CharField(
        "Venue",
        max_length = 128,
        blank = True,
    )

    description = models.TextField(
        "Description",
        blank = True,
        max_length = 512,
    )
    coordinator = models.CharField(
        "Coordinator",
        max_length = 128,
        blank = True,
    )
    phone = models.CharField(
        "Phone",
        max_length = 128,
        blank = True,
    )
    start_time = models.DateTimeField(
        "Start Time",
        default = datetime.utcnow().replace(tzinfo = utc)
            )
    end_time = models.DateTimeField(
        "End Time",
        default = datetime.utcnow().replace(tzinfo = utc)
    )

    def __unicode__(self):
        return self.event.__unicode__()+", "+self.name


class Prize(models.Model):
    p_id = models.ForeignKey(Participant )
    e_id = models.ForeignKey(Event)

    position = models.IntegerField(
        "Position",
        default = 1
    )
    prize_money = models.IntegerField(
        "Amount",
        blank = False
    )
    recieved = models.BooleanField(
        "Recieved status",
        blank = False,
        default = False
    )
    def __unicode__(self):
        return "%s, %s in %s"%(self.p_id, str(self.position), self.e_id)


class Participation(models.Model):
    p_id = models.ForeignKey(
        Participant
    )

    r_id = models.ForeignKey(
        Round
    )

    score = models.IntegerField(
        "Score",
        blank = True
    )

    comment = models.TextField(
        "Comments",
        blank = True
    )

    def __unicode__(self):
        return "%s in %s"%(self.p_id, self.r_id)

