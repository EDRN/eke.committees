# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Committees: views for content types.
'''

from Acquisition import aq_inner
from eke.committees.interfaces import ICommittee, ICommitteeFolder
from eke.knowledge.browser.views import KnowledgeFolderView, KnowledgeObjectView
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class CommitteeFolderView(KnowledgeFolderView):
    '''Default view of a Committee Folder.'''
    __call__ = ViewPageTemplateFile('templates/committeefolder.pt')
    def haveCommittees(self):
        return len(self.committees()) > 0
    def haveSubfolders(self):
        return len(self.subfolders()) > 0
    @memoize
    def committees(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=ICommittee.__identifier__, path=dict(query='/'.join(context.getPhysicalPath()), depth=1))
        byType = {}
        for b in results:
            if not b.committeeType: continue
            committeeType = b.committeeType + u's' # FIXME: Cheesy non-i18n pluralization
            if committeeType not in byType: byType[committeeType] = []
            committees = byType[committeeType]
            committees.append(dict(title=b.Title, url=b.getURL()))
        results = []
        for committeeType, committees in byType.items():
            committees.sort(lambda a, b: cmp(a['title'], b['title']))
            results.append(dict(title=committeeType, committees=committees))
        results.sort(lambda a, b: cmp(a['title'], b['title']))
        return results
    @memoize
    def subfolders(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=ICommitteeFolder.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in results]

class CommitteeView(KnowledgeObjectView):
    '''Default view of a Committee.'''
    __call__ = ViewPageTemplateFile('templates/committee.pt')
