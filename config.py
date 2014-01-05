__author__ = 'eri'

etcpath = '/etc/apache2/'
availablepath = 'sites-available'
enabledpath = 'sites-enabled'
hostspath = '/var/virtualhosts/'


pattern = """
<VirtualHost *:80>
 ServerName {name}
 ServerAlias {name} www.{name}
 DocumentRoot {docroot}
 <Directory {docroot} >
 AllowOverride All
 </Directory>
</VirtualHost>
"""