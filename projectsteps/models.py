from django.db import models
from project.models import Project, get_file_path, image_upload_path, validate_file_extension
from projectpricer.models import Product
from publishedprojects.models import PublishedProject

# Create your models here.
class ProjectStep(models.Model):

    project_step_description = models.TextField(max_length = 200)
    project_step_image = models.ImageField(
        upload_to = image_upload_path,
        blank = True,
        null = True,
        )
    
    # def __unicode__(self):
    #     return unicode("Project {0} -- Step {1}".format(self.step_for_project.project_name))



class PurchasedComponent(models.Model):

    purchased_component_for_step = models.ForeignKey(ProjectStep)
    purchased_component_name = models.CharField(max_length = 20)
    purchased_component_url_link = models.URLField(null = True, blank = True, max_length = 10000)
    purchased_component_quantity = models.IntegerField(default = 1)
    product = models.ForeignKey(Product)
    
    def __unicode__(self):
        return unicode(self.purchased_component_name)   

class FabricatedComponent(models.Model):
    fabricated_component_for_project = models.ForeignKey(
    Project, 
    blank=True,
    null=True,
    related_name = 'base_project'
    )
    fabricated_component_from_project = models.ForeignKey(
    PublishedProject, 
    blank=True,
    null = True,
    related_name = 'component_project'
    )
    fabricated_component_quantity = models.IntegerField(default = 0)
    #price = Gotta get the price somehow....

    fabricated_component_for_step = models.ForeignKey(ProjectStep)


class ProjectFile(models.Model):
    project_file_for_project = models.ForeignKey(
        Project,
        blank=True,
        null=True,)
    project_file_for_step = models.ForeignKey(ProjectStep)


    project_file=models.FileField(
    upload_to=get_file_path,
    validators = [validate_file_extension], 
    )

class StepOrder(models.Model):
   step_order_for_project = models.ForeignKey(Project, null = True, blank = True)
   step = models.ForeignKey(ProjectStep)
   order = models.PositiveIntegerField(default = 0)