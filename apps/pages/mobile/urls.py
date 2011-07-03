from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'pages.mobile.views.index', name='mobile_index'),
    url(r'^landing/$', 'pages.mobile.views.landing', name='mobile_landing'),
    url(r'^smartgrid/$', 'pages.mobile.views.smartgrid', name='mobile_smartgrid'),
    url(r'^smartgrid/basicenrg/$', 'pages.mobile.views.basicenrg', name='mobile_basic_enrg'),
    url(r'^smartgrid/getstarted/$', 'pages.mobile.views.getstarted', name='mobile_get_started'),
    url(r'^smartgrid/movingon/$', 'pages.mobile.views.movingon', name='mobile_moving_on'),
    url(r'^smartgrid/lightsout/$', 'pages.mobile.views.lightsout', name='mobile_lights_out'),
    url(r'^smartgrid/makewatts/$', 'pages.mobile.views.makewatts', name='mobile_make_watts'),
    url(r'^smartgrid/potpourri/$', 'pages.mobile.views.potpourri', name='mobile_pot_pourri'),
    url(r'^smartgrid/opala/$', 'pages.mobile.views.opala', name='mobile_opala'),
    url(r'^smartgrid/task/(\d+)/$', 'pages.mobile.views.task', name='mobile_smartgrid_task'), 
    url(r'^events/(\w*)/$', 'pages.mobile.views.events', name='mobile_events'), 
<<<<<<< HEAD
    url(r'^smartgrid/task/(\d+)/form/$', 'pages.mobile.views.sgform', name='mobile_smartgrid_form'),
    url(r'^events/$', 'pages.mobile.views.events', name='mobile_events') 
=======
    url(r'^smartgrid/task/(\d+)/response/$', 'pages.mobile.views.sgresponse', name='mobile_smartgrid_response'),
    url(r'^events/$', 'pages.mobile.views.events', name='mobile_events'),
    url(r'^quests/(\w*)/$', 'pages.mobile.views.quests', name='mobile_quests') 
>>>>>>> 5d1f0406de5fd0079dd5c56a6a4fa9133f4eb018
)
