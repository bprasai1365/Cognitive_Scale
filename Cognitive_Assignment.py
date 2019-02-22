# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 16:42:29 2019
Bigal Prasai 
@author wzyq2r
"""


import unittest
import json
import os
import requests
class test(unittest.TestCase):

#    
    #adding Authetication 
    def Authentication(self):
        
        user = "username"
        passwd = "password"
        url = "https://api.github.com/basic-auth/user/passwd"
        auth_values = (user, passwd)
        response = requests.get(url, auth=auth_values)
         
        # Convert JSON to dict and print
        print(response.json())
        if (response.status_code != 200) : assert False, "Ivalid login credenatial"
    
    
    
    def test_total_pulls(self):
        response = requests.get('https://api.github.com/repos/openconfig/public/pulls')
        print(response.text)
        print (response.status_code)
        if (response.status_code != 200) : assert False, "Status code mismatch"
        if (len(response.json()) != 8) : print ("Count does not match")
        
        
 
    def test_create_pull_request(self):
        #the POST request body can be created with jinja template
        payload = {"commit_id": "ecdd80bb57125d7ba9641ffaa4d7d2c19d3f3091",
                    "body": "Thank you- you have passed the test keep working hard and inovating !",
                     "event": "REQUEST_CHANGES",
                     "comments": [
                {
                      "path": "file.md",
                      "position": 6,
                      "body": "Please add more information here, and fix this typo."
                    }
                  ]
                }
        payload1 = json.dumps(payload)
        header = {'Accept' : 'application/vnd.github.symmetra-preview+json'}
        response = requests.post(url='https://api.github.com/repos/octocat/Hello-World/pulls/12/reviews/', data=payload1, headers=header, verify=False)
        print (response.text)
        print (response.status_code)
        if (response.status_code != 200): assert False, "create pull request failed"
        pull_request_response = json.loads(response.text)
        pull_request_id = pull_request_response["id"]
        commit_id = pull_request_response["commit_id"]
        if pull_request_id is None :
            assert False, "create pull request failed. no ID created"
        else :
            print ("Pull request ID :"+pull_request_id)
        if (commit_id is None) | (commit_id != "ecdd80bb57125d7ba9641ffaa4d7d2c19d3f3091"):
            assert False, "create pull request failed. commit ID not matching"
        else:
            print ("Pull request commit ID :" + commit_id)
        if pull_request_response["state"] != "CHANGES_REQUESTED" :
            assert False, ("create pull request failed. no state change. Current state :"+pull_request_response["state"])
   
        
        
        
if __name__ == "__main__":
     suite = unittest.TestSuite()
     suite.addTest(test('Authentication'))
     suite.addTest(test('test_total_pulls'))
     suite.addTest(test('test_create_pull_request'))
     
     unittest.TextTestRunner().run(suite)