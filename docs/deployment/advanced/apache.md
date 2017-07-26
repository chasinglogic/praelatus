# Configuring Apache as a Reverse Proxy for Praelatus

Praleatus is a [Django](https://djangoproject.com) application, which means
it's written almost entirely in Python with a few C extensions. What this
means is, in regards to a web server, that it's not very efficient at just
serving static files of any kind. There are specialized pieces of software for
that sort of thing which are written C and tuned for maximum performance from
years of man hours. One such Web Server is Apache. In this guide we're going to
set up Apache to proxy requests to Praelatus while serving static content so you
can get the best performance out of your application instance.

# Installing Apache

Apache is included in every major distro's package repositories and so can be
installed via the package manager. This is the way we recommend installing
Apache however if you want to install from source [Apache has docs for
that](http://httpd.apache.org/docs/current/install.html). Below we've
documented the various package manager commands, choose the appropriate one for
your Distro of choice:

**Note:** Apache does not support Windows. If you're running on a Windows server
please view our docs on [Apache](deployment/advanced/apache).

**Ubuntu**

```bash
# apt-get install apache2
```

**Fedora**

```bash
# dnf install httpd
```

**CentOS / Redhat**

```bash
# yum install httpd
```

# Configuring Apache

Once you've installed Apache we can go about configuring it. First cd to the
appropriate directory:


**Ubuntu**

```bash
# cd /etc/apache2
```

**Fedora / CentOS / Redhat**

```bash
# cd /etc/httpd
```

Create a new file to hold the configuration for our site:

**Ubuntu**

```bash
# nano /etc/apache2/sites-available/mydomain.conf
```

**Fedora / CentOS / Redhat**

```bash
# nano /etc/httpd/conf.d/mydomain.conf
```

**Note:** This assumes you followed our [installation guide](deployment/linux)
if you deviated at all then update this file accordingly.

Changing mydomain to the domain name of the server you're running Praelatus on.
For the rest of this document replace mydomain with that domain.

Insert the following contents into that file:

```xml
# Change 80 to 443 if you're using SSL, which you should be.
<VirtualHost mydomain:80>
   # Serve static files with Apache as it's faster
   Alias "/static" "/opt/praelatus/data/static"

   # Force attachments to download instead of displaying in browser
   <Location "/media/tickets/attachments">
      Header set Content-Disposition attachment
   </Location>

   # Serve media such as project icons, user avatars, ticket attachments etc.
   Alias "/media" "/opt/praelatus/data/media"

   # Pass all other requests to Praelatus
   ProxyPass "/" "http://localhost:8000/"
   ProxyPassReverse "/" "http://localhost:8000/"
</VirtualHost>
```

Now if on Ubuntu run the following command to "enable" the site:

**Ubuntu**

```bash
# ln -s /etc/apache2/sites-enabled/mydomain.conf /etc/apache2/sites-available/mydomain.conf
```

Then we can enable and start Apache:

**Ubuntu**

```bash
# systemctl enable apache2
# systemctl start apache2
```

**Fedora / CentOS / Redhat**

```bash
# systemctl enable httpd
# systemctl start httpd
```

# Common Problems

## I get 400 (Bad Request) errors

Check that you've added your domain to the allowed_hosts in your Praelatus
config.yaml file as [described here](deployment/Linux#configuring-praelatus)

Running into a different problem? Feel free to open an
[issue](https://github.com/praelatus/praelatus/issues) or consult the [Apache
Official Documentation](https://httpd.apache.org/docs/)
