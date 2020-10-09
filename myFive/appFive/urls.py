from django.conf.urls import url
from appFive import views

# Template URl, need to set up the app name

app_name='appFive'

urlpatterns =[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),

]
