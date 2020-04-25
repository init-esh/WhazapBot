from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,JavascriptException
from selenium.common.exceptions import NoSuchElementException
import time
import base64
import os
import requests
from pyvirtualdisplay import Display
from flask import Flask, render_template,request
from threading import Thread
display = Display(visible=0, size=(1024, 600))

app = Flask(__name__)

def sendmsg(contact,text):
	try:
		delay=20
		input_box_search=driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')
		input_box_search.click()
		print("inp found")
		input_box_search.clear()
		input_box_search.send_keys(contact)
		time.sleep(2)
		myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@title='"+contact+"']")))
		selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
		selected_contact.click()
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]')))
		inp_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
		input_box = driver.find_element_by_xpath(inp_xpath)
		time.sleep(2)
		if type(text)==type(str()):
			input_box.send_keys(text + Keys.ENTER)
		elif type(text)==type(list()):
			for msg in text:
				input_box.send_keys(msg + Keys.ENTER)
		time.sleep(2)

		print("Msg Sent to "+contact)
	except TimeoutException:
		print("Timeout")
		driver.quit()
		display.stop()
	except NoSuchElementException:
		print("oo o not found")
		driver.quit()
		display.stop()


def loadui():
	delay=20
	print("Loading Your Whatsapp in background")
	try:
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')))
		print("Loaded...")
	except TimeoutException:
		print("Time Out Internet may be slow.")
		driver.quit()
		display.stop()
	except NoSuchElementException:
		print("Oho There is some error occur, Please try again")
		driver.quit()
		display.stop()

def autoreply():
	pass

def saveimg():
	try:
		canvas = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]')))
		canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
		canvas_png = base64.b64decode(canvas_base64)
		with open(r"./static/canvas.png", 'wb') as f:
			f.write(canvas_png)
	except TimeoutException:
		print("Time Out Internet may be slow.")
		driver.quit()
		display.stop()

def getbase64img():
	canvas = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]')))
	canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
	print(canvas_base64)
	

def checklogin():
	with open("./static/checkwalogin.txt","r") as f1:
		a=f1.read()
	if a=='No':
		return True
	else:
		return False

def initializefiles():
	if not os.path.exists("./geckodriver"):
		os.system("wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz")
		os.system("tar -xvzf geckodriver*")
		os.system("chmod +x geckodriver")
	tpath=os.getenv('PATH')
	os.environ['PATH'] = tpath+':./'
	if not os.path.exists("./static/"):
		print("Staic folder not exists creating it!")
		os.mkdir("static")
	else:
		print("static already exits")
	with open("./static/checkwalogin.txt","w") as f1:
		f1.write("No")
	if not os.path.exists("./templates"):
		print("templates folder not exists , creating it.")
		os.mkdir("templates")
	else:
		print("templates already exists")
	if not os.path.exists("./templates/index.html"):
		print("index.html not exists creating it.")
		with open("./templates/index.html","w") as f1:
			f1.write('<center><h1>Please hard refresh this page (refresh with shift key press)</h1><br><br><img src="/static/canvas.png"><br><br><br><form action="/result" method="POST"><input type="submit" name="submit"><h1>Click Once you scanned the code</h1></form></center>')
	else:
		print("indexfile already exists")

def getunreadmsg():
	query="""a=document.getElementsByClassName("OUeyt");
		var nii="";
		for(i=0;i<a.length;i++)
		{
		t=a[i].parentElement.parentElement.parentElement.parentElement.parentElement.firstElementChild.firstElementChild.innerText;
		n=a[i].parentElement.parentElement.parentElement.innerText;
		nii+=t+":"+n+",";
		}
		return nii"""
	res=driver.execute_script(query)
	print(res[:-1])

