'''
Created on 23-Mar-2019

@author: Balaji M
'''
import requests
import json
import getpass
import os
from os.path import isfile, join
from requests.auth import HTTPBasicAuth

# Input parameters for deployment
u_name= 'user'
password= 'pass'
org_name= 'org'
deploy_env='test'
apigee_mgmtapi_baseurl='https://api.enterprise.apigee.com/v1/'

# Tasks to be executed
def tasks():
    #artifact_name='security-sharedflow1'
    #articat_loc='/Users/Ammuty/Downloads/security-sharedflow1.zip'
    #createRevision(artifact_name,articat_loc)
    #deployRevision(artifact_name)
    
    shared_bundle_loc='/Users/Ammuty/Downloads/sharedflow/'
    proxy_bundle_loc='/Users/Ammuty/Downloads/apiproxy/'
    
    sharedZipFiles = [f for f in os.listdir(shared_bundle_loc) 
             if f.endswith(".zip")
                if isfile(join(shared_bundle_loc, f))
             ]
    for sharedZip in sharedZipFiles:
        artifact_name = sharedZip.split('.zip')[0]
        artifact_loc=shared_bundle_loc+sharedZip
        print('Artifact Name: '+artifact_name)
        print('Artifact Loc: '+artifact_loc)
        createRevision(artifact_name,artifact_loc)
        deployRevision(artifact_name)
    

# creating a version
#TODO: Iterate for multiple zip file
def createRevision(artifact_name,artifact_loc):
    #sflowName= 'security-sharedflow1'
    #artifact_loc = "/Users/Ammuty/Downloads"
    params=(
    ('action','import'),
    ('name', artifact_name))
    files= {
    'file':('security-sharedflow1',open(artifact_loc,'rb')),
    }
    response= requests.post(apigee_mgmtapi_baseurl+"/o/"+org_name+"/sharedflows",params=params,files=files,auth= HTTPBasicAuth(u_name,password))
    if response.ok:
        r_dict= json.loads(response.text)
        print("Created Sharedflow revision successfully")
    else:
        response.raise_for_status()

# accessing already existing shared flows
def deployRevision(artifact_name):
        #s_details= 'security-sharedflow1'
        res1= requests.get(apigee_mgmtapi_baseurl+"/o/"+org_name+"/sharedflows/"+artifact_name+"/deployments",auth= HTTPBasicAuth(u_name,password))
        if res1.ok:
            print("Existing deployment details fetched for: "+artifact_name);
        else:
            res1.raise_for_status()
        res1_dict= json.loads(res1.text)
        
        # Use only for debugging
        #print('Response: '+res1.text)
        
        #If no deployments available for the sharedflow 
        if(res1_dict['environment']==[]):
            print("No deployments found for the Sharedflow. Deploying revision 1 to '"+deploy_env+"' environment")
            revision1= requests.post(apigee_mgmtapi_baseurl+"/o/"+org_name+"/environments/"+deploy_env+"/sharedflows/"+artifact_name+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if revision1.ok:
                print("New Sharedflow revision created: "+revision1)
            else:
                revision1.raise_for_status()
        
        #Check the latest revision deployed already for the shared flow.
        #TODO: Handle needs to be changed for multi-environment situation
        else:
            for doc in res1_dict['environment']:
                for rev in doc['revision']:
                    nm = rev['name'];
                    print("The latest deployed revision already available "+nm)
                    #for nm in rev['name']:
                        #print("the latest deployed revision is "+nm)
            

### Not sure why this piece of code is required ###
#             nm_int= int(nm)
#             for doc1 in res1_dict['environment']:
#                 for rev1 in doc['revision']:
#                     for nm1 in rev['name']:
#                         if nm1!= (nm_int+1):
#                                 print("no further revisions. Creating one.....")
#                                 params1= (('action','import'),('name',artifact_name))
#                                 files= {
#                                  'file':('security-sharedflow1',open('/Users/Ammuty/Downloads/security-sharedflow1.zip','rb')),
#                                 }
#                                 further_response= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/sharedflows",params=params1,files=files,auth= HTTPBasicAuth(u_name,password))
#                                 if further_response.ok:
#                                     print("created further revision to deploy")
#                                 else:
#                                     further_response.raise_for_status()
#                         else:
#                             print("redirecting to deploy....")
###################################################
            
            # Undeploying latest version
            #nm = 12 #BYPASS
            res2= requests.delete(apigee_mgmtapi_baseurl+"/o/"+org_name+"/environments/"+deploy_env+"/sharedflows/"+artifact_name+"/revisions/"+str(nm)+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if res2.ok:
                print("undeployed "+str(nm))
            else:
                res2.raise_for_status()
       
            int_nm1= int(nm)
            
            #Deploy a new version
            res3= requests.post(apigee_mgmtapi_baseurl+"/o/"+org_name+"/environments/"+deploy_env+"/sharedflows/"+artifact_name+"/revisions/"+str(int_nm1+1)+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if res3.ok:
                print("Deployed new version to '"+deploy_env+"' env "+str(int_nm1+1))
            else:
                res3.raise_for_status()
       
if __name__=="__main__":
    tasks()
