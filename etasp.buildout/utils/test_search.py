# -*- coding: utf8 -*-
from AccessControl.SecurityManagement import newSecurityManager
from Products.Archetypes import public as atapi
from Testing.makerequest import makerequest
from zLOG import LOG, INFO
from Products.CMFCore.utils import getToolByName
import time
import csv
import os
import sys

"""
$ /bin/instance run utils/test_search.py [SITE_ID]
"""

def setup_security():
    global app
    uf = app.acl_users
    user = uf.getUserById('admin').__of__(uf)
    newSecurityManager(None, user)
    app = makerequest(app)

def search_text(portal, searchtext):
    """Performs a text search in the catalog."""
    pc_tool = getToolByName(portal, 'portal_catalog')
    results = pc_tool(SearchableText=searchtext)
    for item in results:
        print "%s - %s" % (item.Title, item.getPath())


# do something
if __name__ == '__main__':

    # manage debug ambient
    setup_security()

    # define portal name
    PORTAL_NAME = sys.argv[1]
    portal = getattr(app, PORTAL_NAME)

    # start timer
    t1 = time.time()


    search_text(portal, "Some sample text")

    # commit changes
    #import transaction
    #transaction.commit()

    # stop timer
    t2 = time.time()

    # print time results
    print 'ID do Portal: %s' % (portal.getId())
    print str(t2-t1) + '\tseconds'
    print str((t2-t1)/60) + '\tminutes'
                                                
