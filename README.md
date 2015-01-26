#Wikipedia Enquirer in Python#

This module implements a Python library to query wikipedia using the webservice endpoint at http://en.wikipedia.org/w/api.php.

##Installation##

You will need just to clone the repository and make it available for Python (python path, symbolic link...)


##Usage##

Once installed you can use it from your own python scrips:
```shell
from wikipediaEnquirerPy import *

page_id = '39942'   #This is for the wikipage of Jennifer Anniston
print get_plain_text_from_page_id(page_id)
````

The list of functions currently implemented are (more functionalities can be easily added):
* get_all_links_from_page_title(page_title,include_all=False): returns a list of all the wikilinks for the given page title
* get_plain_text_from_page_id(page_id): returns the text from the wikipedia page for the given page_id (39942 for instance for J. Anniston)
* get_plain_text_from_title(title): returns the text for the wikipedia page for the given page title (Jennifer_Aniston for instance)

The library implements a local cache repository to avoid duplicated queries using the online interface. The first time a query is launched, the
online interface is queried and the results are stored in a local folder (in the subfolder `.wikipedia_cache`). Next calls with the same query
will be read directly from the local cache. You can clean up the local cache by running the command `clean_cache.sh`.

##Contact##
* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl  rubensanvi@gmail.com
* http://rubenizquierdobevia.com/

##License##

Sofware distributed under GPL.v3, see LICENSE file for details.