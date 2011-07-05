Alias /static/ "/var/www/sisquiropraxia/static/"
<Directory "/var/www/sisquiropraxia/static">
        Order allow,deny
        Options Indexes
        Allow from all
        IndexOptions FancyIndexing
</Directory>

Alias /media/ "/usr/lib/python2.5/site-packages/django/contrib/admin/media/"
<Directory "/usr/lib/python2.5/site-packages/django/contrib/admin/media">
        Order allow,deny
        Options Indexes
        Allow from all
        IndexOptions FancyIndexing
</Directory>


WSGIDaemonProcess sisquiropraxia python-path=/var/envs/sisquiropraxia/lib/python2.6/site-packages
WSGIProcessGroup sisquiropraxia
WSGIScriptAlias / "/var/www/sisquiropraxia/deploy/script.wsgi"
WSGIPassAuthorization On


<Directory "/var/www/sisquiropraxia/deploy">
        Allow from all
</Directory>

ErrorLog /var/log/apache2/sisquiropraxia_error.log
CustomLog /var/log/apache2/sisquiropraxia_access.log combined
LogLevel warn

