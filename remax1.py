"""
REMAX code exercise.
"""

# Development environment:  Python 2.7 on OpenBSD 6.3.

import unittest

import urllib2
from xml.etree import ElementTree  
import pprint
import csv

# Booj's test data URL.
XMLURL = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
XMLFILE = 'remax.xml'

# For CSV processing types.
STRINGX = 'string'
LISTX = 'list'
TRUNCATEX = 'truncate'

# For doube quoting comma delimited lists.
DOUBLEQUOTE = chr(34)
# String constants.
EMPTYSTRING = ''
COMMA = ','

# Required Fields.
# Root node:
LISTINGS = 'Listings'

# Node for each listing.
LISTINGX = 'Listing'

# Header for MlsId and others.
LISTINGDETAILS = 'ListingDetails'
# Subfields.
MLSID = 'MlsId'
MLSNAME = 'MlsName'
DATELISTED = 'DateListed'
PRICE = 'Price'

# Header for StreetAddress we want (more than one in XML feed).
LOCATION = 'Location'
# Subfields.
STREETADDR = 'StreetAddress'

# Header for Bedrooms.
BASICDETAILS = 'BasicDetails'
# Subfields.
BEDROOMS = 'Bedrooms'
# Bathrooms are a weirdo field - no information, just a tag,
# followed by specific tags:
#
#     <FullBathrooms>4</FullBathrooms>
#     <HalfBathrooms>1</HalfBathrooms>
#     <ThreeQuarterBathrooms/>
BATHROOMS = 'Bathrooms'
FULLBATHROOMS = 'FullBathrooms'
HALFBATHROOMS = 'HalfBathrooms'
BATHROOM3QRTR = 'ThreeQuarterBathrooms'
DESCRIPTION = 'Description'

# Header for Appliances.
RICHDETAILS = 'RichDetails'
# Subfields.
ROOMS = 'Rooms'
# Sub-sub field.
ROOMX = 'Room'
APPLIANCES = 'Appliances'
# Sub-sub field.
APPLIANCEX = 'Appliance'

# For dictionary.
REQUIREDFIELDS = 'requiredfields'
HASSUBNODES = 'hassubnodes'
# The bathroom tag that is not a parent.
FAUXPARENT = 'fauxparent'

# Hierarchy within XML of required information.

                                                    # MLSId.
LISTINGSTRUCTURE = {LISTINGDETAILS:{REQUIREDFIELDS:[MLSID,
                                                    # MLSName.
                                                    MLSNAME,
                                                    # DateListed.
                                                    DATELISTED,
                                                    # Price.
                                                    PRICE],
                                    HASSUBNODES:{},
                                    FAUXPARENT:{}},
                                              # StreetAddress.
                    LOCATION:{REQUIREDFIELDS:[STREETADDR],
                              HASSUBNODES:{},
                              FAUXPARENT:{}},
                                                  # Bedrooms.
                    BASICDETAILS:{REQUIREDFIELDS:[BEDROOMS,
                                                  # Bathrooms.
                                                  BATHROOMS,
                                                  # Description.
                                                  DESCRIPTION], 
                                  HASSUBNODES:{},
                                  # Bathroom XML setup.
                                  FAUXPARENT:{BATHROOMS:[FULLBATHROOMS,
                                                         HALFBATHROOMS,
                                                         BATHROOM3QRTR]}},
                                                 # Rooms.
                    RICHDETAILS:{REQUIREDFIELDS:[ROOMS,
                                                 # Appliances.
                                                 APPLIANCES], 
                                              # Room subnodes.
                                 HASSUBNODES:{ROOMS:ROOMX,
                                              # Appliance subnodes.
                                              APPLIANCES:APPLIANCEX},
                                 FAUXPARENT:{}}}

# For fauxparent tag Bathrooms tag.
REALTAG = 'realtag'
NOTRELEVANT = 'not relevant'

CSVFIELDS = [MLSID,
             MLSNAME,
             DATELISTED,
             STREETADDR,
             PRICE,
             BEDROOMS,
             BATHROOMS,
             APPLIANCES,
             ROOMS,
             DESCRIPTION]

CSVPROCESSTYPE = {MLSID:STRINGX,
                  MLSNAME:STRINGX,
                  DATELISTED:STRINGX,
                  STREETADDR:STRINGX,
                  PRICE:STRINGX,
                  BEDROOMS:STRINGX,
                  BATHROOMS:FAUXPARENT,
                  APPLIANCES:LISTX,
                  ROOMS:LISTX,
                  DESCRIPTION:TRUNCATEX} 

