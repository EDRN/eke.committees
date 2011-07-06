# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Committees: RDF ingest for Committee Folders and their Committees.
'''

from Acquisition import aq_inner
from eke.knowledge.browser.rdf import KnowledgeFolderIngestor, CreatedObject, registerHandler, IngestHandler
from eke.knowledge.browser.utils import updateObject
from Products.CMFCore.utils import getToolByName
from rdflib import URIRef

_committeeTypeURI = URIRef('http://edrn.nci.nih.gov/rdf/types.rdf#Committee')
_collabGroup = 'edrnsite.collaborations.interfaces.collaborativegroupindex.ICollaborativeGroupIndex'

class CommitteeFolderIngestor(KnowledgeFolderIngestor):
    '''Committee Folder ingestion.'''
    def __call__(self):
        renderResults = super(CommitteeFolderIngestor, self).__call__()
        self.updateCollaborativeGroups()
        return renderResults
    def updateCollaborativeGroups(self):
        '''Update members of any matching collaborative groups'''
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        for committee in [i.obj for i in self.objects if i.obj.committeeType == 'Collaborative Group']:
            for collabGroup in [i.getObject() for i in catalog(object_provides=_collabGroup, Title=committee.title)]:
                members = []
                members.extend(committee.member)
                members.extend(committee.consultant)
                members.extend(committee.coChair)
                members.extend(committee.chair)
                collabGroup.setMembers(members)

class CommitteeHandler(IngestHandler):
    '''Handler for ``Committee`` objects.'''
    def createObjects(self, objectID, title, uri, predicates, statements, context):
        committee = context[context.invokeFactory('Committee', objectID)]
        updateObject(committee, uri, predicates, context)
        return [CreatedObject(committee)]

registerHandler(_committeeTypeURI, CommitteeHandler())
