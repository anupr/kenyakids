from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import datetime
from django.contrib.auth.decorators import login_required
import os, PIL, textwrap, operator
from math import ceil
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import doctemplate, Paragraph, LongTable, Spacer, Image, PageBreak
from reportlab.platypus.tables import GRID_STYLE, BOX_STYLE
from reportlab.platypus import Frame
from kenyakids.web.models import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from django.core.mail import EmailMessage
from kenyakids.web.forms import *
from django.core.urlresolvers import reverse
from django.db.models import Count, get_app, get_models, Q
from cStringIO import StringIO

try:
    import json
except ImportError:
    import simplejson as json
from django.utils.translation import ugettext_lazy as _

menu_items = [
        {"name": _("Children"), "url": "chooseproject/cs/", "id": ""},
        {"name": _("Free Children"), "url": "chooseproject/fr/", "id": ""},
        {"name": _("Areas"), "url": "areas", "id": ""},
        {"name": _("Sponsors"), "url": "chooseproject/sp/", "id": ""},
        {"name": _("Downloads"), "url": "download", "id": ""},
        {"name": _("Statistics"), "url": "chooseproject/st/", "id": ""},
        {"name": _("Mail sponsors"), "url": "chooseproject/sa/", "id": ""},
        {"name": _("Mailing List"), "url": "chooseproject/ml/", "id": ""},
        {"name": _("Translation"), "url": "translation", "id": ""},
]

def register_font(fn):
    def wrapper(request, *args, **kwargs):
        baseFontName = "LinLibertine_Re"
        pdfmetrics.registerFont(TTFont(baseFontName,
            os.path.join(settings.MEDIA_ROOT,
                "fonts/LinLibertine_Re-4.7.5.ttf")))
        style_sheet = getSampleStyleSheet()
        style_sheet["Heading1"].fontName = baseFontName
        style_sheet["Heading3"].fontName = baseFontName
        style_sheet["Title"].fontName = baseFontName
        style_sheet["Normal"].fontName = baseFontName
        kwargs['style_sheet'] = style_sheet
        return fn(request, *args, **kwargs)

    return wrapper


def index(request):
    return render_to_response("web/index.html",
        context_instance=RequestContext(request, {}))


@login_required
def areas(request):
    area_list = Area.objects.filter(iscurrent=True)
    ctx = {"area_list": area_list, "active_tab": "areas"}
    return render_to_response("web/areas.html",
        context_instance=RequestContext(request, ctx))


@login_required
def areafull(request, area_id):
    area = Area.objects.get(pk=area_id)
    ctx = {"area": area}
    return render_to_response("web/areafull.html",
        context_instance=RequestContext(request, ctx))


@login_required
def children(request):
    child_list = Child.objects.filter(iscurrent=True)
    ctx = {"child_list": child_list}
    return render_to_response("web/children.html",
        context_instance=RequestContext(request, ctx))


@login_required
def childgal(request):
    child_list = Child.objects.filter(iscurrent=True)
    ctx = {"child_list": child_list}
    return render_to_response("web/childgallery.html",
        context_instance=RequestContext(request, ctx))


@login_required
def freechildren(request, projectid):
    project = Project.objects.get(pk=projectid)
    child_list = []
    children = Child.objects.filter(area__project=project)
    for child in children:
        if child.isfree():
            child_list.append(child)
    ctx = {"child_list": child_list,
           "active_tab": 'freechildren',
           "num": len(child_list)
    }
    return render_to_response("web/freechildren.html",
        context_instance=RequestContext(request, ctx))


@login_required
def childfull(request, child_id):
    child = Child.objects.get(pk=child_id)
    child_sponsorship = Sponsorship.objects.\
    filter(child__id=child_id).filter(iscurrent=True)
    ctx = {
        "child": child,
        "child_sponsorship": child_sponsorship,
        }
    return render_to_response("web/childfull.html",
        context_instance=RequestContext(request, ctx))


@login_required
def annualreport(request, child_id):
    child = Child.objects.get(pk=child_id)
    checkup = Checkup.objects.filter(child=child_id).order_by('-chkdate')[0]
    ctx = {"child": child, "checkup": checkup}
    return render_to_response("web/annualreport.html",
        context_instance=RequestContext(request, ctx))


@login_required
def freechildfull(request, child_id):
    child = Child.objects.get(pk=child_id)
    ctx = {
        "child": child
    }
    return render_to_response("web/freechildfull.html",
        context_instance=RequestContext(request, ctx))


