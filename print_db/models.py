# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Event(models.Model):
    event_id = models.IntegerField(db_column='event_ID', primary_key=True)  # Field name made lowercase.
    event_name = models.CharField(max_length=45, blank=True, null=True)
    reward = models.CharField(max_length=45, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'event'


class Imply(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event_ID', primary_key=True)  # Field name made lowercase.
    place = models.ForeignKey('Place', models.DO_NOTHING, db_column='place_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'imply'
        unique_together = (('event', 'place'),)


class Participation(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user_ID', primary_key=True)  # Field name made lowercase.
    event = models.ForeignKey(Event, models.DO_NOTHING, db_column='event_ID')  # Field name made lowercase.
    number_of_visits = models.IntegerField(db_column='Number_of_visits', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'participation'
        unique_together = (('user', 'event'),)


class Place(models.Model):
    place_id = models.IntegerField(db_column='place_ID', primary_key=True)  # Field name made lowercase.
    place_name = models.CharField(max_length=45)
    address = models.CharField(max_length=45, blank=True, null=True)
    explanation = models.CharField(max_length=45, blank=True, null=True)
    qr_message = models.CharField(db_column='QR_message', max_length=45, blank=True, null=True)  # Field name made lowercase.
    coordinate = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place'


class User(models.Model):
    user_id = models.CharField(db_column='user_ID', primary_key=True, max_length=45)  # Field name made lowercase.
    user_password = models.CharField(max_length=45)
    user_email = models.CharField(max_length=45, blank=True, null=True)
    user_information = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
