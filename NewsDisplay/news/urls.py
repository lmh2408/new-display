from django.urls import path, include
from . import views


app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('editor', views.editorLogin, name='editorLogin'),
    path('editor/logout', views.editorLogout, name='editorLogout'),
    path('editor/view', views.editorView, name='editorView'),
    path('editor/section', views.editorSection, name='editorSection'),
    path('editor/section/add', views.editorSectionAdd, name='editorSectionAdd'),
    path('editor/section/remove', views.editorSectionRemove, name='editorSectionRemove'),
    path('editor/article/add', views.editorArticleAdd, name='editorArticleAdd'),
    path('editor/article/edit', views.editorArticleEdit, name='editorArticleEdit'),
    path('editor/article/editview/<articleID>', views.editorArticleEditView, name='editorArticleEditView'),
    path('editor/front', views.editorFrontPage, name='editorFrontPage'),
    path('editor/front/remove', views.editorFrontRemove, name='editorFrontRemove'),
]
