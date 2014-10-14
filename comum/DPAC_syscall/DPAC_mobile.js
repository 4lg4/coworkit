/*
	- DPAC Mobile (Done Packages Mobile) 
	- Data: 21-07-2012 
	- Local: http://eos.done.com.br/DPAC_mobile/ 
*/

/* include JS file asynchronous */
function include(file)
	{
	var xhrObj = new XMLHttpRequest();
	
	// open and send a synchronous request
	xhrObj.open('GET', file, false);
	xhrObj.send('');
	
	// add the returned content to a newly created script tag
	var se = document.createElement('script');
	se.type = "text/javascript";
	se.text = xhrObj.responseText;
	document.getElementsByTagName('head')[0].appendChild(se);
	}

// include JS file asynchronous 	
function loadJS(file)
	{
	var fileref = document.createElement('script');
	fileref.setAttribute("type","text/javascript");
	fileref.setAttribute("src", file);

	document.getElementsByTagName("head")[0].appendChild(fileref);
	}

// include CSS file asynchronous 	
function loadCSS(file)
	{
	var fileref=document.createElement("link")
		fileref.setAttribute("rel", "stylesheet")
	  	fileref.setAttribute("type", "text/css")
	  	fileref.setAttribute("href", file)

	document.getElementsByTagName("head")[0].appendChild(fileref);
	}

include("/comum/DPAC_syscall/jquery/jquery-1.7.1.js");
include("/comum/DPAC_syscall/jquery/jquery.mobile.js");
// include("/comum/mobile.js");

include("/comum/DPAC_syscall/jquery/jquery-ui-1.10.0.custom.min.js");

loadCSS("/css/CSS_syscall/comum/DPAC_syscall/jquery.mobile.css");
loadCSS("/css/CSS_syscall/comum/mobile.css");

/* Abre o modulo desejado */
function call(mod)
	{
	// window.location = "/sys/"+mod;
	// mobile_frm
	// document.forms[0].SHOW.value = x;
	document.forms[0].method = "post";
	document.forms[0].action = "/sys/"+mod;
	document.forms[0].submit();
	}