# For filtering - not using regular expression.
#                 "and" is usually if not always
#                 bracketed by spaces.
ANDX = ' and '

# For truncating Description field.
TRUNCLEN = 200

# Assignment
# 
# Write a script to download and parse the given XML feed, manipulate some of the data, and deliver a CSV of the required fields. You may use any additional libraries that you wish, please include a requirements.txt if you do.
# CSV Requirements:
# 
#     1) Contains only properties listed from 2016 [DateListed]
#     2) Contains only properties that contain the word "and" in the Description field
#     3) CSV ordered by DateListed
#     4) Required fields:
#         a) MlsId
#         b) MlsName
#         c) DateListed
#         d) StreetAddress
#         e) Price
#         f) Bedrooms
#         g) Bathrooms
#         h) Appliances (all sub-nodes comma joined)
#         i) Rooms (all sub-nodes comma joined)
#         j) Description (the first 200 characters)
# 
# Technical Requirements
# 
#     5) Interpreter version: python 2.7
#     6) Reasonable unit test coverage
#     7) All libraries used must be documented in requirements.txt
#         We will be using pip install -r requirements.txt prior to running your code
#     8) Raw information to parse / feed url
#         http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml
#         a) This feed must be downloaded from with in the script, raw data must not be downloaded manually
# 
# Submission Requirements
# 
#     9) Work should be tracked with Git
#     10) Submit final product by submitting a pull request
# 
# Purpose
# 
# A lot of the work in our department is parsing and manipulating data from a variety of sources. The given example is one of our XML files that we send to Zillow for property syndication. Our goal in this test is to see how you will approach the processing of this feed. Your solution should take into the account that there will be other XML feeds that need parsing as well, so how modular/reusable you make the code is very important.
# 
# Time Considerations
# 
# This assignment is expect to take a few hours. We ask that you do not spend too much time on this solution. If you are stuck or have questions, feel free to reach out and we will answer quickly.

def getdatafromweb():
    """
    Grab data from website.

    Returns text.
    """
    print 'Connecting to page via urllib2 . . .'
    response = urllib2.urlopen(XMLURL)
    print 'Getting xml . . .'
    return response.read()

def writexmltofile(text):
    """
    Writes xml text to a file.
    """
    print 'Writing data from web to xml file locally . . .'
    with open(XMLFILE, 'w') as f:
        print >> f, text
        f.close()

def writeoutxmlstructure(root):
    """
    Write out data indented in a way
    that is easier to visualize than
    XML tagged data.

    root is an ElementTree object.
    """
    # Get feel for data structure / schema in XML.
    print 'Writing out XML structure to file . . .'
    with open('xmlstructure.txt', 'w') as f2:
        print >> f2, root.tag
        for n in xrange(len(root)):
            print >> f2, '    ' + root[n].tag
            for o in xrange(len(root[n])):
                print >> f2, '        ' + root[n][o].tag
                for p in xrange(len(root[n][o])):
                    print >> f2, '            ' + root[n][o][p].tag
                    # Get appliances (and rooms).
                    for q in xrange(len(root[n][o][p])):
                        print >> f2, '                ' + root[n][o][p][q].tag

def checkfauxparent(tagparent, tagsub):
    # Try to deal with bathrooms.
    if LISTINGSTRUCTURE[tagparent][FAUXPARENT]:
        # Get the real bathroom tags.
        # XXX - this should work here but would need to
        #       be worked out more rigorously if there
        #       were name collisions.
        realsubtags = []
        for subtagx in LISTINGSTRUCTURE[tagparent][FAUXPARENT]:
            # Put the real tags in a list.
            realsubtags.extend(LISTINGSTRUCTURE[tagparent][FAUXPARENT][subtagx])
        if tagsub in LISTINGSTRUCTURE[tagparent][FAUXPARENT]:
            # Not a useful tag, but a header, like Bathrooms.
            return FAUXPARENT
        elif tagsub in realsubtags:
            return REALTAG
    return NOTRELEVANT

