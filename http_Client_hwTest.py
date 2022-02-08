import http.client
import logging
from email.utils import parsedate_to_datetime
from http.cookiejar import http2time
from operator import truediv
import argparse

parser = argparse.ArgumentParser(description="The script would generate http request and check its corresponding response.")
parser.add_argument('-s',"--host", help="host address.", type=str,default="127.0.0.1")
parser.add_argument('-p',"--port", help="port number.", type=int,default=80)
parser.add_argument('-v',"--verbose", help="show details about http response.",action='count',default=0)
args = parser.parse_args()

if args.verbose==0:
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s]: %(message)s')
else:
    logging.basicConfig(level=logging.NOTSET, format='[%(asctime)s - %(levelname)s]: %(message)s')


def check_httpver(httpver):
    if httpver==11:
        return True
    else:
        logging.error("Http version in response is "+str(httpver/10)+". Please use HTTP/1.1 protocol instead.")
        return False

def check_httpstatus(response_code,httpcode):
    if response_code==httpcode:
        return True
    else:
        logging.error("Http status code in response is "+str(response_code)+". However we expect "+str(httpcode)+" instead.")
        return False


def check_httpheader(response):
    def get_httpheader(response, param_name):
        param_value= response.getheader(param_name)
        if param_value!=None:
            return param_value
        else:
            logging.error("Http headers in response do not include \""+param_name +"\".")
            return param_value
    def check_date_format(datestring):
        if http2time(datestring)!=None:
            return True
        else:
            logging.error("Wrong format in date_string:" + datestring+". Please Use the date/time format RFC 7231 (https://www.rfc-editor.org/rfc/rfc7231#section-7.1.1.1)")
            return False
        
    http_header_Server=get_httpheader(response,"Server")
    http_header_LastModified=get_httpheader(response,"Last-Modified")
    http_header_ContentLength=get_httpheader(response,"Content-Length")
    http_header_Date=get_httpheader(response,"Date")
    check_date_format(http_header_Date)

def check_httpbody(response,filepath):
    responseBody=response.read()
    if filepath==None:
        if len(responseBody)==0:
            return True
        else:
            logging.error("Response should not have a body")
    else:
        f = open(filepath,"r",encoding="utf-8")
        html_str= f.read()
        responseBody_str=responseBody.decode("utf-8")
        if responseBody_str==html_str:
            return True
        else:
            logging.error("Unexpected Http response Body. Please check your response body.")
            return False


# GET METHODOLGY Check
logging.info("Send GET Reqeust.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("GET","/")
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,200)
check_httpheader(response)
check_httpbody(response,"index.html")

# HEAD Methodology Test
logging.info("Send HEAD Reqeust.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("HEAD","/")
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,200)
check_httpheader(response)
check_httpbody(response,None)

# If-Modified-Since Function Check: GET Methodology Test with "If-Modified-Since" header
logging.info("Send GET Reqeust with Header {If-Modified-Since:Fri, 04 Feb 2023 20:50:04 GMT}.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("GET","/",headers= {"If-Modified-Since":"Fri, 04 Feb 2023 20:50:04 GMT"})
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,304)
logging.info("Send GET Reqeust with Header {If-Modified-Since:Fri, 04 Feb 1999 20:50:04 GMT}.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("GET","/",headers= {"If-Modified-Since":"Fri, 04 Feb 1999 20:50:04 GMT"})
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,200)


# 400 Error: GET Methodology Test with "If-Modified-Since" header using wrong format for its value
logging.info("Send GET Reqeust with Header {If-Modified-Since:Fri, 04 Feb 1999 20:50:04 GM}.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("GET","/",headers= {"If-Modified-Since":"Fri, 04 Feb 2023 20:50:04 GM"})
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,400)

# 404 Error: GET Methodology Test with wrong uri
logging.info("Send GET Reqeust with {uri:/MissingResource}.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("GET","/MissingResource")
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,404)

# 501 Error: PUT Methodology Test
logging.info("Send PUT Reqeust.")
connection = http.client.HTTPConnection(args.host,args.port,timeout=10)
connection.request("PUT","/")
response = connection.getresponse()
logging.debug("Response (HTTP code + Header) from your server:\nHTTP/"+str(response.version/10)+ " "+str(response.status)+" "+str(response.reason)+"\r\n"+str(response.msg))
check_httpver(response.version)
check_httpstatus(response.status,501)



