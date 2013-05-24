from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from transmeta import TransMeta
from django.core.exceptions import ValidationError
from datetime import datetime

RELIGION_CHOICES = (
    (u'Chr',_(u"Christian")),
    (u'Mus',_(u"Muslim")),
    (u'Hin',_(u"Hindu")),
    (u'Bud',_(u"Buddhist")),
    (u'Oth',_(u"Other")),
    ) 
MALE_GUARDIAN_CHOICES = (
    (u'fa',_(u"Father")),
    (u'gf',_(u"Grandfather")),
    (u'br',_(u"Brother")),
    (u'un',_(u"Uncle")),
    (u'ot',_(u"Other")),
    (u'-',_(u"-")),
    ) 
FEMALE_GUARDIAN_CHOICES = (
    (u'mo',_(u"Mother")),
    (u'gm',_(u"Grandmother")),
    (u'si',_(u"Sister")),
    (u'au',_(u"Aunt")),
    (u'ot',_(u"Other")),
    (u'-',_(u"-")),
    ) 

HEALTH_CHOICES = (
    (u'G',_(u"Good")),
    (u'A',_(u"Average")),
    (u'P',_(u"Poor")),
    (u'-',_(u"-")),
    )

CHARACTER_CHOICES = (
    (u'Fr', _(u"Friendly")),
    (u'Ta', _(u"Talkative")),
    (u'Qu', _(u"Quiet")),
    (u'Am', _(u"Ambitious")),
    )
    
GENDER_CHOICES = (
    (u'M',_(u"Boy")),
    (u'F',_(u"Girl")),
    )

def currentyear():
    return datetime.today().year
    
BIRTH_YEARS = [(x,y) for x,y in enumerate(range(1975,currentyear()+1))]

class Language(models.Model):
    """Names of languages"""
    

    name = models.CharField(_(u"Language"),
                            max_length=50)
    shortname = models.CharField(_(u"Language Code"), 
                                 max_length=10,
                                 unique=True)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": [_("Language already exists")]})

    class Meta:
    	verbose_name_plural = _(u"Languages")
        verbose_name = _(u"language")
        ordering = ('name',)
        

    def __unicode__(self):
            return u"%s" % self.name
 
class Schoolstandard(models.Model):
    

    name = models.CharField(_(u"School Standard"), max_length=150)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": 
                                   [_("School standard already exists")]})

    class Meta:
    	verbose_name_plural = _(u"School standards")
        verbose_name = _(u"school standard")

    def __unicode__(self):
            return u"%s" % self.name
        
class Doctor(models.Model):
    name = models.CharField(_(u"Name"), max_length=100)

    class Meta:
        verbose_name_plural = _(u"Doctors")
        verbose_name = _(u"doctor")

    def __unicode__(self):
        return u"%s" % self.name

class Hobby(models.Model):
    

    name = models.CharField(_(u"Free time"), max_length=150)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": [_("Hobby already exists")]})

    class Meta:
    	verbose_name_plural = _(u"Free time")
        verbose_name = _(u"free time")
        ordering = ('name',)

    def __unicode__(self):
        return u"%s" % self.name

class Character(models.Model):
    

    name = models.CharField(_(u"Character Type"), max_length=150)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": [_("Character already exists")]})

    class Meta:
    	verbose_name_plural = _(u"Character types")
        verbose_name = _(u"character type")

    def __unicode__(self):
        return u"%s" % self.name

class Job(models.Model):
    

    name = models.CharField(_(u"Job"), max_length=150)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": [_("Job already exists")]})

    class Meta:
    	verbose_name_plural = _(u"Jobs")
        verbose_name = _(u"Job")
        ordering = ('name',)

    def __unicode__(self):
        return u"%s" % self.name

class Longtermdiagnosis(models.Model):
    

    name = models.CharField(_(u"Longtermdiagnosis"), max_length=150)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": 
                                   [_("Long term diagnosis already exists")]})

    class Meta:
    	verbose_name_plural = _(u"Long term diagnosis")
        verbose_name = _(u"long term diagnosis")
        ordering = ('name',)

    def __unicode__(self):
        return u"%s" % self.name

