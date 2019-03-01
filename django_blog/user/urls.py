from django.urls import path,re_path
from . import views

app_name='user'
urlpatterns = [
    path('',views.indexView,name='IndexList'),
    path('add_user/',views.AddUserView.as_view(),name='AddUser'),
    path('add_manager/',views.AddManagerView.as_view(),name='AddManager'),
    path('del_user/',views.DelUserView.as_view(),name='DelUser'),
    path('delted_user/',views.DeltedUserView.as_view(),name='DeltedUser'),
    path('edit_user/',views.EditUserView.as_view(),name='EditUser'),
    path('get_city/',views.getCity,name='GetCity'),
    path('get_country/',views.getCountoy,name='GetCountry'),
    path('detail_user/',views.detailUser,name='DetailUser'),
    path('edit_pwd/',views.EditPwd.as_view(),name='EditPwd'),
    path('avatar_user/',views.AvatarUser.as_view(),name='AvatarUser'),
    path('send_email/',views.SendEmal.as_view(),name='SendEmail'),
    re_path('active/(?P<active_code>.*)/', views.changePwd, name='active'),
    path('modiffed/',views.modiffed,name='Modiffed'),
    path('managers/',views.managers,name='Manager'),
    path('edit_manager/',views.EditManager.as_view(),name='EditManager'),
    path('repwd_manager/',views.RepwdManager.as_view(),name='RepwdManager'),
    path('del_manager/',views.delManager,name='DelManager')
]