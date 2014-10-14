function show(object)
	{
	if(document.getElementById && document.getElementById(object) != null)
		{
		node = document.getElementById(object).style.visibility='visible';
		node = document.getElementById(object).style.display='inline';
		}
    else
		{
		if(document.layers && document.layers[object] != null)
			{
			document.layers[object].visibility = 'visible';
			document.layers[object].display = 'inline';
			}
		}
	}
function hide(object)
	{
	if(document.getElementById && document.getElementById(object) != null)
		{
		node = document.getElementById(object).style.visibility='hidden';
		node = document.getElementById(object).style.display='none';
		}
    else
		{
		if(document.layers && document.layers[object] != null)
			{
			document.layers[object].visibility = 'hidden';
			document.layers[object].display = 'none';
			}
		}
	}
