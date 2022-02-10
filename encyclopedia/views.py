from django.shortcuts import render

from . import util

import re

from random import choice



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = markdown_2_html(util.get_entry(title))
    if entry:
        context = {"entry":entry, "title":title}
        return render(request, "encyclopedia/entry.html", context)

    else:
        return render(request, "encyclopedia/not_found.html")

def create_new_page(request):
    if request.POST:
        title = request.POST['title']
        if not util.get_entry(title):
            text = request.POST['content']
            util.save_entry(title, text)
            entry = util.get_entry(title)
            context = {"entry": entry, "title":title}
            return render(request, "encyclopedia/entry.html", context)
        else:
            context = {'title': title}
            return render(request, "encyclopedia/error.html", context)

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    entry = util.get_entry(title)
    if entry:
        context = {"entry": entry, "title":title}
        if request.POST:
            title = request.POST['title']
            if util.get_entry(title):
                text = request.POST['content']
                util.save_entry(title, text)
                entry = markdown_2_html(util.get_entry(title))
                context = {"entry": entry, "title":title}
                return render(request, "encyclopedia/entry.html", context)
        return render(request, "encyclopedia/edit_page.html", context)
    else:
        return render(request, "encyclopedia/not_found.html")


def search_entries(request):
    title = request.GET['q']
    if title != '':
        entry = markdown_2_html(util.get_entry(title))
        if entry:
            context = {"entry":entry, 'title': title}
            return render(request, "encyclopedia/entry.html", context)
        else:
            search = re.compile(r'\w*{}\w*'.format(title), re.I)
            m_entry_list = []
            entry_list = util.list_entries()
            for entry in entry_list:
                match = search.search(entry)
                if match:
                    m_entry_list.append(entry)
            if len(m_entry_list) > 0:
                return render(request, "encyclopedia/search.html", {
                "entries": m_entry_list
                })
            else:
                return render(request, 'encyclopedia/not_found.html')
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    



def rando_entry(request):
    entry_list = util.list_entries()
    title = choice(entry_list)
    entry = markdown_2_html(util.get_entry(title))
    context = {"entry":entry, 'title':title}
    return render(request, "encyclopedia/entry.html", context)

def markdown_2_html(content):
    # You need to adjust lines so that it unordered list deletions dont ruin for loop
    header = re.compile(r'#{1,6}')
    bold = re.compile(r"\_\_([^-\s].*?[^-\s])\_\_|\*{2}([^-\s].*?[^-\s])\*{2}")
    lines = content.split('\n')
    links = re.compile(r"\[(.*?)\]\((.*?)\)")
    ullists = re.compile(r"\*\s\w+")
    ulist = list()
    list_midst = False
    for l, line in enumerate(lines):
        line = bold.sub(r'<b>\1\2</b>', line)
        line = links.sub(r'<a href="\2">\1</a>', line)
        h1 = header.search(line)
        ul = ullists.search(line)
        if list_midst:
            if ul:
                ulist.append(line)
                del line
            else:
                line = mark_2_html_matcher(line, h1)
                list_midst = False
                for item in ulist:
                    kevin = f'<li>{str(item)}</li>'
                    item = f'<li>{str(item)}</li>'
                    print(kevin)
                ulist.insert(0, '<ul>')
                ulist.append('</ul>')
                ulist = ''.join(ulist)
                lines.append(ulist)
                ulist = []
        else:
            if h1:
                n = len(h1.group())
                line = header.sub('', line)
                line = f"<h{n}>"+ line + f"</h{n}>"
            else:
                if ul:
                    ulist.append(line)
                    del line
                    list_midst = True
                else:
                    line = f"<p>{line}</p>"
     
    content = ''.join(lines)
    print(ulist)
    return content

def mark_2_html_matcher(line, h1):
    header = re.compile(r'#{1,6}')
    if h1:
        n = len(h1.group())
        line = header.sub('', line)
        line = f"<h{n}>"+ line + f"</h{n}>"
        return line
    else:
        line = f"<p>{line}</p>"
        return line
# headings,* 
# boldface text, *
# unordered lists, 
# links, *
# paragraphs *