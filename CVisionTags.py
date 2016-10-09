import http.client, urllib.request, urllib.parse, urllib.error, base64
import json


def GetImageInfo(img):
    conn = http.client.HTTPSConnection("api.projectoxford.ai")
    name="error"
    width=0
    i=0
    tag_name=""
    tags_array=[0]

    params = urllib.parse.urlencode({
    # Request parameters no need in this 
    'visualFeatures': 'Categories',
    'visualFeatures': 'Faces',
    'details': 'Celebrities',
    })

    headers = {
    'ocp-apim-subscription-key': "ee6b8785e7504dfe91efb96d37fc7f57",
    'content-type': "application/octet-stream"
    }

    conn.request("POST",  "/vision/v1.0/tag?%s" % params, img, headers)

    res = conn.getresponse()
    data = res.read()
    #print(data)   
    conn.close()
    string=b'name":"'   # строка поиска
    while data.find(string, width,len(data))!=-1:
       start=data.find(string, width,len(data))
       end=data.find(b'"',start+len(string),len(data))
       width=end
       #print(end)
       #i=i+1
       name=data[start+len(string):end]
       tag_name=''
       for i in range(len(name)):
           #print(chr(name[i]))
           tag_name=tag_name+chr(name[i])
       print("name "+ str(tag_name)+ " i " +str(i)+" start "+str(start) +" end " +str(end)+ " width "+str(width))
       tags_array.append(name)
    print (tags_array)
    print(data)
    return tags_array
    

