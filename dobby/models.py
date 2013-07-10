from django.db import models
from django.contrib.sitemaps import Sitemap
import datetime
from django.utils import timezone

#NEW FOR LOGINS
from django.contrib.sessions.models import Session

# Create your models here.

class Team(models.Model):
	name=models.CharField(max_length=200)
	owner=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	#it would be good to add major league team name here

	def __unicode__(self):
		return self.name


class Player(models.Model):
	team=models.ForeignKey(Team)
	name=models.CharField(max_length=200)
	date_added = models.DateTimeField('date added')

	def __unicode__(self):
		return self.name

class Transaction(models.Model):
	team=models.ForeignKey(Team)
	player_name=models.CharField(max_length=200)

	transaction_choices=(
		("added", "added"),
		("demoted", "demoted"),
		("promoted", "promoted"),
		("cut", "cut"),
		("traded", "traded"))
	transaction_type=models.CharField(max_length=100, choices=transaction_choices)
	transaction_date = models.DateTimeField('transaction_date')

	def __unicode__(self):
		return self.player_name+ self.transaction_type

