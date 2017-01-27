from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from MainPage.models import Document
from MainPage.forms import DocumentForm
import TextParsing

def main(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            TextParsing.parse(str = request.FILES['docfile'])
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('MainPage.views.main'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'appTemps/main.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )