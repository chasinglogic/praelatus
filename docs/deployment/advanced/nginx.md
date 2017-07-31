# Configuring NGINX as a Reverse Proxy for Praelatus

Praleatus is a [Django](https://djangoproject.com) application, which means
it's written almost entirely in Python with a few C extensions. What this
means is, in regards to a web server, that it's not very efficient at just
serving static files of any kind. There are specialized pieces of software for
that sort of thing which are written C and tuned for maximum performance from
years of man hours. One such Web Server is NGINX. In this guide we're going to
set up NGINX to proxy requests to Praelatus while serving static content so you
can get the best performance out of your application instance.


# Installing NGINX

NGINX is included in every major distro's package repositories and so can be
installed via the package manager. This is the way we recommend installing
NGINX however if you want to install from source [NGINX has docs for
that](http://nginx.org/en/docs/configure.html). Below we've documented the
various package manager commands, choose the appropriate one for your Distro of
choice:

**Note:** NGINX does not support Windows. If you're running on a Windows server
please view our docs on [Apache](deployment/advanced/apache).

**Ubuntu**

```bash
# apt-get install nginx
```

**Fedora**

```bash
# dnf install nginx
```

**CentOS / Redhat**

```bash
# yum install nginx
```

Once you've installed NGINX we can go about configuring it. First cd to the
appropriate directory:

```bash
# cd /etc/nginx/conf.d
```

Now we're going to create a file called `mydomain.conf` replacing `mydomain`
with whatever domain name is pointing to your instance of Praelatus. Get used
to doing that as I will be using `mydomain` as placeholder text throughout this
document.


# Configuring NGINX


With the text file `/etc/nginx/conf.d/mydomain.conf` open let's insert the
following contents:

**Note:** This assumes you followed our [installation guide](deployment/linux)
if you deviated at all then update this file accordingly.


```nginx
# A server block denotes a "virtual host" which is just a way for nginx to know
# how to handle requests from the matching domain name.
server {
   # Change this to 443 if you're using SSL, which you should be.
   listen 80;

   # If using ssl uncomment and update these lines to point to your key and
   # cert files otherwise continue on.
   # ssl    on;
   # ssl_certificate    /etc/ssl/your_domain_name.pem;
   # ssl_certificate_key    /etc/ssl/your_domain_name.key;

   # mydomain again should be replaced with the domain name of the running
   # instance. The word default here tells NGINX to fall back to this server
   # block if no matching server blocks are found for a request.
   server_name mydomain default;

   # This is where we tell NGINX to serve static assets (images, javascript,
   # css, etc.) which are in Praelatus' data directory. Shown below is the
   # default location. If you've customized the data directory location then
   # update the alias statement accordingly.
   location /static/ {
       alias /opt/praelatus/data;
   }

   # This tells NGINX to serve the attachments and force the download of them.
   # Without this block attachments will still work but if it's a format the
   # browser can recognize (png, xml, txt, etc.) then it will try to display it
   # instead of downloading it.
   location /media/tickets/attachments {
      alias /opt/praelatus/data/media/tickets;
      add_header Content-Disposition "attachment";
   }

   # Serve the rest of the media appropriately (project icons, user avatars,
   # etc.)
   location /media/ {
      alias /opt/praelatus/data/media;
   }

   # Finally all other requests should go to Praelatus.
   location / {
       include proxy_params;
       proxy_pass http://localhost:8000;
   }
}
```

With this configuration in place you can enable and start nginx:

```bash
# systemctl enable nginx
# systemctl restart nginx
```

# Common Problems

## I still get the default "Welcome to NGINX!" page

Some distros have customizations that make NGINX not check certain areas for
configuration. Check your `/etc/nginx/nginx.conf` file for a line that looks
like the following:

```
include conf.d/*;
```

If that's missing then add that line.


## I get 400 (Bad Request) errors

Check that you've added your domain to the allowed_hosts in your Praelatus
config.yaml file as [described here](deployment/Linux#configuring-praelatus)


Running into a different problem? Feel free to open an
[issue](https://github.com/praelatus/praelatus/issues) or consult the excellent
[NGINX Official Documentat](https://nginx.org/en/docs/)