def getdatafromxml(root, listingindex):
    # Inner loop of putessentialdataintodictionary.
    requireddata = {}
    for o in xrange(len(root[listingindex])):
        # LISTINGDETAILS, LOCATION, BASICDETAILS, RICHDETAILS.
        if root[listingindex][o].tag in LISTINGSTRUCTURE:
            tagparent = root[listingindex][o].tag
            for p in xrange(len(root[listingindex][o])):
                tagsub = root[listingindex][o][p].tag
                # Check for bathrooms fauxparent here.
                if checkfauxparent(tagparent, tagsub) == FAUXPARENT:
                    # Do nothing and deal with the header in the
                    # csv processing later.
                    continue
                elif checkfauxparent(tagparent, tagsub) == REALTAG:
                    # Stuff the bathroom tags in as is and deal with
                    # later in csv phase.
                    requireddata[tagsub] = root[listingindex][o][p].text
                if (tagsub in LISTINGSTRUCTURE[tagparent][REQUIREDFIELDS] and
                    tagsub not in LISTINGSTRUCTURE[tagparent][FAUXPARENT]):
                    if tagsub in LISTINGSTRUCTURE[tagparent][HASSUBNODES]:
                        quotedtexttojoin = []
                        for q in xrange(len(root[listingindex][o][p])):
                            tagsubsub = root[listingindex][o][p][q].tag
                            if tagsubsub == LISTINGSTRUCTURE[tagparent][HASSUBNODES][tagsub]:
                                quotedtexttojoin.append(root[listingindex][o][p][q].text)
                            requireddata[tagsub] = quotedtexttojoin
                    else:
                        requireddata[tagsub] = root[listingindex][o][p].text
    key = (requireddata[DATELISTED], requireddata[MLSID])                
    return key, requireddata

def putessentialdataintodictionary(root):
    """
    Gets essential data for the assignment
    into a dictionary keyed on MLSId.

    root is an ElementTree object.

    Returns a dictionary.
    """
    numlistings = 0
    listings = {}
    # Check that Listings is top node.
    if root.tag == LISTINGS:
        for listingindex in xrange(len(root)):
            # Individual listing.
            if root[listingindex].tag == LISTINGX:
                numlistings += 1
                key, requireddata = getdatafromxml(root, listingindex)
                listings[key] = requireddata
    print 'Number of listings = {0:d}'.format(numlistings)
    return listings

def filterlistings(listings):
    # listings is the dictionary of listings.
    # Listings from 2016.
    # key is a two tuple with the date string first.
    filtered = {key:listings[key] for key in listings
                if key[0][:4] == '2016' and
                   listings[key][DESCRIPTION].find(ANDX) > -1}
    return filtered

def findfauxparentfields(fauxparent):
    # Addresses bathroom thing.
    # Returns list.
    # Brute force traverse.
    for tagparent in LISTINGSTRUCTURE:
        # XXX - if there are multiple name collisions,
        #       this will cause problems.  OK for now.
        if (LISTINGSTRUCTURE[tagparent][FAUXPARENT] and
            fauxparent in LISTINGSTRUCTURE[tagparent][REQUIREDFIELDS]):
            return LISTINGSTRUCTURE[tagparent][FAUXPARENT][fauxparent]
    return []

def processcsvrecord(requireddata):
    # requireddata is a dictionary.
    datax = []
    for fieldx in CSVFIELDS:
        # Everything is a string except
        # rooms, appliances, and bathrooms.
        # Description needs to be truncated.
        #
        # Put in missing data for processing.
        if (fieldx not in requireddata and
            CSVPROCESSTYPE[fieldx] != FAUXPARENT):
            if CSVPROCESSTYPE[fieldx] in (STRINGX, TRUNCATEX):
                requireddata[fieldx] = EMPTYSTRING
            elif CSVPROCESSTYPE[fieldx] == LISTX:
                requireddata[fieldx] = []
        if CSVPROCESSTYPE[fieldx] == STRINGX:
            datax.append(requireddata[fieldx])
        elif CSVPROCESSTYPE[fieldx] == TRUNCATEX:
            datax.append(requireddata[fieldx][:TRUNCLEN])
        elif CSVPROCESSTYPE[fieldx] == LISTX: 
            # Double quoted comma delimited list.
            strx = DOUBLEQUOTE + COMMA.join(requireddata[fieldx]) + DOUBLEQUOTE
            datax.append(strx)
        elif CSVPROCESSTYPE[fieldx] == FAUXPARENT:
            subfields = findfauxparentfields(fieldx)
            # Order of subfields hard coded in LISTINGSTRUCTURE.
            joinedlist = []
            for subfieldx in subfields:
                # XXX - str() will put None in for bathrooms that don't
                #       exist - not sure if that is what is desired.
                joinedlist.append(subfieldx + ':' + str(requireddata[subfieldx]))
            strx = DOUBLEQUOTE + COMMA.join(joinedlist) + DOUBLEQUOTE
            datax.append(strx)
    return datax

