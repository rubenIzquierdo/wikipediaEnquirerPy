import os
import sys
import cPickle
import hashlib
import urllib2
import cjson
import time

from urllib import urlencode


WIKI_API_URL = 'http://en.wikipedia.org/w/api.php'

__thisfolder__ = os.path.dirname(os.path.realpath(__file__))
__cache_folder__ = __thisfolder__+'/.wikipedia_cache'

def __get_name_cached_file(query):
    cached_file = __cache_folder__+'/'+hashlib.sha256(query).hexdigest()
    return cached_file


def query_wikipedia(dict_values):
    data_query = urlencode(dict_values)
    cached_file = __get_name_cached_file(data_query)
    if os.path.exists(cached_file):
        fd = open(cached_file,'rb')
        json_obj = cPickle.load(fd)
        fd.close()
    else:
        req = urllib2.Request(WIKI_API_URL,data_query)
                
        #Sometimes there are errors if you query too fast :)
        max_retry = 20
        wait_this = 1
        raw_data = None
        for n in range(0,max_retry):
            try:
                response = urllib2.urlopen(req)
                raw_data = response.read()
            except:
                #An error has ocurred, wait a bit and keep trying
                raw_data = None
                print>>sys.stderr,'Error querying wikipedia with,',str(dict_values)
                print>>sys.stderr,'Waiting',wait_this,'seconds'
                sys.stderr.flush()
                time.sleep(wait_this)
                wait_this += 2
            if raw_data is not None:
                break
        if raw_data is not None:    
            json_obj = cjson.decode(raw_data)
            if not os.path.exists(__cache_folder__): 
                os.mkdir(__cache_folder__)
            fd = open(cached_file,'wb')
            cPickle.dump(json_obj, fd, protocol=-1)
            fd.close()
        else:
            json_obj = {}
    return json_obj

def get_all_links_from_page_title(page_title,include_all=False):
    """
    This needs to run more than once as it only returns max 500
    """
    continue_here = None
    we_are_done = False
    all_links = []
    while not we_are_done:
        values = {'action' : 'query',
                  'prop' : 'links',
                  'titles': page_title,
                  'format' : 'json',
                  'rawcontinue': '1',
                  'pllimit': '500'}
        
        if continue_here is not None:
            values['plcontinue'] = continue_here
            
        json_obj = query_wikipedia(values)
        if 'query_continue' in json_obj:
            continue_here = json_obj['query_continue']['links']['plcontinue']
        else:
            we_are_done = True
        
        try:
            json_links = (json_obj['query']['pages'].values()[0])['links']
        except:
            json_links = []
            
        for link in json_links:
            link_title = link['title'].replace(' ','_')
            if include_all:
                all_links.append(link_title)
            else:
                if 'Wikipedia:' not in link_title and 'Template:' not in link_title and 'Help:' not in link_title and 'Category:' not in link_title and 'Template_talk:' not in link_title:
                    all_links.append(link_title)
    return all_links


def get_plain_text_from_page_id(page_id):
    values = {'action' : 'query',
              'prop' : 'extracts',
              'explaintext': '1',
              'pageids': page_id,
              'format' : 'json'}
    json_obj = query_wikipedia(values)
    try:
        text = json_obj['query']['pages'][page_id]['extract']
    except:
        text = None
    return text
    
def get_plain_text_from_title(title):
    values = {'action' : 'query',
              'prop' : 'extracts',
              'explaintext': '1',
              'titles': title,
              'format' : 'json'}
    json_obj = query_wikipedia(values)
    try:
        text = (json_obj['query']['pages'].values())[0]['extract']
    except:
        text = None
    return text

if __name__ == '__main__':
    page_id = '39942'   #This is for the wikipage of Jennifer Anniston
    #print get_plain_text_from_page_id(page_id)
    
    page_title = 'Jennifer_Aniston'
    print get_plain_text_from_title(page_title)