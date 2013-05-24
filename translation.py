from modeltranslation.translator import translator, TranslationOptions
from kenyakids.web.models import *

class LanguageTranslationOptions(TranslationOptions):
    fields = ('name',)
class SchoolstandardTranslationOptions(TranslationOptions):
    fields = ('name',)
class DoctorTranslationOptions(TranslationOptions):
    fields = ('name',)
class HobbyTranslationOptions(TranslationOptions):
    fields = ('name',)
class CharacterTranslationOptions(TranslationOptions):
    fields = ('name',)
class JobTranslationOptions(TranslationOptions):
    fields = ('name',)
class LongtermdiagnosisTranslationOptions(TranslationOptions):
    fields = ('name',)
class MedicalremarksTranslationOptions(TranslationOptions):
    fields = ('name',)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('name',)
class AreaTranslationOptions(TranslationOptions):
    fields = ('name','description')
class SponsorTranslationOptions(TranslationOptions):
    fields = ('remarks',)
class ChildTranslationOptions(TranslationOptions):
    fields = ('remarks',)
class ChildStoryTranslationOptions(TranslationOptions):
    fields = ('story',)
class SponsorshipTranslationOptions(TranslationOptions):
    fields = ('remarks',)
class ProjectsponsorshipTranslationOptions(TranslationOptions):
    fields = ('remarks',)
class ChildnoteTranslationOptions(TranslationOptions):
    fields = ('matter',)
class SponsornoteTranslationOptions(TranslationOptions):
    fields = ('matter',)
class AreanoteTranslationOptions(TranslationOptions):
    fields = ('matter',)
class DownloadTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Language, LanguageTranslationOptions)
translator.register(Schoolstandard,SchoolstandardTranslationOptions)
translator.register(Doctor,DoctorTranslationOptions)
translator.register(Hobby,HobbyTranslationOptions)
translator.register(Character,CharacterTranslationOptions)
translator.register(Job,JobTranslationOptions)
translator.register(Project,ProjectTranslationOptions)
translator.register(Longtermdiagnosis,LongtermdiagnosisTranslationOptions)
translator.register(Medicalremarks,MedicalremarksTranslationOptions)
translator.register(Area, AreaTranslationOptions)
translator.register(Areanote, AreanoteTranslationOptions)
translator.register(Child, ChildTranslationOptions)
translator.register(ChildStory, ChildStoryTranslationOptions)
translator.register(Childnote, ChildnoteTranslationOptions)
translator.register(Sponsor, SponsorTranslationOptions)
translator.register(Sponsornote, SponsornoteTranslationOptions)
translator.register(Sponsorship, SponsorshipTranslationOptions)
translator.register(Download, DownloadTranslationOptions)
translator.register(Projectsponsorship, ProjectsponsorshipTranslationOptions)
