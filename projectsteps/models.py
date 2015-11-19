from django.db import models
from projectpricer.models import Product
from project.models import Project
import os

# Create your models here.



def get_file_path(instance, filename):
    project_step_id = instance.project_file_for_step_id
    file_upload_path = os.path.join('step_files',
        'step_%s' % project_step_id,
        filename
        )
    return file_upload_path 


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg',]
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')


def get_step_image_path(instance, filename):
    image_upload_path = os.path.join('step_files',
        'PLACEHOLDER',
        filename
        )
    return image_upload_path






class ProjectStep(models.Model):

    project_step_description = models.TextField(blank=True, null=True, max_length = 200)
    project_step_image = models.ImageField(
        upload_to = get_step_image_path,
        blank = True,
        null = True,
        )
    project_step_video = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.project_step_description



class PurchasedComponent(models.Model):

    purchased_component_for_step = models.ForeignKey(ProjectStep)
    purchased_component_name = models.CharField(max_length = 300)
    purchased_component_url_link = models.URLField(null = True, blank = True)
    purchased_component_quantity = models.IntegerField(default = 1)
    product = models.ForeignKey(Product)
    
    def __unicode__(self):
        return unicode(self.product.name)   

class FabricatedComponent(models.Model):
    fabricated_component_for_project = models.ForeignKey(
    Project, 
    blank=True,
    null=True,
    related_name = 'base_project'
    )
    fabricated_component_from_project = models.ForeignKey(
    'publishedprojects.PublishedProject', 
    blank=True,
    null = True,
    related_name = 'component_project'
    )
    fabricated_component_quantity = models.IntegerField(default = 0)

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

   def __unicode__(self):
    return unicode('Project Order for: ' + self.step_order_for_project.project_name)