# Quick start- How to run http_Client_hwTest.py

> python http_Client_hwTest.py -h

usage: http_Client_hwTest.py [-h] [-s HOST] [-p PORT] [-v]

The script would generate http request and check its corresponding response.

optional arguments:
  -h, --help            show this help message and exit
  -s HOST, --host HOST  host address.
  -p PORT, --port PORT  port number.
  -v, --verbose         show details about http response.

# Example:

HTTP request to 127.0.0.1:80. Only show error infomation.
> python http_Client_hwTest.py

HTTP request to 127.0.0.1:80. Show http response and error information.
> python http_Client_hwTest.py -v

HTTP request to 127.0.0.1:6659.
> python http_Client_hwTest.py -p 6659
