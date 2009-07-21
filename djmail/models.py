from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

class AclDomainManager(models.Manager):
    def get_query_set(self):
        from middlewares import get_current_user
        return super(AclDomainManager, self).get_query_set().filter(pk__in = Access.objects.filter(group__in = get_current_user().groups.all()))

class Domain(models.Model):
    name = models.CharField(max_length = 128)
    type = models.CharField(choices = (('VIRTUAL', 'VIRTUAL',), ('RELAY', 'RELAY'), ('LOCAL', 'LOCAL')), max_length = 16)
    objects = AclDomainManager()
    class Meta:
        unique_together = ('name', 'type')
    def __unicode__(self):
        return self.name

class Access(models.Model):
    domain = models.ForeignKey(Domain)
    group = models.ForeignKey(Group)
    class Meta:
        verbose_name_plural = 'Access lists'
    def __unicode__(self):
        return "%s => %s" % (self.group, self.domain)

class User(models.Model):
    domain = models.ForeignKey(Domain)
    username = models.CharField(max_length = 64)
    password = models.CharField(max_length = 64)
    crypt = models.CharField(max_length = 64, blank = True)
    quota = models.IntegerField()
    quota_used = models.IntegerField()
    disabled = models.BooleanField(blank = True, default = False)
    class Meta:
        unique_together = ('username', 'domain')
    def __unicode__(self):
        return '%s@%s' % (self.username, self.domain)
    def save(self):
        import crypt, random, os
        salt = chr(random.randint(ord('0'), ord('Z'))) + chr(random.randint(ord('0'), ord('Z')))
        self.crypt = crypt.crypt(self.password, salt)
        super(User, self).save()
        os.system('%s/createdir %s' % (settings.PROJECT_ROOT, self.pk))

class Alias(models.Model):
    local_part = models.CharField(max_length = 64)
    domain = models.ForeignKey(Domain)
    destination = models.CharField(max_length = 128)
    class Meta:
        unique_together = ('local_part', 'domain')
        verbose_name_plural = 'Aliases'
    def __unicode__(self):
        return '%s@%s => %s' % (self.local_part, self.domain.name, self.destination)

class Route(models.Model):
    domain = models.CharField(max_length = 128)
    server = models.CharField(max_length = 128)
    class Meta:
        unique_together = ('domain', 'server')
    def __unicode__(self):
        return '%s -> %s' % (self.domain, self.server)
