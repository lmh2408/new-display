from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages

from .forms import *
from .models import *


# Create your views here.
def index(request):
    front = FrontPage.objects.all()[:4]
    section = Section.objects.all()

    catag = []
    for s in section:
        a = Article.objects.filter(section=s)[:3]
        if a:
            catag.append({
                'section': s,
                'article': a,
            })

    context = {
        'front': front,
        'catag': catag,
    }
    return render(request, 'news/index.html', context)


def section(request, sectionName):
    try:
        articles = Article.objects.filter(section=Section.objects.get(section=sectionName))[:10]
    except:
        return redirect(reverse('news:index'))

    context = {
        'section': sectionName,
        'articles': articles,
        'articleDisplayNumber': 10,
    }
    return render(request, 'news/section.html', context)


def article(request, articleID):
    try:
        article = Article.objects.get(id=articleID)
    except:
        return redirect(reverse('news:index'))

    return render(request, 'news/article.html', {'article': article})


@require_http_methods(["GET", "POST"])
def editorLogin(request):
    if request.user.is_authenticated:
        return redirect(reverse('news:editorView'))

    if request.method == 'POST':
        # get input
        username = request.POST['username']
        password = request.POST['password']

        # check credential
        user = authenticate(username=username, password=password, is_superuser=True)

        if user is not None:
            login(request, user)
            return redirect(reverse('news:editorView'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid login!', extra_tags='alert-danger')
            return redirect(reverse('news:editorLogin'))

    else:
        return render(request, 'editor/login.html')


def editorLogout(request):
    logout(request)
    return redirect(reverse('news:editorLogin'))


@login_required(login_url='news:editorLogin')
def editorView(request):
    return render(request, 'editor/index.html')


@require_http_methods(["GET"])
@login_required(login_url='news:editorLogin')
def editorSection(request):
    section = Section.objects.all()
    context = {
        'section': section,
    }
    return render(request, 'editor/section.html', context)


@require_http_methods(["POST"])
@login_required(login_url='news:editorLogin')
def editorSectionAdd(request):
    # get input
    sectionAdd = request.POST['sectionAdd']

    if not sectionAdd:
        messages.add_message(request, messages.ERROR, 'Invalid input', extra_tags='alert-danger')
        return redirect(reverse('news:editorSection'))

    s = Section(section=sectionAdd)
    try:
        s.save()
    except:
        messages.add_message(request, messages.ERROR, 'No duplicate allowed!', extra_tags='alert-danger')
        return redirect(reverse('news:editorSection'))

    messages.add_message(request, messages.SUCCESS, f'Added "{sectionAdd}"', extra_tags='alert-success')
    return redirect(reverse('news:editorSection'))


@require_http_methods(["POST"])
@login_required(login_url='news:editorLogin')
def editorSectionRemove(request):
    # get input
    sectionRemove = request.POST.getlist('sectionRemove[]')

    l = len(sectionRemove)
    if l == 0:
        messages.add_message(request, messages.ERROR, 'Invalid input', extra_tags='alert-danger')
        return redirect(reverse('news:editorSection'))

    for section in sectionRemove:
        Section.objects.all().filter(section=section).delete()

    messages.add_message(request, messages.WARNING, f'Deleted {l} section(s)', extra_tags='alert-warning')
    return redirect(reverse('news:editorSection'))


@require_http_methods(["GET", "POST"])
@login_required(login_url='news:editorLogin')
def editorArticleAdd(request):
    if request.method == 'POST':
        f = ArticleUpload(request.POST, request.FILES)
        if f.is_valid():
            a = Article(
                author=f.cleaned_data['author'],
                section=f.cleaned_data['section'],
                header=f.cleaned_data['header'],
                subheader=f.cleaned_data['subheader'],
                thumbnail=f.cleaned_data['thumbnail'],
                body=f.cleaned_data['body']
            )
            try:
                a.save()
            except:
                messages.add_message(request, messages.ERROR, 'Trouble saving into data table!', extra_tags='alert-danger')
                return redirect(reverse('news:editorArticleAdd'))

            messages.add_message(request, messages.SUCCESS, 'Added article into database!', extra_tags='alert-success')
            return redirect(reverse('news:editorArticleEditView', kwargs={'articleID': a.id}))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid input!', extra_tags='alert-danger')
        return redirect(reverse('news:editorArticleAdd'))
    else:
        section = Section.objects.all()
        context = {
            'section': section,
        }
        return render(request, 'editor/articleAdd.html', context)


@require_http_methods(["GET"])
@login_required(login_url='news:editorLogin')
def editorArticleEdit(request):
    article = Article.objects.all()
    return render(request, 'editor/articleEdit.html', {'article': article})


@require_http_methods(["GET","POST"])
@login_required(login_url='news:editorLogin')
def editorArticleEditView(request, articleID):
    if request.method == 'POST':
        f = ArticleEdit(request.POST, request.FILES)

        if f.is_valid():
            try:
                a = Article.objects.get(id=articleID)
            except:
                messages.add_message(request, messages.ERROR, 'Error getting id', extra_tags='alert-danger')
                return redirect(reverse('news:editorArticleEdit'))

            a.author = f.cleaned_data['author']
            a.header = f.cleaned_data['header']
            a.section = f.cleaned_data['section']
            a.subheader = f.cleaned_data['subheader']
            a.body = f.cleaned_data['body']

            if f.cleaned_data['thumbnail']:
                a.thumbnail.delete()
                a.thumbnail = f.cleaned_data['thumbnail']

            a.save()

        else:
            messages.add_message(request, messages.ERROR, 'Edit failed!', extra_tags='alert-danger')

        return redirect(reverse('news:editorArticleEditView', kwargs={'articleID':articleID}))

    else:
        try:
            article = Article.objects.get(id=articleID)
        except:
            return redirect(reverse('news:editorArticleEdit'))

        section = Section.objects.all()

        return render(request, 'editor/articleEditView.html', {'article': article, 'section': section})


@require_http_methods(["GET","POST"])
@login_required(login_url='news:editorLogin')
def editorFrontPage(request):
    if request.method == 'POST':
        f = FrontAdd(request.POST)

        if f.is_valid():
            fp = FrontPage(
                article=f.cleaned_data['article']
            )
            try:
                fp.save()
            except:
                messages.add_message(request, messages.ERROR, 'No duplicate allowed', extra_tags='alert-danger')
                return redirect(reverse('news:editorFrontPage'))

            messages.add_message(request, messages.SUCCESS, 'Article added to Front.', extra_tags='alert-success')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid input!', extra_tags='alert-danger')

        return redirect(reverse('news:editorFrontPage'))

    else:
        front = FrontPage.objects.all()
        article = Article.objects.all()
        context = {
            'front': front,
            'article': article,
        }
        return render(request, 'editor/frontEdit.html', context)


@require_http_methods(["POST"])
@login_required(login_url='news:editorLogin')
def editorFrontRemove(request):
    f = FrontRemove(request.POST)

    if f.is_valid():
        for q in f.cleaned_data['article']:
            q.delete()
        messages.add_message(request, messages.SUCCESS, 'Removed article(s) from Front.', extra_tags='alert-success')
    else:
        messages.add_message(request, messages.ERROR, 'Error removing article(s) from Front.', extra_tags='alert-danger')

    return redirect(reverse('news:editorFrontPage'))
