import requests
import json
import getpass
from requests.auth import HTTPBasicAuth
# asks for credentials and version name
print("you need to enter credentials\n")
u_name= input("enter username: ")
print("\n")
password= getpass.getpass("enter password: ")
org_name= input("enter your organization name")    
def tasks():
    task= input("press 1 to create a shared flow or any other number to process already existing shared flows")
    if task== '1':
        version()
    else:
        access()
# creating a version
def version():
    revision_name= input("enter the shared flow name you want to create: ")
    params=(
    ('action','import'),
    ('name', revision_name),)
        files= {
    'file':('1.zip',open('C:/Users/1439516/Downloads/zip_files/1.zip','rb')),
    }
    response= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/sharedflows",params=params,files=files,auth= HTTPBasicAuth(u_name,password))
    if response.ok:
        
        r_dict= json.loads(response.text)
        print("Created successfully")
        #print(r_dict)
    else:
        response.raise_for_status()
    choice= input("Press 1 to create more shared flows or 2 to access already existing shared flows")
    if choice =='1':
        version()
    if choice=='2':
        access()
    else:
        print("exiting")
# accessing already existing shared flows
def access():
        s_details= input("enter the name of required shared flow: ")
        res1= requests.get("https://api.enterprise.apigee.com/v1/o/"+org_name+"/sharedflows/"+s_details+"/deployments",auth= HTTPBasicAuth(u_name,password))
        if res1.ok:
            print("ok")
        else:
            res1.raise_for_status()
        res1_dict= json.loads(res1.text)
        if(res1_dict['environment']==[]):
            print("No deployments. Deploying 'test' environment to revision 1")
            revision1= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/environments/test/sharedflows/"+s_details+"/revisions/1/deployments", auth=HTTPBasicAuth(u_name,password))
            if revision1.ok:
                print("deployed revision 1")
            else:
                revision1.raise_for_status()
        else:
            for doc in res1_dict['environment']:
                for rev in doc['revision']:
                    for nm in rev['name']:
                        print(nm)
            print("the latest deployed revision is "+nm)
            nm_int1=int(nm)
            nm_int= int(nm)
            for doc1 in res1_dict['environment']:
                for rev1 in doc['revision']:
                    for nm1 in rev['name']:
                        if nm1!= (nm_int+1):
                                print("no further revisions. Creating one.....")
                                params1= (('action','import'),('name',s_details),)
                                files= {
                                 'file':('1',open('C:/Users/1439516/Downloads/zip_files/1.zip','rb')),
    }
                                further_response= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/sharedflows",params=params1,files=files,auth= HTTPBasicAuth(u_name,password))
                                if further_response.ok:
                                    print("created further revision to deploy")
                                else:
                                    further_response.raise_for_status()
                        else:
                            print("redirecting to deploy....")
        #undeploying latest version
            res2= requests.delete("https://api.enterprise.apigee.com/v1/o/"+org_name+"/environments/test/sharedflows/"+s_details+"/revisions/"+nm+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if res2.ok:
                print("undeployed "+nm)
            else:
                res2.raise_for_status()
       
            int_nm1= int(nm)
#deploying a new version
            res3= requests.post("https://api.enterprise.apigee.com/v1/o/"+org_name+"/environments/test/sharedflows/"+s_details+"/revisions/"+str(int_nm1+1)+"/deployments", auth=HTTPBasicAuth(u_name,password))
            if res3.ok:
                   print("deployed new version 'test' to revision "+str(int_nm1+1))
            else:
                    res3.raise_for_status()
        continue_choice= input("enter 1 to continue or 2 to create shared flow ")
        if continue_choice=='1':
                access()
        if continue_choice=='2':
                version()
        else:
                print("exiting")
       
if __name__=="__main__":
    tasks()
