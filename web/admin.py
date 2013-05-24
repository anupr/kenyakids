from django.contrib import admin
from kenyakids.web.models import *
from kenyakids.web.forms import *
from django import forms

class Projectadmin(admin.ModelAdmin):
    def queryset(self, request):
        # Show only projects created by the user in the admin
        qs = super(Projectadmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return request.user.project_set.all()
    filter_horizontal = ('admins',)

class AreaAdmin(admin.ModelAdmin):
    def queryset(self, request):
        # Show only projects created by the user in the admin
        qs = super(AreaAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return Area.objects.filter(project__in=request.user.project_set.all())
    list_display = ("name","project", "code",)
    search_fields = ["code"]

    class Media:
        js = ("/sitemedia/js/jquery.js",
              "/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
              "/sitemedia/js/admin_textarea.js")

class SponsorAdmin(admin.ModelAdmin):
    list_display = ("code", "lname", "fname","addnames", "iscurrent")
    search_fields = ["code", "lname"]
    list_filter = ('iscurrent',) 
    
class ChildStoryAdmin(admin.TabularInline):
    model = ChildStory
    max_num = 1
    
    class Media:
            js = ("/sitemedia/js/jquery.js",
                  "/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
                  "/sitemedia/js/admin_textarea.js")
class CheckupAdmin(admin.TabularInline):
    model = Checkup
    max_num = 1
    filter_horizontal = ('ltdiag','medrem')
    
class Siblinginline(admin.TabularInline):
    model = Sibling

class ChildAdmin(admin.ModelAdmin):
    def has_change_permission(self, request,obj=None):
        # obj is the child and we fetch the project associated with the child through
        # the area.
        if request.user.is_superuser:
            return True
        if obj == None:
            return True
        if request.user.project_set.filter(name=obj.area.project.name).count():
            return True
        return False
    def has_delete_permission(self, request, obj=None):
        # Same as change permission
        if request.user.is_superuser:
            return True
        if obj == None:
            return True
        if request.user.project_set.filter(name=obj.area.project.name).count():
            return True
        return False

    def queryset(self, request):
        # Show only projects created by the user in the admin
        qs = super(ChildAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return Child.objects.filter(area__project__in=request.user.project_set.all())
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            if request.user.is_superuser:
                kwargs["queryset"] = Area.objects.all()
            else:
                kwargs["queryset"] = Area.objects.filter(project__in=request.user.project_set.all())
        return super(ChildAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            
    list_display = ("code", "name", "fatherjob", "motherjob",
                    "iscurrent")
    search_fields = ["code", "name"]
    list_filter = ('iscurrent','area__project')
    filter_horizontal = ('hobbies','character')
    inlines = [Siblinginline,ChildStoryAdmin,CheckupAdmin]
    
    class Media:
            js = ("/sitemedia/js/jquery.js",
                  "/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
                  "/sitemedia/js/admin_textarea.js")



class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ("sponsor", "child", "iscurrent")
    search_fields = ["sponsor__code", "child__code"]
    list_filter = ('iscurrent',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "child":
            kwargs["queryset"] = Child.objects.filter(area__project__in=request.user.project_set.all())
        return super(SponsorshipAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ("/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
              "/sitemedia/js/admin_textarea.js")

class ProjectsponsorshipAdmin(admin.ModelAdmin):
    list_display = ("sponsor", "area","iscurrent")
    search_fields = ["sponsor__code",]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "area":
            kwargs["queryset"] = Area.objects.filter(project__in=request.user.project_set.all())
        return super(ProjectsponsorshipAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ("/sitemedia/js/jquery.js",
              "/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
              "/sitemedia/js/admin_textarea.js")



class ChildnoteAdmin(admin.ModelAdmin):
    list_display = ("notedate", "child")
    search_fields = ["notedate", "child"]

class SponsornoteAdmin(admin.ModelAdmin):
    list_display = ("notedate", "sponsor",)
    search_fields = ["notedate", "sponsor"]

    class Media:
        js = ("/sitemedia/js/jquery.js",
              "/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
              "/sitemedia/js/admin_textarea.js")

class AreanoteAdmin(admin.ModelAdmin):
    list_display = ("notedate", "area",)
    search_fields = ["notedate", "area"]

    class Media:
        js = ("/sitemedia/js/jquery.js",
              "/sitemedia/js/wymeditor/jquery.wymeditor.min.js",
              "/sitemedia/js/admin_textarea.js")

class DownloadAdmin(admin.ModelAdmin):
        list_display = ("name",)
        search_fields = ["name"]

admin.site.register(Schoolstandard)
admin.site.register(Doctor)
admin.site.register(Hobby)
admin.site.register(Character)
admin.site.register(Job)
admin.site.register(Language)
admin.site.register(Project,Projectadmin)
admin.site.register(Longtermdiagnosis)
admin.site.register(Medicalremarks)
admin.site.register(Area, AreaAdmin)
admin.site.register(Areanote, AreanoteAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Childnote, ChildnoteAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Sponsornote, SponsornoteAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(Projectsponsorship, ProjectsponsorshipAdmin)
