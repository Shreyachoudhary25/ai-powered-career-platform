from django.urls import path
from .views import login_view, signup_view, logout_view
from .views import mentor_list, send_mentorship_request
from .views import mentor_requests, update_mentorship_status


urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),

    path('mentors/', mentor_list, name='mentor_list'),
    path('mentors/<int:mentor_id>/request/', send_mentorship_request, name='send_mentorship_request'),
    path('mentor/requests/', mentor_requests, name='mentor_requests'),
    path('mentor/requests/<int:request_id>/update/', update_mentorship_status, name='update_mentorship_status'),

]