def getallcontact():
	try:
		query="""function fnCheckIfNumberFromCharIndex(str, charIndex){
		var currentIndex = charIndex+1;
		var num = "+";
		while(parseInt(str[currentIndex]) ||str[currentIndex] == 0 || fnIsCharIgnorable(str[currentIndex])){
		if(!fnIsCharIgnorable(str[currentIndex])){
		num+=str[currentIndex];
		}
		currentIndex++;
		}
		function fnIsCharIgnorable(char){
		var ignorable = ["", " ", "(", ")", "-"];
		if(ignorable.indexOf(char)>=0){
		return true;
		}
		return false;
		}
		return num;
		}
		function getAllIndexOf(str,char){
		var arr = [];
		var currentIndex =str.indexOf(char);
		var intLimit = 100;
		var limit=0;
		var prevCharIndex = 0;
		while(currentIndex >= 0 && currentIndex <= str.length && limit <= intLimit){
		currentIndex =str.indexOf(char,prevCharIndex+1);
		arr.push(currentIndex);
		prevCharIndex = currentIndex;
		limit++;
		}
		return arr;
		}
		function fnFindAllNumberFromString(str){
		var allNums = new Set();
		var aryIndexes = getAllIndexOf(str,'+');
		for(var index  in aryIndexes){
		var ci = aryIndexes[index];
		var currentNumber = fnCheckIfNumberFromCharIndex(str,ci);
		allNums.add(currentNumber);
		}
		return Array.from(allNums);
		}
		function fnFindIIOfPaneSide(){ 
		var paneSide = document.getElementById("pane-side");
		var IIName = "";
		for(p in paneSide){if(p.indexOf("reactInternal")>=0){ IIName=p; break;} }
		return paneSide[IIName];
		}
		function fnFindIIOfMain(){ 
		var main = document.getElementById("main");
		var IIName = "";
		for(p in main){if(p.indexOf("reactInternal")>=0){ IIName=p; break;} }
		return main[IIName];
		}
		function fnFindIIOfElement(element){
		if(!element){
		return null;
		}
		var IIName = "";
		for(p in element){if(p.indexOf("reactInternal")>=0){ IIName=p; break;} }
		return element[IIName];
		}
		function fnFindIIOfSide(){
		var side = document.getElementById("side");
		var IIName = "";
		for(p in side){if(p.indexOf("reactInternal")>=0){ IIName=p; break;} }
		return side[IIName];
		}
		function fnGetAllChats(){
		var paneII = fnFindIIOfPaneSide();
		if(!paneII){
		return;
		}
		return paneII.memoizedProps.children[0][0].props.chats;
		}
		function fnGetAllContacts(){
		var chats = fnGetAllChats();
		var ct = chats[0];
		if(!chats[0]){
		return;
		}
		return ct.contact.collection.models;
		}
		function fnFindGroupParticipentsArea(){
		var you =finda("You","span");
		if(!you){
		return null;
		}
		var element = you;
		while(element.parentElement.style.pointerEvents != "auto"){
		element = element.parentElement;
		if(!element.parentElement){
		break;
		return null;
		}
		}
		return element.parentElement;
		}
		window.WACEInterval = setInterval(function(){
		var paneSide = document.getElementById("side");
		var divWACEAllChats =document.getElementById("divWACEAllChats");
		if(paneSide && !divWACEAllChats){
		fnAddChatIconToPaneSide();
		}
		var divWACEAllGroupParticipants =document.getElementById("divWACEAllGroupParticipants");
		if(fnGetGroupParticipents() && !divWACEAllGroupParticipants){
		fnAddParticipantsIconToParticipantArea();
		}
		var divDisplay = document.getElementById("divDisplay");
		if(!divDisplay){
		fnAddDisplayPopup();
		}
		},1000);
		function fnClearInterval(){
		fnClearInterval(window.WACEInterval);
		}
		function onClickOfChats(){
		var allChats =fnGetAllChats();
		var lstContacts = [];
		for(var index in allChats){
		var chat = allChats[index];
		if(chat.isUser){
		lstContacts.push({
		number: chat.id.user,
		name: chat.name || "Unknown "+chat.id.user
		});
		}
		}
		return lstContacts;
		}
		function onClickOfContacts(){
		var allContacts = fnGetAllContacts();
		var myContacts = allContacts.filter(function(item){return item.isMyContact})
		var lstContacts = [];
		var nii="";
		for(var index in myContacts){
		var chat = myContacts[index];
		if(chat.isUser){
		lstContacts.push({
		number: chat.id.user,
		name: chat.name || "Unknown "+chat.id.user
		});
		var name=chat.name || "Unknown "+chat.id.user;
		nii+=chat.id.user+":"+name+",";
		}
		}
		return nii;
		}
		abc=onClickOfContacts();
		return abc;
		"""
		a=driver.execute_script(query)
		#result=driver.execute_script("onClickOfContacts();")
		print(a)
	except JavascriptException:
		print("Check Javascriptcode")
		driver.quit()
		display.stop()	



initializefiles()
#display.start()

driver = webdriver.Firefox()
#driver.set_window_size(1024, 600)
driver.get("https://web.whatsapp.com")
print("wait for your input, Goto localhost:5000 for more detail\n")
saveimg()

class FlaskThread(Thread):
    def run(self):
        app.run(
            host='127.0.0.1', port=5000, debug=True, use_debugger=True,
            use_reloader=False)


@app.route("/")
def index():
	return(render_template("index.html"))

@app.route("/result",methods=['GET','POST'])
def result():
	if request.method == "POST":
		with open("./static/checkwalogin.txt","w") as f1:
			f1.write("Yes")
	return "Successfully logged in to whatsapp server"

server = FlaskThread()
server.daemon = True
server.start()
print("Waiting for for your click")
while checklogin():
	saveimg()
	time.sleep(10)
	print("i am in a loop waiting for your input....\n")

print("Logged In")



#test("Kishan Falna",["1234787878787878787878","test two","test 3","test 7","8","9","10"])
loadui()
getunreadmsg()
getallcontact()
driver.quit()
#display.stop()