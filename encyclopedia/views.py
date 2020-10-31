from django import forms
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown
# import mistletoe
# from mistletoe.latex_renderer import LaTeXRenderer

import numpy as np

from . import util


class SearchSite(forms.Form):
    query = forms.CharField(label="",
     help_text="Search for any article located on the site.")
   

class NewPage(forms.Form):
    text_area = forms.CharField(label="", 
    help_text="Create your own Markdown Document.",
    widget=forms.Textarea)
    document_title = forms.CharField(label="Document Title")


def index(request):
    
    context = {
        "entries": util.list_entries(),
        'search_bar_form': SearchSite()
    }

    return render(request, "encyclopedia/index.html", context)


def page(request, page_title):

    md = markdown.Markdown()
    # Use util function to read markdown file
    markdown_contents = util.get_entry(page_title)
    # Convert markdown string into html
    
    if markdown_contents is not None:
        page_contents = md.convert(markdown_contents)
        # with open("entries/Python.md", 'r') as fin:
        #     rendered = mistletoe.markdown(fin, LaTeXRenderer)
        #     print(rendered)
    else:
        page_contents = '<h1>Page not found</h1>'

    context = {'page_title': page_title,
                'search_bar_form': SearchSite(),
                'entry_content': page_contents
    }

    response = render(request, "encyclopedia/page_template.html", context)
    return response


def createpage(request):

    empty_form = NewPage()

    if request.method == "POST":
        filled_form = NewPage(request.POST)
        if filled_form.is_valid():
            file_exists_already = filled_form.cleaned_data["document_title"] in util.list_entries()    
            if not file_exists_already:
                document_title = filled_form.cleaned_data["document_title"]
                markdown_contents = filled_form.cleaned_data["text_area"]
                util.save_entry(document_title, markdown_contents)
                return HttpResponseRedirect(reverse("wiki", 
                kwargs={"page_title": document_title}))

    have_to_resend_form = request.method != "POST" or not filled_form.is_valid()

    if have_to_resend_form:
        context = {"create_page_form": empty_form,
        'search_bar_form': SearchSite()
    }
    else:
        context = {"create_page_form": filled_form,
            'search_bar_form': SearchSite()
        }

    response = render(request, "encyclopedia/createpage.html", context)
    
    return response


def randompage(request):
    entries = util.list_entries()
    num_entries = entries.__len__()
    rand_index = np.random.randint(0, num_entries - 1)
    random_entry = entries[rand_index]

    return HttpResponseRedirect(reverse("wiki", 
    kwargs={"page_title": random_entry}))


def search(request):

    form = SearchSite()
    is_substring_of_queries = []
        
    if request.method == "GET":
        form = SearchSite(request.GET)
        
        if form.is_valid():
            for entry in util.list_entries():
                existsIdenticalResult = form.cleaned_data["query"].casefold() == entry.casefold() 
                existsResult = form.cleaned_data["query"].casefold() in entry.casefold()    
                if existsIdenticalResult:
                    return HttpResponseRedirect(reverse("wiki",
                     kwargs={"page_title": entry}))
                elif existsResult: 
                    is_substring_of_queries.append(entry)
        
    context = {
        "search_bar_form": SearchSite(),
        "is_substring_of_queries": is_substring_of_queries
    }

    response = render(request, "encyclopedia/search.html", context)
    return response