@login_required
def sponsors(request, projectid):
    project = Project.objects.get(pk=projectid)
    sponsorships_list = Sponsorship.objects.filter(child__area__project=project)
    project_sponsorships_list = Projectsponsorship.objects.filter(area__project=project)
    sponsors_list = [ii for ii in project_sponsorships_list]
    sponsors_list += [ii for ii in sponsorships_list]
    ctx = {"sponsor_list": sponsor_list}
    return render_to_response("web/sponsors.html",
        context_instance=Request(request, ctx))


@login_required
def sponsorfull(request, sponsor_id, projectid=None):
    sponsor = Sponsor.objects.get(pk=sponsor_id)
    sponsorship = Sponsorship.objects.filter(sponsor__id=sponsor_id)
    ctx = {
        "sponsor": sponsor,
        "sponsorship": sponsorship,
        "projectid": projectid
    }
    return render_to_response("web/sponsorfull.html",
        context_instance=RequestContext(request, ctx))


@register_font
def printstats(request, style_sheet=None):
    """
    Prints a list of sponsors and children
    """
    doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,
        'proj_stats.pdf'),
        pagesize=A4)
    normal_para = lambda x: Paragraph(unicode(x), style=style_sheet["Normal"])
    data = [map(normal_para, [_("Sponsor Number"), _("Sponsor"),
                              _("Child Number"), _("Child")])]
    sponsorships = Sponsorship.objects.filter(iscurrent=True).order_by('sponsor')
    for sponsorship in sponsorships:
        row = map(normal_para, (sponsorship.sponsor.code,
                                u"%s %s" % (sponsorship.sponsor.fname,
                                            sponsorship.sponsor.lname),
                                sponsorship.child.code,
                                sponsorship.child.name))
        data.append(row)
    table = LongTable(data, style=GRID_STYLE)
    page_flowables = [table]
    doct._doSave = 0
    doct.build(page_flowables)
    canvas = doct.canv
    canvas.setTitle(unicode(_("Statistics")))
    response = HttpResponse(canvas.getpdfdata(), mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=stats.pdf"
    return response


def child_report_data(child, style_sheet=None):
    normal_para = lambda x: Paragraph(x, style=style_sheet["Normal"])
    child_table = [
        [normal_para(_(u"Name")),
         normal_para(u"%s (%s)" % (child.name, child.code))],
        [normal_para(_(u"Sex")), normal_para(child.get_sex_display())],
        [normal_para(_(u"Date of birth")),
         normal_para(child.dob.strftime("%d-%m-%Y"))],
        [normal_para(_(u"Language")),
         normal_para(child.language.name or "-")],
        [normal_para(_(u"Religion")),
         normal_para(child.get_religion_display())],
        [normal_para(_(u"School standard")),
         normal_para(child.schoolstd.name or "-")],
        [normal_para(_(u"Fathers Name")),
         normal_para(child.fathername)],
        [normal_para(_(u"Fathers Job")),
         normal_para(unicode(child.fatherjob))],
        [normal_para(_(u"Mothers Name")),
         normal_para(child.mothername)],
        [normal_para(_(u"Mothers Job")),
         normal_para(unicode(child.motherjob))],
        [normal_para(_(u"Siblings")),
         normal_para(u", ".join([unicode(hob) for hob in\
                                 child.sibling_set.all()]))],
        [normal_para(_(u"Health")),
         normal_para("-")],
        [normal_para(_(u"Free time")),
         normal_para(u", ".join([unicode(hob.name) for hob in\
                                 child.hobbies.all() if hob.name]).capitalize())],
        [normal_para(_(u"Remarks")),
         normal_para(unicode(child.remarks or "-"))]
    ]
    checkup_exists = Checkup.objects.filter(child=child).order_by('-chkdate')
    if checkup_exists.count():
        child_table[-3][1] = normal_para(unicode(
            checkup_exists[0].get_health_display() or "-"))
    return child_table


@register_font
def childreport(request, children, style_sheet=None):
    """
    Takes a list of children and prints them out 4 at a time
    """
    doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,
        'child_report.pdf'),
        pagesize=A4)
    style = GRID_STYLE
    style.add(*('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
    style.add(*('LEFTPADDING', (0, 0), (-1, -1), 15))
    style.add(*('RIGHTPADDING', (0, 0), (-1, -1), 15))
    children = [ii for ii in children]
    num_pages = ceil(len(children) / 4.0)
    data = []
    page_flowables = []
    for ii in range(len(children)):
        data.append(child_report_data(children[ii], style_sheet=style_sheet))

    col_table = lambda x: LongTable(x, colWidths=[100, 150], style=style)
    for ii in range(int(num_pages)):
        try:
            col11 = col_table(data[4 * ii])
        except IndexError:
            col11 = Spacer(2, 2)
        try:
            col12 = col_table(data[4 * ii + 1])
        except IndexError:
            col12 = Spacer(2, 2)
        try:
            col21 = col_table(data[4 * ii + 2])
        except IndexError:
            col21 = Spacer(2, 2)
        try:
            col22 = col_table(data[4 * ii + 3])
        except IndexError:
            col22 = Spacer(2, 2)

        page_table = LongTable([
            [col11, Spacer(2, 0), col12],
            [col21, Spacer(2, 0), col22],
        ])
        page_flowables.append(page_table)

    doct._doSave = 0
    doct.build(page_flowables)
    canvas = doct.canv
    canvas.setTitle(unicode(_("Child report")))
    response = HttpResponse(canvas.getpdfdata(), mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=child_report.pdf"
    return response


@register_font
def sponsoraddress(request, sponsors, style_sheet=None):
    """
    Takes a list of sponsors and prints them out 12 at a time
    """
    doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,
        'sponsors_list.pdf'),
        pagesize=A4)
    style = GRID_STYLE
    style.add(*('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
    style.add(*('LEFTPADDING', (0, 0), (-1, -1), 15))
    style.add(*('RIGHTPADDING', (0, 0), (-1, -1), 15))
    data = []
    normal_para = lambda x: Paragraph(x, style=style_sheet["Normal"])
    sponsors = [Sponsor.objects.get(pk=ii) for ii in sponsors]
    sponsor_rows = ceil(len(sponsors) / 2.0)
    for ii in range(int(sponsor_rows)):
        try:
            col1 = normal_para("%s %s<br />%s<br />%s"
                               "<br />%s<br />%s" % (sponsors[2 * ii].fname,
                                                     sponsors[2 * ii].lname,
                                                     sponsors[2 * ii].street,
                                                     sponsors[2 * ii].postal,
                                                     sponsors[2 * ii].city,
                                                     sponsors[2 * ii].country))
            col2 = normal_para("%s %s<br />%s<br />%s"
                               "<br />%s<br />%s" % (sponsors[2 * ii + 1].fname,
                                                     sponsors[2 * ii + 1].lname,
                                                     sponsors[2 * ii + 1].street,
                                                     sponsors[2 * ii + 1].postal,
                                                     sponsors[2 * ii + 1].city,
                                                     sponsors[2 * ii + 1].country))
        except IndexError:
            continue
        data.append([col1, col2])
    sponsor_table = LongTable(data, style=style)
    page_flowables = [sponsor_table]
    doct._doSave = 0
    doct.build(page_flowables)
    canvas = doct.canv
    canvas.setTitle(unicode(_("Sponsors List")))
    response = HttpResponse(canvas.getpdfdata(), mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=sponsors_list.pdf"
    return response


def dochildsearch(request, projectid, start_code='', end_code=''):
    """
    gets a list of children and sends them to be printed in pdf
    """
    project = Project.objects.get(pk=projectid)
    if not start_code:
        try:
            start_code = Child.objects.filter(area__project=project).order_by('code')[0].code
        except:
            start_code = 0
    if not end_code:
        try:
            end_code = Child.objects.filter(area__project=project).order_by('-code')[0].code
        except:
            end_code = 0
    lst = Child.objects.filter(area__project=project).filter(code__range=(start_code, end_code))
    if request.method == 'POST':
        if request.POST.get("is_passive"):
            lst = lst.filter(iscurrent=True)
        search_form = ChildSearchForm(user=request.user, qs=lst, data=request.POST)
        if search_form.is_valid():
            if search_form.cleaned_data['start_code'] and search_form.cleaned_data[
                                                          'end_code'] and 'search' in request.POST.keys():
                return HttpResponseRedirect(reverse("childsearch",
                    kwargs={"start_code": search_form.cleaned_data["start_code"],
                            "end_code": search_form.cleaned_data["end_code"],
                            "projectid": projectid}))
            if 'child_report' in request.POST.keys():
                return childreport(request, search_form.cleaned_data['children'])

            if 'annual_report' in request.POST.keys():
                return printannualreportnew(request, projectid, search_form.cleaned_data['children'])
            if 'child_story' in request.POST.keys():
                return printchildstory(request, search_form.cleaned_data['children'])

    search_form = ChildSearchForm(user=request.user, qs=lst)
    empty = 1
    c = {"search_form": search_form,
         'start_code': start_code,
         'end_code': end_code,
         'active_tab': 'childsearch',
         'project': project
    }
    return render_to_response("web/childsearch.html",
        context_instance=RequestContext(request, c))


@login_required
def childsearch(request, projectid, start_code='', end_code=''):
    project = Project.objects.get(pk=projectid)
    countchildren = Child.objects.filter(area__project=project).count()
    if countchildren:
        return dochildsearch(request, projectid, start_code=start_code, end_code=end_code)
    nochildren = True
    c = {
        'nochildren': nochildren,
        'active_tab': 'childsearch',
        'project': project,
        }
    return render_to_response("web/childsearch.html",
        context_instance=RequestContext(request, c))


@login_required
def chooseproject(request, origin):
    """gets the list of projects for which the user has permissions"""
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = request.user.project_set.all()
    c = {'projects': projects,
         'origin': origin}
    return render_to_response("web/chooseproject.html",
        context_instance=RequestContext(request, c))


@login_required
def sponsorsearch(request, projectid, sstr=''):
    """
    gets a list of sponsors
    """
    project = Project.objects.get(pk=projectid)
    sponsorships_list = Sponsorship.objects.filter(child__area__project=project)
    project_sponsorships_list = Projectsponsorship.objects.filter(area__project=project)
    lst = [(ii.sponsor.id, ii.sponsor) for ii in project_sponsorships_list]
    lst += [(ii.sponsor.id, ii.sponsor) for ii in sponsorships_list]
    reslist = []
    if request.method == 'POST':
        search_form = SponsorSearchForm(qs=lst, data=request.POST)
        if search_form.is_valid():
            if search_form.cleaned_data['sstr']  and 'search' in request.POST.keys():
                sstr = search_form.cleaned_data['sstr']
                return HttpResponseRedirect(reverse("sponsorsearch", kwargs={"projectid": projectid, "sstr": sstr}))
            if 'print' in request.POST.keys():
                return sponsoraddress(request, search_form.cleaned_data['sponsors'])
    else:
        if sstr:
            for item in lst:
                try:
                    if item[1].lname.lower().rfind(sstr.lower()) != -1:
                        reslist.append(item)
                except:
                    pass
            search_form = SponsorSearchForm(qs=reslist)
        else:
            search_form = SponsorSearchForm(qs=lst)
    c = {"search_form": search_form,
         'last': sstr,
         'active_tab': 'sponsorsearch',
         "projectid": projectid,
         'project': project
    }
    return render_to_response("web/sponsorsearch.html",
        context_instance=RequestContext(request, c))


@login_required
def download(request):
    """ View for downloads """
    download_list = Download.objects.all()
    ctx = {"download_list": download_list, 'active_tab': 'download'}
    return render_to_response("web/down.html",
        context_instance=RequestContext(request, ctx))


@register_font
def printannualreport(request, children, style_sheet=None):
    """
    prints annual report of the selected children
    """
    doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,
        'annual_report.pdf'),
        pagesize=A4)
    style = GRID_STYLE
    style.add(*('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
    style.add(*('LEFTPADDING', (0, 0), (-1, -1), 15))
    style.add(*('RIGHTPADDING', (0, 0), (-1, -1), 15))

    img = Image(os.path.join(settings.MEDIA_ROOT, "pics/fidalogo.jpg"),
        width=100, height=60)
    page_title = Paragraph(_(u"Annual Sponsorship child report"),
        style=style_sheet["Heading1"])
    project_name = Paragraph(_(unicode(settings.PROJECT_NAME)),
        style=style_sheet["Heading3"])
    normal_para = lambda x: Paragraph(unicode(x), style=style_sheet["Normal"])
    child_data_heading = Paragraph(_(u"General information about the child"),
        style=style_sheet["Heading3"])
    child_health_heading = Paragraph(_(u"Information about the child's health"),
        style=style_sheet["Heading3"])

    children_row = []
    children_health_row = []
    for child in children:
        child_row = []
        health_row = []
        child_row.append((normal_para(_(u"Name")), normal_para(child.name)))
        child_row.append((normal_para(_(u"Child number")), normal_para(child.code)))
        child_row.append((normal_para(_(u"Village area")), normal_para(child.area)))
        child_row.append((normal_para(_(u"Sex")), normal_para(child.get_sex_display())))
        child_row.append((normal_para(_(u"Date of birth")),
                          normal_para(child.dob.strftime("%d-%m-%Y"))))
        child_row.append((normal_para(_(u"Language")),
                          normal_para(child.language.name or "-")))
        child_row.append((normal_para(_(u"Religion")),
                          normal_para(child.get_religion_display())))
        child_row.append((normal_para(_(u"Character")),
                          normal_para(_(u", ".join([unicode(hob.name) for hob in child.character.all() if hob.name])))))
        child_row.append((normal_para(_(u"School standard")),
                          normal_para(child.schoolstd.name or "-")))
        child_row.append((normal_para(_(u"School performance")),
                          normal_para(child.get_schoolperf_display())))
        child_row.append((normal_para(_(u"Free time")),
                          normal_para(
                              u", ".join([unicode(hob.name) for hob in child.hobbies.all() if hob.name]).capitalize())))

        checkup_exists = Checkup.objects.filter(child=child.id).order_by('-chkdate')
        checkup_child = None
        if checkup_exists.count():
            checkup_child = checkup_exists[0]
        health_row.append([normal_para(_(u"Health")), normal_para("-")])
        health_row.append([normal_para(_(u"Height")), normal_para("-")])
        health_row.append([normal_para(_(u"Weight")), normal_para("-")])
        health_row.append([normal_para(_(u"Long term diagnosis")), normal_para("-")])
        health_row.append([normal_para(_(u"Medical remarks")), normal_para("-")])
        if checkup_child:
            health_row[-5][1] = normal_para(checkup_child.get_health_display())
            health_row[-4][1] = normal_para(checkup_child.height)
            health_row[-3][1] = normal_para(checkup_child.weight)
            health_row[-2][1] = normal_para(
                u",".join([unicode(rem.name) for rem in checkup_child.ltdiag.all() if rem.name]))
            health_row[-1][1] = normal_para(u",".join([unicode(rem.name) for rem in checkup_child.medrem.all()]))
        health_row.append([normal_para(_(u"Remarks")),
                           normal_para(child.remarks)])
        health_row.append([normal_para(_(u"Date")),
                           normal_para(datetime.now().strftime("%d-%m-%Y"))])

        children_row.append(child_row)
        children_health_row.append(health_row)

    page_flowables = []
    for ii in range(len(children_row)):
        child_data_table = LongTable(children_row[ii], style=style)
        child_health_table = LongTable(children_health_row[ii], style=style)
        page_flowables.extend([header_img, page_title, project_name,
                               child_data_heading, child_data_table,
                               child_health_heading, child_health_table,
                               PageBreak(), ])
    doct._doSave = 0
    doct.build(page_flowables)
    canvas = doct.canv
    canvas.setTitle(unicode(_("Annual Sponsorship child report")))
    response = HttpResponse(canvas.getpdfdata(), mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=annual_report.pdf"
    return response


@register_font
def printannualreportnew(request, projectid, children, style_sheet=None):
    """
    prints annual report of the selected children
    """
    project = Project.objects.get(pk=projectid)
    doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,'annual_report.pdf',),
        pagesize=A4,
        leftMargin = 5,
        rightMargin = 5,
        topMargin = 5,
        bottomMargin = 5,
    )
    style = GRID_STYLE
    style.add(*('VALIGN', (0, 0), (-1, -1), 'TOP'))
    style.add(*('LEFTPADDING', (0, 0), (-1, -1), 5))
    style.add(*('RIGHTPADDING', (0, 0), (-1, -1), 5))
    style1 = BOX_STYLE
    style1.add(*('VALIGN', (0, 0), (1, 1), 'TOP'))
    style1.add(*('ALIGN', (0, 1), (1, 1), 'RIGHT'))
    headimg = PIL.Image.open(os.path.join(settings.MEDIA_ROOT, "pics/fidalogo.jpg"))
    headimg.thumbnail((120, 120), PIL.Image.ANTIALIAS)
    headimg.save(os.path.join(settings.MEDIA_ROOT, "fidalogo.tn"), "JPEG")
    header_img = Image(os.path.join(settings.MEDIA_ROOT, "fidalogo.tn"))
    page_title = Paragraph(_(u"Sponsored child report"),
        style=style_sheet["Heading3"])
    project_name = Paragraph((project.name),
        style=style_sheet["Heading3"])
    normal_para = lambda x: Paragraph(unicode(x), style=style_sheet["Normal"])
    child_data_heading = Paragraph(_(u"General information about the child"),
        style=style_sheet["Heading3"])
    child_story_heading = Paragraph(_(u"Child story"),
        style=style_sheet["Heading3"])
    date_printed = Paragraph(_(u"Dated %s" % datetime.today().strftime("%d-%m-%Y")),
        style=style_sheet["Heading3"])

    children_row = []
    for child in children:
        try:
            childimg = PIL.Image.open(os.path.join(settings.MEDIA_ROOT, str(child.picture)))
            childimg.thumbnail((300, 300), PIL.Image.ANTIALIAS)
            childimg.save(os.path.join(settings.MEDIA_ROOT, str(child.picture)+".tn"), "JPEG")
            img = Image(os.path.join(settings.MEDIA_ROOT,str(child.picture)+".tn"))
        except:
            img = None

        child_row = []
        child_row.append((normal_para(_(u"Name")), normal_para(child)))
        child_row.append((normal_para(_(u"Village area")), normal_para(child.area)))
        child_row.append((normal_para(_(u"Sex")), normal_para(child.get_sex_display())))
        child_row.append((normal_para(_(u"Date of birth")),
                          normal_para(child.dob.strftime("%d-%m-%Y"))))
        child_row.append((normal_para(_(u"Language")),
                          normal_para(child.language.name or "-")))
        child_row.append((normal_para(_(u"Religion")),
                          normal_para(child.get_religion_display())))
        child_row.append((normal_para(_(u"Character")),
                          normal_para(_(u", ".join([unicode(hob.name) for hob in child.character.all() if hob.name])))))
        child_row.append((normal_para(_(u"School standard")),
                          normal_para(child.schoolstd.name or "-")))
        child_row.append((normal_para(_(u"School performance")),
                          normal_para(child.get_schoolperf_display())))
        child_row.append((normal_para(_(u"Free time")),
                          normal_para(
                              u", ".join([unicode(hob.name) for hob in child.hobbies.all() if hob.name]).capitalize())))

        child_row.append((normal_para(_(u"Male guardian type")),
                          normal_para(child.get_maleguardiantype_display() or "-")))
        child_row.append((normal_para(_(u"Male guardian name")),
                          normal_para(child.fathername or "-")))
        child_row.append((normal_para(_(u"Male guardian job")),
                          normal_para(child.fatherjob or "-")))
        child_row.append((normal_para(_(u"Female guardian type")),
                          normal_para(child.get_femaleguardiantype_display() or "-")))
        child_row.append((normal_para(_(u"Female guardian name")),
                          normal_para(child.mothername or "-")))
        child_row.append((normal_para(_(u"Female guardian job")),
                          normal_para(child.motherjob or "-")))
        if child.sibling_set.all().count() > 0:
            child_row.append((normal_para(_(u"Siblings")),
                              normal_para(_(u", ".join([unicode(hob) for hob in child.sibling_set.all()])))))
        child_row.append((normal_para(_(u"Remarks")),
                          normal_para(child.remarks or "-")))
        try:
            child_story = ChildStory.objects.get(child=child)
        except ChildStory.DoesNotExist:
            child_story = None
        story_content = child_story.story or '-'
        c_st = normal_para((story_content))
        #if story_content:
        #    story_content = story_content.replace('</p>', '</p><br /><br />',
        #        story_content.count('</p>') - 1)

        children_row.append((child_row, img, c_st))

    page_flowables = []
    for ii in range(len(children_row)):
        head_row = []
        head_row.append((header_img, children_row[ii][1]))
        head_row.append((page_title, project_name))
        head_data_table = LongTable(head_row, style=style1)
        child_data_table = LongTable(children_row[ii][0],colWidths=(150,422), style=style)
        page_flowables.extend([head_data_table])
        page_flowables.extend([child_data_table,
                               child_story_heading,
                               children_row[ii][2],
                               date_printed,
                               PageBreak(), ])

    doct._doSave = 0
    doct.build(page_flowables)

    canvas = doct.canv
    canvas.setTitle(unicode(_("Annual Sponsorship child report")))
    response = HttpResponse(canvas.getpdfdata(), mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=annual_report.pdf"
    return response


@register_font
def printchildstory(request, children, style_sheet=None):
    doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,
        'child_story.pdf'),
        pagesize=landscape(A4))
    data = []
    row = []
    for child in children:
        try:
            child_story = ChildStory.objects.get(child=child)
        except ChildStory.DoesNotExist:
            child_story = None
        story_content = child_story and child_story.story or '-'
        if story_content:
            story_content = story_content.replace('</p>', '</p><br /><br />',
                story_content.count('</p>') - 1)
        row.append((Paragraph(unicode(child_story or '-'), style=style_sheet["Title"]),
                    Paragraph(story_content, style=style_sheet["Normal"])))
        if len(row) == 2:
            data.append(row)
            row = []
    if row:
        data.append(row)
    style = GRID_STYLE
    style.add(*('VALIGN', (0, 0), (-1, -1), 'MIDDLE'))
    style.add(*('LEFTPADDING', (0, 0), (-1, -1), 15))
    style.add(*('RIGHTPADDING', (0, 0), (-1, -1), 15))
    table = LongTable(data, colWidths=360, rowHeights=215, style=style)
    page_flowables = [table]
    doct._doSave = 0
    doct.build(page_flowables)
    canvas = doct.canv
    canvas.setTitle(unicode(_("Child Stories")))
    response = HttpResponse(canvas.getpdfdata(), mimetype="application/pdf")
    response["Content-Disposition"] = "attachment; filename=child_story.pdf"
    return response


@login_required
def statistics(request, projectid):
    project = Project.objects.get(pk=projectid)
    children_by_area = Child.objects.filter(area__project=project).order_by('area').values('area',
        'area__name').\
    annotate(num_per_area=Count('area'))
    #num_sponsors = Sponsor.objects.filter(iscurrent=True).count()
    num_sponsorships = Sponsorship.objects.filter(child__area__project=project).filter(iscurrent=True).count()
    num_project_sponsors = Projectsponsorship.objects.filter(area__project=project).count()
    num_children = Child.objects.filter(area__project=project).filter(iscurrent=True).count()
    num_girls = Child.objects.filter(area__project=project).filter(sex='F', iscurrent=True).count()
    num_boys = num_children - num_girls

    for ps in Projectsponsorship.objects.all():
        num_sponsorships += (ps.children or 0)
        #num_free_children = Child.objects.filter(area__project=project).extra(
        #where=["""id not in(select child_id from web_sponsorship """
        #"""where web_sponsorship.iscurrent=True)"""]
        #).filter(iscurrent=True).count()
    ctx = {
        #'num_sponsors': num_sponsors,
        'num_sponsorships': num_sponsorships,
        'num_project_sponsors': num_project_sponsors,
        'num_children': num_children,
        #'num_free_children': num_free_children,
        'num_boys': num_boys,
        'num_girls': num_girls,
        'children_by_area': children_by_area,
        'active_tab': 'statistics',
        'project': project,
        }
    return render_to_response("web/statistics.html",
        context_instance=RequestContext(request, ctx))


@login_required
def bulkmail(request, projectid, sstr=''):
    """
    Bulkmailer for committee members
    """
    project = Project.objects.get(pk=projectid)
    form = Bulkmailform(project, sstr)
    if request.POST:
        form = Bulkmailform(project, sstr, request.POST)
        if 'search' in request.POST.keys():
            sstr = request.POST['sstr']
            return HttpResponseRedirect("/bulkmail/%d/%s/" % (int(projectid), sstr))
        if form.is_valid():
            fm = form.cleaned_data
            subject = fm['subject']
            message = fm['message']
            frm = settings.DEFAULT_FROM_EMAIL
            lst = []
            emaillist = []
            if 'sel' in request.POST.keys():
                for sp in fm['sponsors']:
                    emaillist.append(Sponsor.objects.get(pk=int(sp)))
            tmpl = loader.get_template('web/mail.txt')
            for user in emaillist:
                mail_ctx = RequestContext(request, {
                    'sponsor': user,
                    'msg': message
                })
                mail_msg = tmpl.render(mail_ctx)
                emailmsg = EmailMessage(subject, mail_msg, frm, [user.email])
                if request.FILES:
                    flname = request.FILES['attach'].name
                    cnt = request.FILES['attach'].read()
                    emailmsg.attach(flname, cnt)
                emailmsg.send()
            return HttpResponseRedirect("%s?status=success"
            % reverse("bulkmail"))
    ctx = {
        'form': form,
        'project': project,
        'active_tab': 'bulkmail'
    }
    if request.GET.get("status") == "success":
        ctx.update({"success": True})
    return render_to_response("web/bulkmail.html",
        context_instance=RequestContext(request, ctx))


@login_required
@register_font
def mailinglist(request, projectid, style_sheet=None):
    project = Project.objects.get(pk=projectid)
    sponsorships_list = Sponsorship.objects.filter(child__area__project=project)
    project_sponsorships_list = Projectsponsorship.objects.filter(area__project=project)
    sponsors_list = [ii for ii in project_sponsorships_list]
    sponsors_list += [ii for ii in sponsorships_list]

    if request.POST:
        ordering_field = request.POST.get("ordering_field").strip()
        if ordering_field:
            ordering_map = {u"Id": u"_temp_id", u"FirstName": u"sponsor.fname",
                            u"Surname": u"sponsor.lname",
                            u"Sponsorships": u"", u"From": u"startdate",
                            u"Country": u"sponsor.country",
                            u"Address": u"sponsor.code", u"Remarks": u"remarks"}
            for idx, ii in enumerate(sponsors_list):
                ii._temp_id = idx
            order = request.POST.get("ordering")
            reverse = False
            if order == u"desc":
                reverse = True
            if ordering_map.get(ordering_field):
                attr = operator.attrgetter(ordering_map.get(ordering_field))
                sponsors_list.sort(key=attr, reverse=reverse)
        doct = doctemplate.SimpleDocTemplate(os.path.join(settings.TMP_DIR,
            'mailing_list.pdf'),
            pagesize=landscape(A4))
        header = Paragraph(unicode(_("List of sponsors")),
            style_sheet["Title"])
        spacer = Spacer(10, 10)
        data = [map(unicode, [_(u"First Name"), _(u"Last Name"),
                              _(u"Sponsorships"), _(u"From"),
                              _(u"Country"), _(u"Address"),
                              _(u"Remarks")])]

        def fit_into_paragraph(ustr):
            return Paragraph(u"\n".join(textwrap.wrap(ustr, 18)),
                style_sheet["Normal"])

        for ii in sponsors_list:
            if isinstance(ii, Projectsponsorship):
                child_details = u"%s: %s %s" % (ii.area.code,
                                                ii.children or 0,
                                                _("children"))
            else:
                child_details = u"%s: %s" % (ii.child.code,
                                             ii.child.name)
            data.append((
                fit_into_paragraph(ii.sponsor.fname),
                fit_into_paragraph(ii.sponsor.lname),
                fit_into_paragraph(child_details),
                fit_into_paragraph(ii.startdate.strftime("%d-%m-%Y")),
                fit_into_paragraph(ii.sponsor.country),
                fit_into_paragraph(u"%s: %s\n%s\n%s - "
                                   "%s\n%s\n%s\n%s" % (_("Code"),
                                                       ii.sponsor.code,
                                                       ii.sponsor.street,
                                                       ii.sponsor.city,
                                                       ii.sponsor.postal,
                                                       ii.sponsor.country,
                                                       ii.sponsor.phone,
                                                       ii.sponsor.email)),
                fit_into_paragraph(ii.remarks or '-')))
        table = LongTable(data, style=GRID_STYLE)
        page_flowables = [header, spacer, table]
        doct._doSave = 0
        doct.build(page_flowables)
        canvas = doct.canv
        canvas.setTitle(unicode(_("%s Sponsor List" % settings.SHORT_PROJECT_NAME)))
        response = HttpResponse(canvas.getpdfdata(),
            mimetype="application/pdf")
        response["Content-Disposition"] = 'attachment;filename=mailing_list.pdf'
        return response
    total_sponsor_count = range(1, project_sponsorships_list.count()\
                                   + sponsorships_list.count() + 1)
    total_sponsor_count.reverse()
    ctx = {
        'sponsor_id': total_sponsor_count,
        'project_sponsorships_list': project_sponsorships_list,
        'sponsorships_list': sponsorships_list,
        'active_tab': 'mailinglist',
        'project': project
    }
    return render_to_response("web/mailinglist.html",
        context_instance=RequestContext(request, ctx))


@login_required
def trans_page(request):
    return render_to_response("web/translation_choice.html",
        context_instance=RequestContext(request, {}))


def gen_trans_db_strings_list(curr_lang_code):
    default_lang_code = "en"
    app = get_app("web")
    models = get_models(app)
    trans_models = filter(lambda x: getattr(x._meta,
        "translatable_fields",
        None), models)
    untrans_summary = []
    for model_class in trans_models:
        trans_fields = model_class._meta.translatable_fields
        for field in trans_fields:
            trans = model_class.objects.filter(\
                Q(**{"%s_%s" % (field,
                                curr_lang_code): ""}) |\
                Q(**{"%s_%s__isnull" % (field,
                                        curr_lang_code):
                         True}))
            if not trans.count():
                continue
            for model_inst in trans:
                model_inst.admin_change_url = reverse("admin:%s_%s_change" % (model_inst._meta.app_label,
                                                                              model_inst._meta.module_name),
                    args=(model_inst.pk,))
                untrans_summary.append((field, model_inst))
    return untrans_summary


@login_required
def trans_db_strings(request):
    curr_lang_code = request.LANGUAGE_CODE
    untrans_summary = gen_trans_db_strings_list(curr_lang_code)
    context = {"untrans_summary": untrans_summary}
    return render_to_response("web/trans_db_strings.html",
        context_instance=RequestContext(request,
            context))

#csv conversion

def convertfromcsv(filename):
    fle = open(filename, 'r')
    for line in fle.readlines():
        parse = line.split('|')
        if not Sponsor.objects.filter(code=int(parse[6])).count() > 0:
            pc = parse[4].split()
            Sponsor.objects.create(lname=parse[0],
                fname=parse[1],
                addnames=parse[2],
                street=parse[3],
                postal=pc[0],
                city=pc[1],
                country=parse[5],
                code=int(parse[6]),
                email=parse[7],
            )
    return 1
