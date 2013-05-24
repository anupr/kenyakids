from django import forms
from django.db.models import Q
from kenyakids.web.models import Child, Sponsor,Sponsorship,Projectsponsorship
from django.utils.translation import gettext_lazy as _

__all__ = ["Childselectform", "ChildSearchForm", "SponsorSearchForm", "Bulkmailform"]

#printing child reports. First select an area and then return all children of the area
#next select the children for printing, group them by 4 and print
#return and generate the pdf for them
class Childselectform(forms.Form):
    """
    form to display a list of children with multiselect checkboxes
    """
    def __init__(self,area, *args, **kwargs):
        super(Childselectform, self).__init__(*args, **kwargs)
        self.fields['children'].choices = [(chld.id, chld.code) for chld in Child.objects.filter(area__id = area)]

    children = forms.MultipleChoiceField(choices = (), 
                                         widget = forms.CheckboxSelectMultiple)


class ChildSearchForm(forms.Form):
    """
    form to search for children
    """
    def __init__(self,user=None, qs = None, *args, **kwargs):
        super(ChildSearchForm, self).__init__(*args, **kwargs)
        self.fields['children'].queryset = qs or Child.objects.filter(area__project__in=user.project_set.all())

    children   = forms.ModelMultipleChoiceField(Child.objects.all(), 
						widget = forms.CheckboxSelectMultiple,
						required = False)
    start_code = forms.IntegerField(label = _("From"),
				    required = False)
    end_code   = forms.IntegerField(label = _("To"),
				    required = False)
    is_passive = forms.BooleanField(label = _("Passive children"),
				    required = False)
    
class SponsorSearchForm(forms.Form):
    """
    form to search for sponsors
    """
    def __init__(self, qs=None, *args, **kwargs):
        super(SponsorSearchForm, self).__init__(*args, **kwargs)
        self.fields['sponsors'].choices = qs
    sponsors = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple,required = False)
    sstr = forms.CharField(label = _("Last name contains"), required = False)

class Bulkmailform(forms.Form):
    """
    Form for the bulkmailer
    """
    def __init__(self,project,sstr, *args, **kwargs):
        super(Bulkmailform, self).__init__(*args, **kwargs)
        sponsorships_list = Sponsorship.objects.filter(child__area__project = project)
        project_sponsorships_list = Projectsponsorship.objects.filter(area__project = project)
        lst = [ii for ii in project_sponsorships_list]
        lst += [ii for ii in sponsorships_list]
        if sstr:
            lst = Sponsor.objects.filter(Q(lname__icontains = sstr) 
					 | Q(fname__icontains = sstr))
	self.fields['sponsors'].choices = [(sponsor.id,sponsor) for sponsor in lst]
    sstr = forms.CharField(label = _("Name contains the string:"),required = False)
    sponsors = forms.MultipleChoiceField(choices = (), 
					 widget = forms.CheckboxSelectMultiple,
                                         required = False)
    subject = forms.CharField(max_length = 30, label = _("Subject"), required = True)
    message = forms.CharField(label = _("Message/Mail"), widget = forms.Textarea, 
			      required = True)
    attach = forms.FileField(label = _("Attached file"),
			     required = False)