class Medicalremarks(models.Model):
    

    name = models.CharField(_(u"Short term sickness"), max_length=150)

    def clean_fields(self, exclude=None):
        if not self.id and \
                self.__class__.objects.filter(name_en=self.name_en).count():
            raise ValidationError({"name_en": 
                                   [_("Short term sickness already exists")]})

    class Meta:
    	verbose_name_plural = _(u"Short term sicknesses")
        verbose_name = _(u"Short term sicknesses")
        ordering = ('name',)

    def __unicode__(self):
        return u"%s" % self.name
        
class Project(models.Model):
    """just a number and name as this holds areas"""

    code = models.IntegerField(_(u"Project Code Number"), unique=True)
    name = models.CharField(_(u"Project Name"), max_length=150, unique=True)
    admins = models.ManyToManyField(User,verbose_name = _("Project admins"))
    class Meta:
        verbose_name_plural = _(u"Projects")
        verbose_name = _(u"Project")
        ordering = ('code',)

    def __unicode__(self):
        return u"%s %s" % (self.code,self.name)
        
class Area(models.Model):
    

    code = models.IntegerField(_(u"Area Code Number"))
    name = models.CharField(_(u"Area Name"), max_length=150, unique=True)
    description = models.TextField(_(u"Area Description"), 
                                   blank=True, null=True)
    picture = models.ImageField(_(u"Picture of Area"), upload_to="images/misc",
                                blank=True, null=True)
    iscurrent = models.BooleanField(_(u"Is active"), default = True)
    project = models.ForeignKey(Project)
    lastchild = models.IntegerField(default=1,editable=False)

    class Meta:
        verbose_name_plural = _(u"Areas")
        verbose_name = _(u"area")
        unique_together = ('code','project')
        ordering = ('project','code')

    def __unicode__(self):
        return u"%s %s-%s" % (self.name,str(self.project.code),str(self.code))
        
class Sponsor(models.Model):
    

    code = models.IntegerField(_(u"Sponsor Code Number"), unique=True)
    fname = models.CharField(_(u"First Name"), max_length=80,
                             blank=True, null=True)
    lname = models.CharField(_(u"Last Name"), max_length=80)
    addnames = models.CharField(_(u"Additional names"), max_length=150,blank=True, null=True)
    street = models.TextField(_(u"Street Address"), blank=True, null=True)
    city = models.TextField(_(u"City or Town"), blank=True, null=True)
    postal = models.TextField(_(u"Postal Code"), blank=True, null=True)
    country = models.CharField(_(u"Country"), max_length=100, 
                               blank=True, null=True)
    phone = models.CharField(_(u"Phone Numbers"), max_length=50, 
                             blank=True, null=True)
    email = models.EmailField(_(u"Email Address"), blank=True, null=True)
    remarks = models.TextField(_(u"Remarks"), blank=True, null=True)
    iscurrent = models.BooleanField(_(u"Is active"), default = True)

    class Meta:
        ordering = ['lname','fname']
        verbose_name_plural = _(u"Sponsors")
        verbose_name = _(u"sponsor")

    def __unicode__(self):
        return u"%s %s %s" %(self.lname, self.fname,self.code)
        