def writetocsv(filteredlistings):
    # filteredlistings is a dictionary.
    # Sort on date listed, then MLSId.
    counter = 0
    sortedkeys = sorted([key for key in filteredlistings])
    with open('solution.csv', 'w') as f:
        writerx = csv.writer(f)
        writerx.writerow(CSVFIELDS)
        for key in sortedkeys:
            counter += 1
            if counter % 10 == 0:
                print 'Wrote {0:03d} records to csv.'.format(counter)
            linex = processcsvrecord(filteredlistings[key])
            writerx.writerow(linex)

def workproblem():
    # Wrapper.
    text = getdatafromweb()
    # Not essential but helpful for debugging.
    writexmltofile(text)
    # Not part of required solution, but key
    # to getting solution set up and useful
    # for debugging.
    root = ElementTree.fromstring(text)
    writeoutxmlstructure(root)
    listings = putessentialdataintodictionary(root)
    print 'Writing dictionary of listings to file . . .'
    with open('listingsdictionary.py', 'w') as f3:
        pprint.pprint(listings, stream=f3)
    print 'Filtering listings . . .'
    filteredlistings = filterlistings(listings)
    print 'Writing dictionary of filtered listings to file . . .'
    with open('listingsdictionaryfiltered.py', 'w') as f3:
        pprint.pprint(filteredlistings, stream=f3)
    writetocsv(filteredlistings)

class TestXMLRealtorScript(unittest.TestCase):
    def testxmlgrab(self):
        # Does data show up from urllib2 call.
        self.assertTrue(getdatafromweb())
    def testcheckfauxparent(self):
        # Test tricky part of data structure (the bathrooms).
        self.assertEquals(checkfauxparent(BASICDETAILS, HALFBATHROOMS), REALTAG)
        self.assertEquals(checkfauxparent(BASICDETAILS, BATHROOMS), FAUXPARENT)
        self.assertEquals(checkfauxparent(RICHDETAILS, ROOMS), NOTRELEVANT)
    def testlookupdictionaryintegrity(self):
        # Make sure "constant" dictionary and list setups are as intended.
        self.assertEquals(LISTINGSTRUCTURE[LOCATION][HASSUBNODES], {})
        self.assertEquals(LISTINGSTRUCTURE[LOCATION][REQUIREDFIELDS][0], STREETADDR)
        self.assertEquals(LISTINGSTRUCTURE[BASICDETAILS][REQUIREDFIELDS][1], BATHROOMS)
        self.assertEquals(LISTINGSTRUCTURE[RICHDETAILS][REQUIREDFIELDS][1], APPLIANCES)
        self.assertEquals(LISTINGSTRUCTURE[RICHDETAILS][HASSUBNODES][APPLIANCES], APPLIANCEX)
        self.assertEquals(CSVFIELDS[6], BATHROOMS)
        self.assertEquals(CSVPROCESSTYPE[DATELISTED], STRINGX)
        self.assertEquals(CSVPROCESSTYPE[APPLIANCES], LISTX)
        self.assertEquals(CSVPROCESSTYPE[DESCRIPTION], TRUNCATEX)
    def testfilter(self):
        # Test the listing filter.
        badlistings1 = {('2016-07-04', 'xxxx'):{DESCRIPTION:'blah'}}
        badlistings2 = {('2014-07-04', 'xxxx'):{DESCRIPTION:' and '}}
        goodlistings = {('2016-07-04', 'xxxx'):{DESCRIPTION:' and '}}
        self.assertEquals(filterlistings(badlistings1), {})
        self.assertEquals(filterlistings(badlistings2), {})
        self.assertEquals(filterlistings(goodlistings), goodlistings)
    def testfindfauxparentfields(self):
        self.assertEquals(findfauxparentfields(BATHROOMS), [FULLBATHROOMS,
                                                            HALFBATHROOMS,
                                                            BATHROOM3QRTR])
        self.assertEquals(findfauxparentfields(STREETADDR), [])


if __name__ == '__main__':
    # unittest.main()
    workproblem()
