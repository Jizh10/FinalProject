#!/usr/bin/python37all
from jinja2 import Template
import cgi
import json
from urllib.request import urlopen
from urllib.parse import urlencode

# parse the data into json format
data = cgi.FieldStorage()
output = {}
step = data.getvalue('step')
inputPos = data.getvalue('position')
inputAngle = data.getvalue('angle')
posSet = data.getvalue('set position')
image = data.getValue('image')
imageIndex = data.getValue('image index')
lastImageIndex = data.getValue('last image index')
auto = data.getValue('execute auto mode')
takeImage = data.getValue('take image')

output['step'] = step
output['inputPos'] = inputPos
output['inputAngle'] = inputAngle
output['posSet'] = posSet
output['auto'] = auto
output['takeImage'] = takeImage

with open('final_project.txt', 'r') as fin:
  prevData = json.load(fin)

normalTab = ""
autoTab = ""
stepTab = ""
posTab = ""
displayAngle = prevData['displayAngle']
displayPos = prevData['displayPos']
displaySetPos = prevData['displaySetPos']
displaySetAngle = prevData['displaySetAngle']

if image != None:
  if image == 'prev image':
    imageIndex = str(int(imageIndex) - 1)
  elif image == 'next image':
    imageIndex = str(int(imageIndex) - 1)
  else:
    imageIndex = lastImageIndex
elif image != None:
  normalTab = "defaultMode"
  lastImageIndex = str(int(lastImageIndex) + 1)
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
elif inputPos != None:
  normalTab = "defaultMode"
  posTab = "defaultStep"
  displayPos = inputPos
elif inputAngle != None:
  normalTab = "defaultMode"
  displayAngle = inputAngle
else:
  autoTab = "defaultMode"
  if posSet == 'set position':
    displaySetPos = prevData['displayPos']
    displaySetAngle = prevData['displayAngle']
  elif auto == 'execute auto mode':
    lastImageIndex = str(int(lastImageIndex) + 10)
  else:
    displaySetPos = prevData['displaySetPos']
    displaySetAngle = prevData['displaySetAngle']

output['displaySetAngle'] = displaySetAngle
output['displaySetPos'] = displaySetPos
output['displayPos'] = displayPos
output['displayAngle'] = displayAngle
with open('final_project.txt', 'w') as fout:
  json.dump(output,fout)

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
<img src="/usr/FinalProject/{{imageIndex}}.jpg" alt="test image" width="500" height="333">
<br>
<form action="/cgi-bin/final_project.py" method="POST">
  <input type = "submit" name = "image" value = "prev image">
  <input type = "submit" name = "image" value = "next image">
  <input type = "submit" name = "image" value = "last image">
  <input type = "hidden" name = "image index" value = {{imageIndex}}>
  <input type = "hidden" name = "last image index" value ={{lastImageIndex}}>
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
    <input type = "image" src = "camera.jpg" alt = "Submit" width = "100" height = "100">
    <input type = "hidden" name = "take image" value = "1">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}> 
  </form>
	<p>Current Angle (from 0 to 360): {{ang}} </p>
  <p>Enter Desired Angle: </p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "angle">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}>
  </form>
  <br>
  <p>Current Position (from 0 to 20): {{pos}}</p>
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
  </form>
  <br>
  <p>No Object Detected</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "detect" value = "detect">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {{lastImageIndex}}> 
  </form> 
</div>

<div id="step" class="tabcontent">
  <p>Take an Image</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "image" src = "camera.jpg" alt = "Submit" width = "100" height = "100">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {lastImageIndex}}> 
  </form>
  <p>Current Angle (from 0 to 360): {{ang}} </p>
  <p>Enter Desired Angle: </p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "angle">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {lastImageIndex}}> 
  </form>
  <br>
  <p>Current Position (from 0 to 20): {{pos}} </p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "submit" name = "step" value = "left step">
    <input type = "submit" name = "step" value = "right step">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {lastImageIndex}}> 
  </form>
</div>

<div id="position" class="tabcontent">
  <p>Take an Image</p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "image" src = "camera.jpg" alt = "Submit" width = "100" height = "100">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {lastImageIndex}}> 
  </form>
  <p>Current Angle (from 0 to 360): {{ang}} </p>
  <p>Enter Desired Angle: </p>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "angle">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {lastImageIndex}}> 
  </form>
  <br>
  <p>Current Position (from 0 to 20): {{pos}}</p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step')">Adjust By Step</button>
    <button class="tablinks" onclick="clickHandle(event, 'position')">Adjust By Position</button>
  </div>
  <br>
  <form action="/cgi-bin/final_project.py" method="POST">
    <input type = "text" name = "position">
    <input type = "submit" value = "adjust">
    <input type = "hidden" name = "image index" value = {{imageIndex}}>
    <input type = "hidden" name = "last image index" value = {lastImageIndex}}> 
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
  lastImageIndex=lastImageIndex
)
print(html)