class Child(models.Model):
    

    code = models.CharField(_(u"Child Code Number"),max_length=50, blank=True, null=True,editable=False)
    area = models.ForeignKey(Area, verbose_name=_(u"Area"))
    name = models.CharField(_(u"Child Name"), max_length=80)
    sex = models.CharField(_(u"Sex"), max_length=2, choices=GENDER_CHOICES)
    dob = models.DateField(_(u"Date of Birth"))
    language = models.ForeignKey(Language, verbose_name=_(u"Language"),
                                 related_name='languages')
    religion = models.CharField(_(u"Religion"), max_length=3, 
                                choices=RELIGION_CHOICES)
    maleguardiantype = models.CharField(_(u"Male Guardian type"), max_length=2, choices=MALE_GUARDIAN_CHOICES,
                        default='-')
    fathername = models.CharField(_(u"Male Guardian Name"), max_length=80)
    fatherjob = models.ForeignKey(Job, verbose_name=_(u"Male Guardian Job"),
                                  related_name='Fathers_Job')
    femaleguardiantype = models.CharField(_(u"Female Guardian type"), max_length=2, choices=FEMALE_GUARDIAN_CHOICES,
                        default='-')
    mothername = models.CharField(_(u"Female Guardian Name"), max_length=80)
    motherjob = models.ForeignKey(Job, verbose_name=_(u"Female Guardian Job"),
                                  related_name='Mothers_Job')
    remarks = models.TextField(_(u"Remarks"), blank=True, null=True)
    picture = models.ImageField(_(u"Picture of Child"),
                                upload_to="images/misc", 
                                blank=True, null=True)
    family_picture = models.ImageField(_(u"Picture of Family"),
                                       upload_to="images/misc", 
                                       blank=True, null=True)
    character = models.ManyToManyField(Character, verbose_name=_(u"Character"),
                                  related_name='Character')
    iscurrent = models.BooleanField(_(u"Is active"), default = True)
    schoolperf = models.CharField(_(u"School Performance"),
                                  max_length=3, choices=HEALTH_CHOICES,default='-')
    schoolstd = models.ForeignKey(Schoolstandard, 
                                  verbose_name=_(u"School Standard"))
    hobbies = models.ManyToManyField(Hobby, verbose_name=_(u"Free time"), 
                                     related_name='hobbies', blank=True, 
                                     null=True)
  
    class Meta:
        verbose_name_plural = _(u"Children")
        verbose_name = _(u"child")
        ordering = ["code"]
        unique_together = ('name','dob')
        
    def save(self, *args, **kwargs):
        lc = self.area.lastchild
        if not self.code:
            self.code = '%s-%s-%s' % (str(self.area.project.code),
                                        str(self.area.code),
                                        str(lc))
            self.area.lastchild = lc + 1
            self.area.save()
        super(Child,self).save(*args, **kwargs)
        
    def isfree(self):
        free = False
        if self.iscurrent:
            if self.sponsorship_set.all().count() == 0:
                free = True
            elif self.sponsorship_set.all().count() ==1:
                if not self.sponsorship_set.all()[0].iscurrent:
                    free = True
        return free
        
            

    def __unicode__(self):
        return u"%s : %s" %(self.code,self.name)

class ChildStory(models.Model):
    

    child = models.ForeignKey(Child)
    story = models.TextField()

    class Meta:
        verbose_name_plural = _("Child Stories")

    def __unicode__(self):
        return "%s" %(self.child)
        
class Sibling(models.Model):
    

    child = models.ForeignKey(Child)
    name = models.CharField(_("Name"),max_length=50)
    gender = models.CharField(_("Gender"),max_length=1,choices=GENDER_CHOICES)
    birthyear = models.IntegerField(_("Year of birth"),choices=BIRTH_YEARS)

    class Meta:
        verbose_name_plural = _("Siblings")

    def __unicode__(self):
        return "%s %s %s" %(self.name,self.get_gender_display(),self.get_birthyear_display())
    
class Sponsorship(models.Model):
    """ links child to sponsor, startdate enddate and comments"""
    

    sponsor = models.ForeignKey(Sponsor,verbose_name=_(u"Sponsor"))
    child = models.ForeignKey(Child, verbose_name=_(u"Child"))
    startdate = models.DateField(_(u"Start Date"))
    enddatedate = models.DateField(_(u"End Date"), blank=True, null=True)
    remarks = models.TextField(_(u"Remarks"), blank=True, null=True)
    iscurrent = models.BooleanField(_(u"Is active"), default = True)

    class Meta:
        verbose_name_plural = _(u"Sponsorships")
        verbose_name = _(u"sponsorship")

    def __unicode__(self):
        return u"%s: %s" %(self.sponsor, self.child)
        
