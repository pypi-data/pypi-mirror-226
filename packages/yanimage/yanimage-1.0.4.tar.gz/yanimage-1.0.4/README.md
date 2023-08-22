# Yanimage

***Yanimage*** is a Python module that can parse image links on demand, as well as download them.

```
from yanimage import UrlImage, Download

links = UrlImage(search, value, iw, ih).parse()

Download(links, path).download()
```

UrlImage:

* search - search query

* value - number of desired images

* iw - the desired number of pixels wide. Default = None

* ih - the desired number of pixels wide. Default = None

Download:

* links - you need to insert a variable (array) with links to pictures.

* path - the path where you want to save the pictures.

* verbose - displays information about loading images. Sample output of 'Saved 1 of 4 pictures'