from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from wiki.models import Wiki, Document

import simplejson as json

import os

def home(request):
    wikis = Wiki.objects.all()

    data = {
        u'wikis': [wikis[x:x+3] for x in xrange(0, len(wikis), 3)]
    }

    return render_to_response(u'home.html', data, context_instance=RequestContext(request))

def _postdoc(request, is_image):
    docpath = u'{0}/{1}'.format(
            settings.MEDIA_ROOT,
            is_image and u'images' or u'documents'
    )

    if not os.path.exists(docpath):
        os.mkdir(docpath)

    f = request.FILES[u'file']

    fd = open(u'{0}/{1}'.format(docpath, f.name), u'wb+')
    for chunk in f.chunks():
        fd.write(chunk)
    fd.close()

    url = u'{0}/{1}/{2}'.format(
            settings.MEDIA_URL,
            is_image and u'images' or u'documents',
            f.name
    )

    try:
        doc = Document.objects.get(path=url)
    except Document.DoesNotExist:
        doc = Document()

        doc.is_image = is_image
        doc.path = url

        doc.wikipath = request.POST[u'page']
        doc.save()

    return HttpResponse(doc.path)

@login_required
def post_img(request):
    if request.method == u'POST':
        return _postdoc(request, True)

@login_required
def post_doc(request):
    if request.method == u'POST':
        return _postdoc(request, False)
