# coding: utf-8
from itertools import chain
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.postgres.operations import HStoreExtension
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from inface import settings
from dateutil.relativedelta import *
import datetime

class SysConfig(models.Model):
    param = HStoreField(verbose_name=_(u'System Config Param'),)
    def __unicode__(self):
        return u'%s' % _(u'System Config')

class Dept(models.Model):
    name = models.CharField(max_length=50, verbose_name=_(u'department'))
    parent = models.ForeignKey("self", verbose_name=_(u'parent'),null=True,blank=True)
    level = models.IntegerField(verbose_name=_(u'department level'), default=0, editable=False)
    rank = models.IntegerField(verbose_name=_(u'rank'), default=0)
    is_root = models.BooleanField(default=False, verbose_name=_(u'root'))
    is_removed = models.BooleanField(default=False, verbose_name=_(u'delete'))

    def save(self, force_insert=False, **kwargs):
        old_level = self.level
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        if old_level != self.level:
            for child in self.children():
                child.save()
        super(Dept, self).save(force_insert, **kwargs)

    def name_with_spacer(self):
        spacer = ''
        for i in range(0, self.level):
            spacer += u'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        if self.level > 0:
            spacer += u'|-&nbsp;'
        return spacer + self.name

    def get_flattened(self):
        flat_structure = [self]
        for child in self.children():
            flat_structure = chain(flat_structure, child.get_flattened())
        return flat_structure

    def siblings(self):
        if not self.parent:
            return Dept.objects.none()
        else:
            if not self.pk:
                return self.parent.children()
            else:
                return self.parent.children().exclude(pk=self.pk)

    def has_siblings(self):
        return self.siblings().count() > 0

    def children(self):
        _children = Dept.objects.filter(parent=self,is_removed=False).order_by('rank',)
        for child in _children:
            child.parent = self
        return _children

    def has_children(self):
        return self.children().count() > 0

    def as_tree(self):
        children = list(self.father.filter(is_removed=False))
        branch = bool(children)
        yield branch, self
        for child in children:
            for next in child.as_tree():
                yield next
        yield branch, None
    def __unicode__(self):
        return u'%s' % self.name
    def grading_name(self):
        return self.parent and (u'%s » %s' % (self.parent.name,self.name)) or (u'%s' % self.name)
    @property
    def root_dept(self):
        return Dept.objects.get(is_root=True)

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name,last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    first_name = models.CharField(verbose_name=_(u'first name'), max_length=50)
    last_name = models.CharField(verbose_name=_(u'last name'), max_length=50)
    alias = models.CharField(verbose_name=_(u'user alias') , unique=True, max_length=50)
    dept = models.ForeignKey(Dept, verbose_name=_(u'department'), null=True)
    position = models.CharField(verbose_name=_(u'position'), max_length=40,blank=True)
    mobile = models.CharField(verbose_name=_(u'mobile'), max_length=12,unique=True,blank=True)
    email = models.EmailField(verbose_name=_(u'email'),max_length=200,unique=True,db_index=True,)
    attr = HStoreField(verbose_name=_(u'user attributes'),)
    is_active = models.BooleanField(verbose_name=_(u'active'),default=True)
    is_admin = models.BooleanField(verbose_name=_(u'administrator'),default=False)
    is_leader = models.BooleanField(verbose_name=_(u'leader'),default=False)
    is_virtual_user = models.BooleanField(verbose_name=_(u'virtual user'),default=False)
    no_login = models.BooleanField(verbose_name=_(u'not allowed login'),default=False)
    master = models.ForeignKey("self", verbose_name=_(u'master user'),null=True,blank=True)
    order = models.PositiveIntegerField(verbose_name=_(u'order by'), default=0)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        ordering = ['order']

    def get_full_name(self):
        # The user is identified by their email address
        return u'%s%s' % (self.first_name,self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin