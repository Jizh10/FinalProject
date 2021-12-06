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
position = data.getvalue('position')
output['step'] = step
output['position'] = position

with open('final_project.txt', 'w') as f:
  json.dump(output,f)

normalTab = "defaultMode"
# rapidTab = "2"
stepTab = "defaultStep"
# posTab = "4"


# if step != None:
#   normalTab = "defaultMode"
#   stepTab = "defaultStep"
# elif position != None:
#   normalTab = "defaultMode"
#   posTab = "defaultStep"
# else:
#   rapidTab = "defaultMode"


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
<img src="/usr/FinalProject/image.jpg" alt="test image" width="500" height="333">
</center>
<br>

<div class="tab">
  <button class="tablinks" onclick="clickHandle(event, 'normal')" id={{normalTab}}>Normal Mode</button>
  <button class="tablinks" onclick="clickHandle(event, 'rapid')">Rapid Mode</button>
</div>

<div id="normal" class="tabcontent">
	<p>Current Angle: </p>
  <p>Enter Desired Angle: </p>
  <br>
  <p>Current Position: </p>
  <div class="tab">
    <button class="tablinks" onclick="clickHandle(event, 'step') id={{stepTab}}">Adjust By Step</button>
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

document.getElementById("defaultMode").click();
document.getElementById("defaultStep").click();
</script>

</body>
</html>
""")

html = html.render(
  normalTab=normalTab,
  stepTab=stepTab
)
print(html)