class Projectsponsorship(models.Model):
    """ links child to sponsor, startdate enddate and comments"""
    

    sponsor = models.ForeignKey(Sponsor,verbose_name=_(u"Sponsor"))
    area = models.ForeignKey(Area,verbose_name=_(u"Area"))
    startdate = models.DateField(_(u"Start Date"))
    enddatedate = models.DateField(_(u"End Date"), blank=True, null=True)
    children = models.IntegerField(_(u"Number of children"), 
                                   blank=True, null=True)
    remarks = models.TextField(_(u"Remarks"), blank=True, null=True)
    iscurrent = models.BooleanField(_(u"Is active"), default = True)

    class Meta:
        verbose_name_plural = _(u"Community Sponsorships")
        verbose_name = _(u"Community sponshorship")

    def __unicode__(self):
        return u"%s: %s" %(self.sponsor, self.area)
        
class Checkup(models.Model):
    """ Doctors checkup report"""
    child = models.ForeignKey(Child,verbose_name=_(u"Child"))
    chkdate = models.DateField(_(u"Date"))
    height = models.IntegerField(_(u"Height in cms"), blank=True, null=True)
    weight = models.DecimalField(_(u"Weight in kgs"), max_digits=5, 
                                 decimal_places=2, blank=True, null=True)
    ltdiag = models.ManyToManyField(Longtermdiagnosis,
                                    verbose_name=_(u"Longterm Diagnosis"),
                                    blank=True, null=True)
    medrem = models.ManyToManyField(Medicalremarks,
                                    verbose_name=_(u"Medical Remarks"),
                                    blank=True, null=True)
    health = models.CharField(_(u"Health"), max_length=2, 
                              choices=HEALTH_CHOICES)
    doctor = models.ForeignKey(Doctor, verbose_name=_(u"Doctor"))

    class Meta:
        ordering = ['child']
        unique_together = (("child","chkdate"),)
        verbose_name_plural = _(u"Checkups")
        verbose_name = _(u"checkup")

    def __unicode__(self):
        return u"%s: %s" %(self.child, self.chkdate)
        
class Childnote(models.Model):
    

    child = models.ForeignKey(Child, verbose_name = _(u"Child"))
    notedate = models.DateField(_(u"Date"), auto_now = True)
    matter = models.TextField(_(u"Note"), blank = True, null = True)

    class Meta:
        verbose_name_plural = _(u"Notes on child")
        verbose_name = _(u"note on child")
        

    def __unicode__(self):
        return u"%s: %s" %(self.notedate, self.child)
        
class Sponsornote(models.Model):
    

    sponsor = models.ForeignKey(Sponsor, verbose_name = _(u"Sponsor"))
    notedate = models.DateField(_(u"Date"), auto_now = True)
    matter = models.TextField(_(u"Note"), blank = True, null = True)

    class Meta:
        verbose_name_plural = _(u"Notes on sponsor")
        verbose_name = _(u"note on sponsor")
        

    def __unicode__(self):
        return u"%s: %s" %(self.notedate, self.sponsor)
        
class Areanote(models.Model):
    

    area = models.ForeignKey(Area, verbose_name = _(u"Area"))
    notedate = models.DateField(_(u"Date"), auto_now = True)
    matter = models.TextField(_(u"Note"), blank = True, null = True)

    class Meta:
        verbose_name_plural = _(u"Notes on area")
        verbose_name = _(u"note on area")
        

    def __unicode__(self):
        return u"%s: %s" %(self.notedate, self.area)
        
class Download(models.Model):
    name = models.CharField(_(u"Name of Document"), max_length=250, unique=True)
    language = models.ForeignKey(Language, null=True, blank=True)
    document = models.FileField(_(u"File"), upload_to="images/downloads/")

    class Meta:
        verbose_name_plural = _(u"Downloads")
        verbose_name = _(u"download")

    def __unicode__(self):
        return u"%s : %s" %(self.name, self.language)
