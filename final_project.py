#!/usr/bin/python37all
from jinja2 import Template
# note jinja2 is used such that the css {} does not interfere with the print format
import cgi
import json
import time

# parse the data into json format
data = cgi.FieldStorage()
output = {}
step = data.getvalue('step')
inputPos = data.getvalue('position')
inputAngle = data.getvalue('angle')
posSet = data.getvalue('set position')
image = data.getvalue('image')
imageIndex = data.getvalue('image index')
lastImageIndex = data.getvalue('last image index')
auto = data.getvalue('auto')
takeImage = data.getvalue('take image')
init = data.getvalue('init')
detect = data.getvalue('detect')

# immediate inputs that can be outputted 
output['step'] = step
output['inputPos'] = inputPos
output['inputAngle'] = inputAngle
output['posSet'] = posSet
output['auto'] = auto
output['takeImage'] = takeImage
output['detect'] = detect

# check if the html page is just initialized to determine how the previous relevant data is obtained
if init == '1':
  prevData = {'displayAngle':"0", 'displayPos':"0", 'displaySetPos':"0", 'displaySetAngle':"0"}
else:
  with open('final_project.txt', 'r') as fin:
    prevData = json.load(fin)

# initialize the tab to stay on and values being displayed
normalTab = ""
autoTab = ""
stepTab = ""
posTab = ""
distance = "No Object Detected"
displayAngle = prevData['displayAngle']
displayPos = prevData['displayPos']
displaySetPos = prevData['displaySetPos']
displaySetAngle = prevData['displaySetAngle']

# if the user is trying to browse the gallery
if image != None:
  normalTab = "defaultMode"
  # for previous image
  if image == 'prev image':
    if int(imageIndex)-1 < 1:
      imageIndex = lastImageIndex
    else:
      imageIndex = str(int(imageIndex) - 1)
  # for next image
  elif image == 'next image':
    if int(imageIndex)+1 > int(lastImageIndex):
      imageIndex = str(1)
    else:
      imageIndex = str(int(imageIndex) + 1)
  # for last image
  else:
    imageIndex = lastImageIndex
# if the user is trying to take an image
elif takeImage != None:
  normalTab = "defaultMode"
  lastImageIndex = str(int(lastImageIndex) + 1)
# if the user is trying to step left or right with the camera
elif step != None:
  normalTab = "defaultMode"
  stepTab = "defaultStep"
  displayAngle = prevData['displayAngle']
  if step == 'left step':
    inputPos = str(int(prevData['displayPos']) - 1)
  else:
    inputPos = str(int(prevData['displayPos']) + 1)
  output['inputPos'] = inputPos
  displayPos = inputPos
# if the user is adjusting postion through the position adjustment button
elif inputPos != None:
  normalTab = "defaultMode"
  posTab = "defaultStep"
  displayPos = inputPos
# if the user is adjusting angle through the angle adjustment button
elif inputAngle != None:
  normalTab = "defaultMode"
  displayAngle = inputAngle
# if the user is operating on the auto tab
else:
  autoTab = "defaultMode"
  if posSet == 'set position':
    displaySetPos = prevData['displayPos']
    displaySetAngle = prevData['displayAngle']
  elif auto == 'auto':
    lastImageIndex = str(int(lastImageIndex) + 10)
  else:
    displaySetPos = prevData['displaySetPos']
    displaySetAngle = prevData['displaySetAngle']

# determine what the display angle and position should be
output['displaySetAngle'] = displaySetAngle
output['displaySetPos'] = displaySetPos
output['displayPos'] = displayPos
output['displayAngle'] = displayAngle

# dump the parsed data
with open('final_project.txt', 'w') as fout:
  json.dump(output,fout)

# if the user is trying to detect the distance, wait until the background python code measures the distance then take it from the json file and set the display of distance to that
while detect == 'detect':
  with open('final_project.txt', 'r') as fin:
    data = json.load(fin)
    detect = data['detect']
    if detect != 'detect':
      distance = "Object Detect: " +  str(int(float(data['detect']))) + "mm"


