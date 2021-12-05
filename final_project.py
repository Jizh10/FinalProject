#!/usr/bin/python37allimport cgi
import json
from urllib.request import urlopen
from urllib.parse import urlencode

# html page format
html = """Content-type: text/html

<html>
<head>
<style>
