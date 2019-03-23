'''
Created on 23-Mar-2019

@author: Ammuty
'''
import requests
import json
import getpass
from requests.auth import HTTPBasicAuth

# Input parameters for deployment
u_name= 'user'
password= 'pwd'
org_name= 'org'
deploy_env='test'

#TODO: Pass environment as one of the parameter

def tasks():
        version()
        access()

# creating a version
def version():
    sflowName= 'security-sharedflow1'
    artifact_loc = "/Users/Ammuty/Downloads"
    params=(
    ('action','import'),
    ('name', sflowName))
    files= {
    'file':('security-sharedflow1',open('/Users/Ammuty/Downloads/security-sharedflow1.zip','rb')),
    }
    response= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/sharedflows",params=params,files=files,auth= HTTPBasicAuth(u_name,password))
    if response.ok:
        r_dict= json.loads(response.text)
        print("Created Sharedflow successfully")
    else:
        response.raise_for_status()

# accessing already existing shared flows
def access():
        s_details= 'security-sharedflow1'
        res1= requests.get("https://api.enterprise.apigee.com/v1/o/"+org_name+"/sharedflows/"+s_details+"/deployments",auth= HTTPBasicAuth(u_name,password))
        if res1.ok:
            print("ok")
        else:
            res1.raise_for_status()
        res1_dict= json.loads(res1.text)
        print('Response: '+res1.text)
        
        #If no deployments available for the sharedflow 
        if(res1_dict['environment']==[]):
            print("No deployments found for the Sharedflow. Deploying revision 1 to '"+deploy_env+"' environment")
            revision1= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/environments/"+deploy_env+"/sharedflows/"+s_details+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if revision1.ok:
                print("Current deployed Sharedflow revision"+revision1)
            else:
                revision1.raise_for_status()
        
        #Check the latest revision deployed already for the shared flow.
        #TODO: Handle needs to be changed for multi-environment situation
        else:
            for doc in res1_dict['environment']:
                for rev in doc['revision']:
                    nm = rev['name'];
                    print("The latest deployed revision is "+nm)
                    #for nm in rev['name']:
                        #print("the latest deployed revision is "+nm)
            

### Not sure why this piece of code is required ###
#             nm_int= int(nm)
#             for doc1 in res1_dict['environment']:
#                 for rev1 in doc['revision']:
#                     for nm1 in rev['name']:
#                         if nm1!= (nm_int+1):
#                                 print("no further revisions. Creating one.....")
#                                 params1= (('action','import'),('name',s_details))
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
            res2= requests.delete("https://api.enterprise.apigee.com/v1/o/"+org_name+"/environments/"+deploy_env+"/sharedflows/"+s_details+"/revisions/"+str(nm)+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if res2.ok:
                print("undeployed "+str(nm))
            else:
                res2.raise_for_status()
       
            int_nm1= int(nm)
            
            #Deploy a new version
            res3= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/environments/"+deploy_env+"/sharedflows/"+s_details+"/revisions/"+str(int_nm1+1)+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if res3.ok:
                print("Deployed new version to '"+deploy_env+"' env "+str(int_nm1+1))
            else:
                res3.raise_for_status()
       
if __name__=="__main__":
    tasks()
