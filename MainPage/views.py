from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from MainPage.models import Document
from MainPage.models import Result
from MainPage.forms import DocumentForm
import TextParsing
import Analyze

import json
import numpy as np
import matplotlib.pyplot as plt

def main(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            parser = TextParsing.TextParsing(request.FILES['docfile'].name)
            # Redirect to the document list after POST
            # return HttpResponseRedirect('MainPage.views.main')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'appTemps/main.html',
        {'documents': documents, 'form': form},
    )

def results(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            parser = TextParsing.TextParsing(request.FILES['docfile'].name)
            analyzer = Analyze.Analyze()
            score = analyzer.getAverageScores(parser)
            labels = ['compound', 'neg', 'neu', 'pos']
            ind = np.arange(4)
            width = .5
            plt.bar(ind, score, width)
            plt.ylabel('Normalized Score')
            plt.xticks(ind,labels)
            # fig, ax = plt.subplots()
            # plot = ax.bar(ind, score, width)
            plt.savefig('ConversationAnalysis/media/graph.png')
            # Redirect to the document list after POST
            # return HttpResponseRedirect('MainPage.views.main')
    else:
        form = DocumentForm() # A empty, unbound form

    return render(request, 'appTemps/results.html', {'score': score})

def tags(request):
    if request.method == 'GET':
        tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
        tag_model = Result(tags=json.dumps({'tags': tags }))
        return HttpResponse(tag_model.tags, content_type='application/json')
