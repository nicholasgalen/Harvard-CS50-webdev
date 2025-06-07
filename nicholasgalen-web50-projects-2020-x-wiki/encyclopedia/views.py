import random
from django.shortcuts import render, redirect
from django.http import Http404
from encyclopedia import util
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page '{title}' not found"
        }, status=404)
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    entries_lower = [entry.lower() for entry in entries]
    
    if query.lower() in entries_lower:
        return redirect("entry", title=entries[entries_lower.index(query.lower())])
    
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()
        entries_lower = [entry.lower() for entry in entries]
        
        if title.strip().lower() in entries_lower:
            return render(request, "encyclopedia/new.html", {
                "error": "Page already exists",
                "title": title,
                "content": content
            })
        
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page '{title}' not found"
        }, status=404)
        
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry", title=title)