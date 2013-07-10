from django.contrib import admin
from dobby.models import Team

#Teams
class TeamAdmin(admin.ModelAdmin):
	pass

admin.site.register(Team, TeamAdmin)


#Players
from dobby.models import Player

class PlayerAdmin(admin.ModelAdmin):
	pass

admin.site.register(Player, PlayerAdmin)

#TRANSACTIONS
from dobby.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
	pass

admin.site.register(Transaction, TransactionAdmin)
