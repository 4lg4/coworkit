// This script and many more are available free online at
// The JavaScript Source!! http://javascript.internet.com
// Original:  Nick Baker -->

// Cookie Functions  ////////////////////  (:)


// Set the cookie.
// SetCookie('your_cookie_name', 'your_cookie_value', exp);


// Get the cookie.
// var someVariable = GetCookie('your_cookie_name');



var expDays = 3;
var exp = new Date(); 
exp.setTime(exp.getTime() + (expDays*24*60*60*1000));



function getCookieVal (offset) {  
	var endstr = document.cookie.indexOf (";", offset);  
	if (endstr == -1) { endstr = document.cookie.length; }
	return unescape(document.cookie.substring(offset, endstr));
}



function getCookie (name) {  
	var arg = name + "=";  
	var alen = arg.length;  
	var clen = document.cookie.length;  
	var i = 0;  
	while (i < clen) {    
		var j = i + alen;    
		if (document.cookie.substring(i, j) == arg) return getCookieVal (j);    
		i = document.cookie.indexOf(" ", i) + 1;    
		if (i == 0) break;   
	}  
	return null;
}



function setCookie (name, value) {  
	var argv = setCookie.arguments;  
	var argc = setCookie.arguments.length;  
	var expires = (argc > 2) ? argv[2] : null;  
	var path = (argc > 3) ? argv[3] : null;  
	var domain = (argc > 4) ? argv[4] : null;  
	var secure = (argc > 5) ? argv[5] : false;  
	document.cookie = name + "=" + escape (value) + 
	((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + 
	((path == null) ? "" : ("; path=" + path)) +  
	((domain == null) ? "" : ("; domain=" + domain)) +    
	((secure == true) ? "; secure" : "");
}




// cookieForms saves form content of a page.



// use the following code to call it:
//  <body onLoad="cookieForms('open', 'form_1', 'form_2', 'form_n')" onUnLoad="cookieForms('save', 'form_1', 'form_2', 'form_n')">



// It works on text fields and dropdowns in IE 5+
// It only works on text fields in Netscape 4.5





function cookieForms()
	{  
	var mode = cookieForms.arguments[0];
	

	for(f=1; f<cookieForms.arguments.length; f++)
		{
		formName = cookieForms.arguments[f];
		
		if(mode == 'open')
			{	
			cookieValue = getCookie('saved_'+formName);
			if(cookieValue != null)
				{
				var cookieArray = cookieValue.split('#cf#');
				
				if(cookieArray.length == document[formName].elements.length)
					{
					for(i=0; i<document[formName].elements.length; i++)
						{
						if(cookieArray[i].substring(0,6) == 'select')
							{
							try
								{
								document[formName].elements[i].options.selectedIndex = cookieArray[i].substring(7, cookieArray[i].length-1);
								}
							catch(err)
								{
								// ignora erro caso a caixa de seleçao nao tenha sido carregada
								}
							}
						else if(cookieArray[i].substring(0,2) == 'sm')
							{
							try
								{
								temp = cookieArray[i].substring(2, cookieArray[i].length-1);
								if(temp.indexOf('#') != -1)
									{
									temp = temp.split('#');
									for(g=0;g<temp.length;g++)
										{
										document[formName].elements[i].options[temp[g]].selected=true;
										}
									}
								else
									{
									document[formName].elements[i].options[temp].selected=true;
									}
								}
							catch(err)
								{
								// ignora erro caso a caixa de selecao nao tenha sido carregada
								}
							}
						else if((cookieArray[i] == 'cbtrue') || (cookieArray[i] == 'rbtrue'))
							{
							document[formName].elements[i].checked = true;
							}
						else if((cookieArray[i] == 'cbfalse') || (cookieArray[i] == 'rbfalse'))
							{
							document[formName].elements[i].checked = false;
							}
						else
							{
							document[formName].elements[i].value = (cookieArray[i]) ? cookieArray[i] : '';
							}
						}
					}
				}
			}

		if(mode == 'save')
			{	
			cookieValue = '';
			for(i=0; i<document[formName].elements.length; i++)
				{
				fieldType = document[formName].elements[i].type;
				if(fieldType == 'password')
					{
					passValue = '';
					}
				else if(fieldType == 'checkbox')
					{
					passValue = 'cb'+document[formName].elements[i].checked;
					}
				else if(fieldType == 'radio')
					{
					passValue = 'rb'+document[formName].elements[i].checked;
					}
				else if(fieldType == 'select-one')
					{
					passValue = 'select'+document[formName].elements[i].options.selectedIndex;
					}
				else if(fieldType == 'select-multiple')
					{
					passValue = 'sm';
					for(g=0; g<	document[formName].elements[i].options.length; g++)
						{
						if(document[formName].elements[i].options[g].selected == true)
							{
							passValue += g+'#';
							}
						}
					}
				else
					{
					passValue = document[formName].elements[i].value;
					}
				cookieValue = cookieValue + passValue + '#cf#';
				}
			cookieValue = cookieValue.substring(0, cookieValue.length-4); // Remove last delimiter
			
			setCookie('saved_'+formName, cookieValue, exp);		
			}	
		}
	}

//  End -->