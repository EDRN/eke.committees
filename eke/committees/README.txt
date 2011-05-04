This package provides Plone 3 content objects for the EDRN Knowledge
Environment (EKE_)'s management, display, and RDF ingest of committees.


Content Types
=============

The content types introduced in this package include the following:

Committee Folder
    A folder that contains Committees.  It can also repopulate its
    contents from an RDF data source.
Committee
    A single EDRN committee identified by URI_.

The remainder of this document demonstrates the content types and RDF ingest
using a series of functional tests.


Tests
=====

In order to execute these tests, we'll first need a test browser::

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portalURL = self.portal.absolute_url()
        
We also change some settings so that any errors will be reported immediately::

    >>> browser.handleErrors = False
    >>> self.portal.error_log._ignored_exceptions = ()
        
We'll also turn off the portlets.  Why?  Well for these tests we'll be looking
for specific strings output in the HTML, and the portlets will often have
duplicate links that could interfere with that::

    >>> from zope.component import getUtility, getMultiAdapter
    >>> from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
    >>> for colName in ('left', 'right'):
    ...     col = getUtility(IPortletManager, name=u'plone.%scolumn' % colName)
    ...     assignable = getMultiAdapter((self.portal, col), IPortletAssignmentMapping)
    ...     for name in assignable.keys():
    ...             del assignable[name]

And finally we'll log in as an administrator::

    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portalURL + '/login_form?came_from=' + portalURL)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()


Addable Content
---------------

Here we'll exercise some of the content objects available in this project and
demonstrate their properties and constraints.


Committee Folder
~~~~~~~~~~~~~~~~

A Committee Folder contains Committees.  They can be created anywhere in the
portal::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='committee-folder')
    >>> l.url.endswith('createObject?type_name=Committee+Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Senate Committees'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/committees/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'senate-committees' in portal.objectIds()
    True
    >>> f = portal['senate-committees']
    >>> f.title
    'Senate Committees'
    >>> f.description
    'This folder is just for functional tests.'
    >>> f.rdfDataSource
    'testscheme://localhost/committees/a'

Committee Folders hold Committees as well as other Committee Folders.  We'll
test adding Committees below, but let's make sure there's a link to create
nested Committee Folders::

    >>> browser.open(portalURL + '/senate-committees')
    >>> l = browser.getLink(id='committee-folder')
    >>> l.url.endswith('createObject?type_name=Committee+Folder')
    True


Committee
~~~~~~~~~

A single Committee object represents an EDRN committee.  Committees can be
created only in Committee Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='committee')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

However, before we create one, we'll need some people in the system that can
be committee members.  So, let's add some::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = 'Questionable Sites'
    >>> browser.getControl(name='description').value = 'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/b'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites/ingest')

Now we can create our own committee::

    >>> browser.open(portalURL + '/senate-committees')
    >>> l = browser.getLink(id='committee')
    >>> l.url.endswith('createObject?type_name=Committee')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = 'Agriculture, Nutrition, and Forestry'
    >>> browser.getControl(name='abbreviatedName').value = 'ANF'
    >>> browser.getControl(name='committeeType').value = 'Committee'
    >>> browser.getControl(name='chair:list').displayValue = ['Alottaspank, Dirk (2d)']
    >>> browser.getControl(name='coChair:list').displayValue = ['Cusexijilomimi, Crystal Hotstuff (3d)', 'Pawaka, Makin (3d)']
    >>> browser.getControl(name='consultant:list').displayValue = ['Pawaka, Makin (3d)']
    >>> browser.getControl(name='member:list').displayValue = ['Alottaspank, Dirk (2d)', 'Cusexijilomimi, Crystal Hotstuff (3d)', 'Pawaka, Makin (3d)']
    >>> browser.getControl(name='form.button.save').click()
    >>> 'agriculture-nutrition-and-forestry' in f.objectIds()
    True
    >>> c = f['agriculture-nutrition-and-forestry']
    >>> c.title
    'Agriculture, Nutrition, and Forestry'
    >>> c.committeeType
    'Committee'
    >>> len(c.chair)
    1
    >>> c.chair[0].title
    'Alottaspank, Dirk'
    >>> len(c.coChair)
    2
    >>> c.coChair[0].title, c.coChair[1].title
    ('Cusexijilomimi, Crystal Hotstuff', 'Pawaka, Makin')
    >>> len(c.consultant)
    1
    >>> c.consultant[0].title
    'Pawaka, Makin'
    >>> len(c.member)
    3
    >>> c.member[0].title, c.member[1].title, c.member[2].title
    ('Alottaspank, Dirk', 'Cusexijilomimi, Crystal Hotstuff', 'Pawaka, Makin')


Committee View
~~~~~~~~~~~~~~

