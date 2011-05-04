# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
Testing base code.
'''

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc
import eke.knowledge.tests.base as ekeKnowledgeBase
import eke.site.tests.base as ekeSiteBase

# Traditional Products we have to load manually for test cases:
# (none at this time)

@onsetup
def setupEKECommittees():
    '''Set up additional products required.'''
    fiveconfigure.debug_mode = True
    import eke.committees
    zcml.load_config('configure.zcml', eke.committees)
    fiveconfigure.debug_mode = False
    ztc.installPackage('eke.site')
    ztc.installPackage('eke.committees')


setupEKECommittees()
ptc.setupPloneSite(products=['eke.committees'])

_twoCommitteesRDF = '''<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF xmlns:_3='http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#' xmlns:_4='http://purl.org/dc/terms/' 
    xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='http://usa.gov/data/committees/1'>
    <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Committee'/>
    <_4:title>Appropriations</_4:title>
    <_3:abbreviatedName>App</_3:abbreviatedName>
    <_3:committeeType>Committee</_3:committeeType>
    <_3:chair rdf:resource='http://pimpmyho.com/data/registered-person/3'/>
    <_3:coChair rdf:resource='http://pimpmyho.com/data/registered-person/1'/>
    <_3:consultant rdf:resource='http://pimpmyho.com/data/registered-person/3'/>
    <_3:member rdf:resource='http://pimpmyho.com/data/registered-person/3'/>
    <_3:member rdf:resource='http://pimpmyho.com/data/registered-person/2'/>
  </rdf:Description>
  <rdf:Description rdf:about='http://edrn.nci.nih.gov/data/committees/2'>
    <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Committee'/>
    <_4:title>Ways and Means</_4:title>
    <_3:committeeType>Committee</_3:committeeType>
  </rdf:Description>
</rdf:RDF>'''

_threeCommitteesRDF = '''<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF xmlns:_3='http://edrn.nci.nih.gov/xml/rdf/edrn.rdf#' xmlns:_4='http://purl.org/dc/terms/' 
    xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about='http://usa.gov/data/committees/1'>
    <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Committee'/>
    <_4:title>Appropriations</_4:title>
    <_3:abbreviatedName>App</_3:abbreviatedName>
    <_3:committeeType>Committee</_3:committeeType>
    <_3:chair rdf:resource='http://pimpmyho.com/data/registered-person/3'/>
    <_3:coChair rdf:resource='http://pimpmyho.com/data/registered-person/1'/>
    <_3:consultant rdf:resource='http://pimpmyho.com/data/registered-person/3'/>
    <_3:member rdf:resource='http://pimpmyho.com/data/registered-person/3'/>
    <_3:member rdf:resource='http://pimpmyho.com/data/registered-person/2'/>
  </rdf:Description>
  <rdf:Description rdf:about='http://usa.gov/data/committees/2'>
    <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Committee'/>
    <_4:title>Ways and Means</_4:title>
    <_3:committeeType>Committee</_3:committeeType>
  </rdf:Description>
  <rdf:Description rdf:about='http://usa.gov/data/committees/3'>
    <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Committee'/>
    <_4:title>Science and Technology</_4:title>
    <_3:committeeType>Committee</_3:committeeType>
  </rdf:Description>
</rdf:RDF>'''

def registerLocalTestData():
    ekeSiteBase.registerLocalTestData()
    ekeKnowledgeBase.registerTestData('/committees/a', _twoCommitteesRDF)
    ekeKnowledgeBase.registerTestData('/committees/b', _threeCommitteesRDF)

class BaseTestCase(ekeKnowledgeBase.BaseTestCase):
    '''Base for tests in this package.'''
    def setUp(self):
        super(BaseTestCase, self).setUp()
        registerLocalTestData()
    
# We use the one from eke.site because it installs a testing mail host,
# and when we ingest sites that mail host needs to be there.
class FunctionalBaseTestCase(ekeSiteBase.FunctionalBaseTestCase):
    '''Base class for functional (doc-)tests.'''
    def setUp(self):
        super(FunctionalBaseTestCase, self).setUp()
        registerLocalTestData()
    

