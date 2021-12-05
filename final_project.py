#!/usr/bin/python37all
import cgi
import json
from urllib.request import urlopen
from urllib.parse import urlencode

# html page format
html = """Content-type: text/html

<html>
<head>
<style>
<link type="text/css" rel="stylesheet" href="/usr/FinalProject/styles.css" />
</style>
</head>

<body>

<center>
<img src="/usr/FinalProject/image.jpg" alt="test image" width="500" height="333">
</center>
<br>

<div class="tab">
  <button class="tablinks" onclick="clickHandle(event, 'normal')">Normal Mode</button>
  <button class="tablinks" onclick="clickHandle(event, 'rapid')">Rapid Mode</button>
</div>

<div id="normal" class="tabcontent">
	<p>Current Angle: </p>
  <p>Enter Desired Angle: </p>
  <br>
  <p>Current Position: </p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
</div>

<div id="rapid" class="tabcontent">
  <p>No Position Set</p> 
</div>

<div id="step" class="tabcontent">
  <p>Current Angle: </p>
  <p>Enter Desired Angle: </p>
  <br>
  <p>Current Position: </p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "step" value = "left step">
    <input type = "submit" name = "step" value = "right step">
  </form>
</div>

<div id="position" class="tabcontent">
  <p>Current Angle: </p>
  <p>Enter Desired Angle: </p>
  <br>
  <p>Current Position: </p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "position">
    <input type = "submit" value = "adjust">
  </form>
</div>

<script>
function clickHandle(event, mode) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(mode).style.display = "block";
  event.currentTarget.className += " active";
}
</script>
   
</body>
</html>
"""
print(html)