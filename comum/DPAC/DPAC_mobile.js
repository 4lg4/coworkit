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

loadCSS("/css/mobile/jquery/jquery.mobile-1.3.0-beta.1.min.css");
loadCSS("/css/mobile/jquery/done_eos.min.css");
loadCSS("/css/mobile/jquery/jquery.mobile.structure-1.3.0-beta.1.min.css.css");
	
include("/comum/jquery/jquery-1.9.0.min.js");
include("/comum/jquery/jquery.mobile-1.3.0-beta.1.min.js");
// include("/comum/mobile.js");


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