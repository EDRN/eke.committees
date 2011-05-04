# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Committees: RDF ingest for Committee Folders and their Committees.
'''

from eke.knowledge.browser.rdf import KnowledgeFolderIngestor, CreatedObject, registerHandler, IngestHandler
from eke.knowledge.browser.utils import updateObject
from rdflib import URIRef

_committeeTypeURI = URIRef('http://edrn.nci.nih.gov/rdf/types.rdf#Committee')

class CommitteeFolderIngestor(KnowledgeFolderIngestor):
    '''Committee Folder ingestion.'''

class CommitteeHandler(IngestHandler):
    '''Handler for ``Committee`` objects.'''
    def createObjects(self, objectID, title, uri, predicates, statements, context):
        committee = context[context.invokeFactory('Committee', objectID)]
        updateObject(committee, uri, predicates, context)
        return [CreatedObject(committee)]

registerHandler(_committeeTypeURI, CommitteeHandler())
