from django.conf.urls import patterns, include, url

#NEW LOGIN STUFF
from django.contrib.auth.views import login, logout, password_change, password_change_done

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	url(r'^$', 'dobby.views.home', name='home'),
	url(r'^dobby/$', 'dobby.views.index'),
	#url(r'^team/$', 'dobby.views.index'),

	url(r'^team/(?P<team_id>\d+)$', 'dobby.views.team'),
	url(r'^promote/(?P<team_id>\d+)$', 'dobby.views.promote'),
    
    #NEW!
    url(r'^eligibility_check/(?P<team_id>\d+)$', 'dobby.views.eligibilityCheck'),
    
	url(r'^cut/(?P<team_id>\d+)$', 'dobby.views.cut'),
	url(r'^add/(?P<team_id>\d+)$', 'dobby.views.add'),
	url(r'^demote/(?P<team_id>\d+)$', 'dobby.views.demote'),
	url(r'^player/(?P<player_id>\d+)$', 'dobby.views.player'),
	#url(r'^login/$', 'django.contrib.auth.views.login'),

	url(r'^accounts/login/$',  login),
	url(r'^accounts/logout/$', 'dobby.views.logout_view'),
	url(r'^accounts/password_change/$',  password_change),
	url(r'^accounts/password_change_done/$',  password_change_done),
	url(r'^transactionlog/$',  'dobby.views.transaction_log'),
	#url(r'^login/$', 'django.contrib.auth.views.login'),
	#url(r'^logout/$', logout),


	#url('/', 'dobby.views.index'),
	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
	
    url(r'^email/$',  'dobby.views.email_moves')
    
)
