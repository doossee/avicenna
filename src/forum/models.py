from django.db import models

from src.management.models import User, Doctor, Patient
from django.utils.translation import gettext_lazy as _


class DiseaseCategory(models.Model):
    
    """Disease category model"""

    title = models.CharField(verbose_name=_("Disease category title"), max_length=255)
    description = models.TextField(verbose_name=_("Disease category desctiption"), blank=True)

    class Meta:
        verbose_name = _("Disease category")
        verbose_name_plural = _("Disease categories")


class DiseasePost(models.Model):
    
    """Disease post model """

    sender = models.ForeignKey(
        verbose_name=_("Disease post sender"), to=User,
        on_delete=models.CASCADE, related_name='disease_posts'
    )
    title = models.CharField(verbose_name=_("Disease post title"), max_length=255)
    content = models.TextField(_("Disease post content"))
    intensity = models.IntegerField(_("Disease intentity"))
    categories = models.ForeignKey(
        verbose_name=_("Disease category"), to=DiseaseCategory,
        on_delete=models.SET_NULL, related_name='disease_posts', null=True
    )
    views = models.ManyToManyField(User, related_name='viewed_posts', blank=True)
    created_at = models.DateTimeField(verbose_name=_("Create date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Update date"), auto_now=True)

    class Meta:
        verbose_name = _("Disease post")
        verbose_name_plural = _("Disease posts")


class DiseasePostAttachment(models.Model):
    
    """Disease post attachment model"""

    disease_post = models.ForeignKey(
        verbose_name=_("Disease post"), to=DiseasePost,
        on_delete=models.CASCADE, related_name='attachments'
    )
    title = models.CharField(verbose_name=_("Title"), max_length=90)
    attachment = models.FileField(verbose_name=_("Attachment"), upload_to='uploads/post_attachments/')  
         
    class Meta:
        verbose_name = _("Disease post")
        verbose_name_plural = _("Disease posts")


class Comment(models.Model):

    """Comment model"""

    sender = models.ForeignKey(
        verbose_name=_("Comment sender"), to=User,
        on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        verbose_name=_("Comment post"), to=DiseasePost,
        on_delete=models.CASCADE, related_name='comments'
    )
    parent = models.ForeignKey(
        verbose_name=_("Parent comment"), to='self',
        on_delete=models.CASCADE, related_name='replies', null=True, blank=True
    )
    content = models.TextField(verbose_name=_("Comment text"))
    likes = models.ManyToManyField(verbose_name=_("Comment likes"), to=User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(verbose_name=_("Comment dislikes"), to=User, related_name='disliked_comments', blank=True)
    created_at = models.DateTimeField(verbose_name=_("Create date"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Update date"), auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


# class Rating(models.Model):

#     """Rating model"""

#     RATE_CHOICES = (
#         (1, _('Ok')),
#         (2, _('Fine')),
#         (3, _('Good')),
#         (4, _('Amazing')),
#         (5, _('Incredible'))
#     )
     
    
#     doctor = models.ForeignKey(
#         to=Doctor,
#         verbose_name=_('Rated doctor'),
#         related_name='ratings',
#         on_delete=models.CASCADE
#     )
    
#     rate = models.PositiveSmallIntegerField(_('Rate'),choices=RATE_CHOICES)
#     review = models.TextField(_('Review text'))

#     # Create and update dates
#     created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

#     class Meta:
#         verbose_name = _('Rating')
#         verbose_name_plural = _('Ratings')