# html page format
html = Template("""Content-type: text/html

<html>
<head>
<style>
body {font-family: Arial;}

/* Style the tab */
.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons inside the tab */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
  font-size: 17px;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}
</style>
</head>

<body>

<center>
<h2>Video Stream</h2>
<iframe src="http://192.168.0.210:8082" width = "700" height = "600" title="video"></iframe>
<br>
<br>
<h2>Image Gallery</h2>
<img src="http://192.168.0.210/{{imageIndex}}.jpg" alt="test image" width="500" height="333">
<br>
<form action="/cgi-bin/final_project.py" method="POST">
  <input type = "submit" name = "image" value = "prev image">
  <input type = "submit" name = "image" value = "next image">
  <input type = "submit" name = "image" value = "last image">
  <input type = "hidden" name = "image index" value = {{imageIndex}}>
  <input type = "hidden" name = "last image index" value ={{lastImageIndex}}>
  <input type = "hidden" name = "init" value = "0">
</form>
</center>
<br>

<div class="tab">
  <button class="tablinks" onclick="clickHandle(event, 'normal')" id={{normalTab}}>Normal Mode</button>
  <button class="tablinks" onclick="clickHandle(event, 'auto')" id={{autoTab}}>Auto Mode</button>
</div>

<div id="normal" class="tabcontent">
  <p>Take an Image</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "image" src = "http://192.168.0.210/camera.jpg" alt = "Submit" width = "100" height = "100">
    <input type = "hidden" name = "take image" value = "1">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0">
  </form>
	<p>Current Angle (from 0 to 360): {{ang}} </p>
  <p>Enter Desired Angle: </p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "angle">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0">
  </form>
  <br>
  <p>Current Position (from 0 to 45): {{pos}}</p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step') "id={{stepTab}}>Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')" id={{posTab}}>Adjust By Position</button>
  </div>
</div>

<div id="auto" class="tabcontent">
  <p>Position Set (position, angle): {{setPos}}, {{setAngle}}</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "set position" value = "set position">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "auto" value = "auto">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0">
  </form>
  <br>
  <p>{{distance}}</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "detect" value = "detect">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form> 
</div>

<div id="step" class="tabcontent">
  <p>Take an Image</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "image" src = "http://192.168.0.210/camera.jpg" alt = "Submit" width = "100" height = "100">
    <input type = "hidden" name = "take image" value = "1">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form>
  <p>Current Angle (from 0 to 360): {{ang}} </p>
  <p>Enter Desired Angle: </p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "angle">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form>
  <br>
  <p>Current Position (from 0 to 45): {{pos}} </p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "step" value = "left step">
    <input type = "submit" name = "step" value = "right step">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form>
</div>

<div id="position" class="tabcontent">
  <p>Take an Image</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "image" src = "http://192.168.0.210/camera.jpg" alt = "Submit" width = "100" height = "100">
    <input type = "hidden" name = "take image" value = "1">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form>
  <p>Current Angle (from 0 to 360): {{ang}} </p>
  <p>Enter Desired Angle: </p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "angle">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
  </form>
  <br>
  <p>Current Position (from 0 to 45): {{pos}}</p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "position">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
    <input type = "hidden" name = "init" value = "0"> 
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

document.getElementById("defaultMode").click();
document.getElementById("defaultStep").click();
</script>

</body>
</html>
""")

html = html.render(
  normalTab=normalTab,
  autoTab=autoTab,
  stepTab=stepTab,
  posTab=posTab,
  ang=displayAngle,
  pos=displayPos,
  setPos=displaySetPos,
  setAngle=displaySetAngle,
  imageIndex=imageIndex,
  lastImageIndex=lastImageIndex,
  distance=distance
)
print(html)