
import os

#Importing the rdflib requirements
from rdflib import Graph,Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib.namespace import  RDF, RDFS
cwd=os.getcwd()




#importing the library to read the xml data
import xml.etree.ElementTree as ET

#Create a tree to get the XML data
tree = ET.parse('Shopping_Mall.xml')

root=tree.getroot()

shop_name = []
shop_number= []
floor_no = []
category_type = []

myNamespace="http://www.semanticweb.org/home/ontologies/2023/3/Shopping_Mall" #Namespace
namedIndividual = URIRef('http://www.w3.org/2002/07/owl#NamedIndividual') #namedIndividual

#for element in root.findall()
for child in root:
    #print("outside",child, type(child))
    if(child.tag == 'building'):
        #print("inside",child, type(child))
        for child1 in child:
            if(child1.tag == 'floor'):
                for child2 in child1:
                    if(child2.tag=='Shops'):

                        for element in child1.findall(child2.tag+'/shop_name'):
                            shop_name.append(element.text.strip())
                        for element in child1.findall(child2.tag+'/shop_number'):
                            shop_number.append(element.text.strip())
                        for element in child1.findall(child2.tag+'/floor_no'):
                            floor_no.append(element.text.strip())
                        for element in child1.findall(child2.tag+'/category_type'):
                            category_type.append(element.text.strip())
shop_name1 = []
shop_number1 = []
floor_no1 = []
category_type1  = []
flag= 0
for i in shop_name:
    for j in shop_name1:
        if(i == j):
            flag = 1
    if(flag == 0):
        shop_name1.append(i)
    else:
        flag= 0
shop_name = shop_name1
for i in shop_number:
    for j in shop_number1:
        if(i == j):
            flag = 1
    if(flag == 0):
        shop_number1.append(i)
    else:
        flag= 0
shop_number = shop_number1
for i in floor_no:
    for j in floor_no1:
        if(i == j):
            flag = 1
    if(flag == 0):
        floor_no1.append(i)
    else:
        flag= 0
floor_no = floor_no1
for i in category_type:
    for j in category_type1:
        if(i == j):
            flag = 1
    if(flag == 0):
        category_type1.append(i)
    else:
        flag= 0
category_type = category_type1
print(shop_name)
print(shop_number)
print(floor_no)
print(category_type)

g=Graph()
g.parse("Assignment4rdf.rdf", format='xml')

print("OWL File Loaded")

exist = 1
#rdftype = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
def isAlreadyDefined(subject):
    for s in g.subjects():
        if(subject in str(s) and 1 == exist):
            return True
    return False

all_triplets=[]
object_properties=[]
attribute_properties=[]
index_no=[0]
newRDFTriples = []


#creating the role triplets for the customer - places - order
for index in range(len(shop_name)):
    individualName=str(myNamespace)+"#"+shop_name[index]
    arc_class=str(myNamespace)+"#"+"shop_name"
    arc_individual = URIRef(individualName)

    if(isAlreadyDefined(individualName)==False):
        all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
        newRDFTriples.append((arc_individual,RDF.type, URIRef(namedIndividual)))

        #Adding Data Properties - id,name,contact of the customer.
        subject=arc_individual
        pred= URIRef(str(myNamespace)+"#hasFloorNo")
        literal=floor_no[index]
        newRDFTriples.append((subject,pred, Literal(literal,datatype=XSD.string)))

        pred= URIRef(str(myNamespace)+"#category_type")
        literal=category_type[index]
        newRDFTriples.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))



for i in range(0,len(all_triplets),1):
    print(all_triplets[i])

print("----------------------------------------------")
for i in range(0,len(newRDFTriples),1):
    print(newRDFTriples[i])
    print('\n')
print("Total number of triples generated")
print(len(newRDFTriples))
g.serialize(destination="Assignment4rdf_final.rdf", format='xml')

from owlready2 import *
import rdflib
onto = get_ontology(cwd+"/Assignment4rdf.rdf").load()
with onto:
    sync_reasoner()
onto.save("Assignment4rdf_consistent.rdf")

g2=rdflib.Graph()
from rdflib.compare import to_isomorphic, graph_diff
g2.parse("Assignment4rdf_final.rdf", format='xml')

count = 0
for s,p,o in g2:
    print(" ",end=" ")
    count=count+1
iterator = 0
for i in range(20):
    iterator = 2
print("No of Triples Before the reasoner ->  " ,count)

g3=rdflib.Graph()
for i in range(20):
    iterator = 2
g3.parse("Assignment4rdf_consistent.rdf", format='xml')

count = 0
intial_condtion = True
for s,p,o in g3:
    count=count+1

print("No of Triples After :  " ,count)
#iso_1 ,iso2= to_isomorphic(g2),to_isomorphic(g3)
iso1 = to_isomorphic(g2)
print("completed iso1")
iso2 = to_isomorphic(g3)
if(iso1 == iso2 and intial_condtion == True):
    print("See the result")
    print("No Inferences found")
else:
    in_both, in_first, in_second = graph_diff(iso1,iso2)
    print(" New Inderences",end=" ")
    print("+",end=" ")
    print("All Inderences",end=" ")
    def helper(g,f,add,intial):
        for l in sorted(g.serialize(format='nt').splitlines()):
            if(l) :
                # print(l)
                f.write(l)
                f.write("\n")

    f = open("Allinferred.txt", "w")
    print("operation successful")
    helper(in_second, f,0,1)
    f.close()

    f = open("DATAinferred.txt", "w")

    helper(in_both, f,0,1)
    helper(in_second, f,0,1)
    f.close()