The default view for a Committee is fairly basic.  The only special thing is
that members should be hyperlinks::

    >>> browser.open(portalURL + '/senate-committees/agriculture-nutrition-and-forestry')
    >>> browser.contents
    '...Chair...href=.../alottaspank-dirk...Alottaspank, Dirk...'


Committee Folder View
~~~~~~~~~~~~~~~~~~~~~

A Committee Folder by default displays its committees in alphabetical order by
title.  Let's check that.  First, we'll need to toss in a couple other
committees::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Foreign Relations'
    >>> browser.getControl(name='committeeType').value = 'Committee'
    >>> browser.getControl(name='form.button.save').click()

That's one; now another::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Armed Services'
    >>> browser.getControl(name='committeeType').value = 'Committee'
    >>> browser.getControl(name='form.button.save').click()

Now, the ordering::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.contents
    '...Agriculture...Armed Services...Foreign Relations...'

Perfect.  Note though that all types of committees we added above were just
that: plain committees.  There are also subcommittees, working groups, teams,
and collaborative groups.  Each of the committees within those groupings
should appear separately, and the groupings themselves in alphabetical order.

Adding yet more committees then::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Disaster Recovery'
    >>> browser.getControl(name='committeeType').value = 'Subcommittee'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Tiger Research'
    >>> browser.getControl(name='committeeType').value = 'Team'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Bipartisan'
    >>> browser.getControl(name='committeeType').value = 'Working Group'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Progress Limiting'
    >>> browser.getControl(name='committeeType').value = 'Collaborative Group'
    >>> browser.getControl(name='form.button.save').click()

And the ordering?  Take a look::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.contents
    '...Collaborative Groups...Progress...Committees...Subcommittees...Disaster...Teams...Tiger......Working Groups...Bipartisan...'

Additionally, any nested Committees Folders should appear above the list of
committees::

    >>> 'Special Subsection' not in browser.contents
    True
    >>> browser.getLink(id='committee-folder').click()
    >>> browser.getControl(name='title').value = 'Special Subsection on Independent Committees'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.contents
    '...Special Subsection...Collaborative Groups...Committees...Subcommittees...Teams...Working Groups...'


RDF Ingestion
-------------

Committee Folders support a URL-callable method that causes them to ingest
content via RDF, just like Knowledge Folders in the ``eke.knowledge`` package.

First, let's create a new, empty folder with which to play::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='committee-folder').click()
    >>> browser.getControl(name='title').value = 'House Committees'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/committees/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/house-committees/content_status_modify?workflow_action=publish')
    >>> f = portal['house-committees']

Ingesting from the RDF data source ``testscheme://localhost/committees/a``::

    >>> browser.getLink('Ingest').click()
    >>> browser.contents
    '...The following items have been created...Appropriations...'
    >>> len(f.objectIds())
    2
    >>> 'appropriations' in f.objectIds() and 'ways-and-means' in f.objectIds()
    True
    >>> a = f['appropriations']
    >>> a.title
    'Appropriations'
    >>> a.abbreviatedName
    'App'
    >>> a.committeeType
    'Committee'
    >>> len(a.chair), a.chair[0].title
    (1, 'Alottaspank, Dirk')
    >>> len(a.coChair), a.coChair[0].title
    (1, 'Pawaka, Makin')
    >>> len(a.consultant), a.consultant[0].title
    (1, 'Alottaspank, Dirk')
    >>> len(a.member)
    2
    >>> memberNames = [i.title for i in a.member]
    >>> 'Alottaspank, Dirk' in memberNames and 'Cusexijilomimi, Crystal Hotstuff' in memberNames
    True

The source ``testscheme://localhost/committees/b`` contains both the above
committees and an additional one.  Since ingestion purges existing objects, we
shouldn't get duplicate copies of the above committees::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/committees/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> objIDs = f.objectIds()
    >>> objIDs.sort()
    >>> objIDs
    ['appropriations', 'science-and-technology', 'ways-and-means']


RDF Data Sources
~~~~~~~~~~~~~~~~

The URL to an RDF data source is nominally displayed on a Committee folder,
but only if you're an administrator.  Let's log in as an administrator::

    >>> browser.open(portalURL + '/login_form?came_from=' + portalURL)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

And look, there's the RDF URL::

    >>> browser.open(portalURL + '/house-committees')
    >>> browser.contents
    '...RDF Data Source...testscheme://localhost/committees/b...'

However, mere mortals shouldn't see that::

    >>> browser.open(portalURL + '/logout')
    >>> browser.open(portalURL + '/house-committees')
    >>> 'RDF Data Source' not in browser.contents
    True

That's it!


.. References:
.. _EKE: http://cancer.jpl.nasa.gov/documents/applications/knowledge-environment
.. _RDF: http://w3.org/RDF/
.. _URI: http://w3.org/Addressing/
