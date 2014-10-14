/* [INI]  Upload form 1 -------------------------------------------------------------------------------  
interval = null;

function fetch(uuid)
	{
	req = new XMLHttpRequest();
	req.open("GET", "/progress", 1);
	req.setRequestHeader("X-Progress-ID", uuid);
	req.onreadystatechange = function()
		{
		if(req.readyState == 4)
			{
			if(req.status == 200)
				{
				// poor-man JSON parser 
				var upload = eval('new Object(' + req.responseText + ')');
				// change the width if the inner progress-bar 
				if(upload.state == 'done' || upload.state == 'uploading')
					{
					bar = document.getElementById('progressbar');
					w = (upload.received*99)/upload.size;
					bar.style.width = w + '%';
					document.getElementById('progressbar_perc').innerHTML = parseInt(w) + '%';
					}
				// we are done, stop the interval 
				if(upload.state == 'done')
					{
					bar = document.getElementById('progressbar');
					bar.style.width = '100%';
					document.getElementById('progressbar_perc').innerHTML = '100%';
					window.clearTimeout(interval);						
					\$("#progress_status").hide(); // esconde barra de progressao
					\$("#progress_form").show(); // esconde barra de progressao						
					\$(".button").text('Escolha o Arquivo'); // limpa o formulario						
					\$(".file-holder").text(''); // limpa o formulario
					\$("#doc_add").hide(); // esconde o botao de upload
					anexoAdd("",1); // atualiza tela
					\$("#doc_descrp").val("");
					\$("#doc_file").val("");
					\$("#doc_file").val("");
					\$(".file-holder").val("");
					}
				}
			}
		}
	req.send(null);
	}

function ProgressBar(event)
	{
	document.getElementById('progress').innerHTML = '<div id="progressbar_perc" style="text-align: left; position: absolute; left: 49%; margin-top: 2px;">0%</div><div id="progressbar" style="width: 100%; background-color: #00cc00; width: 0%; height: 100%; float: left;"></div>';

	// generate random progress-id 
	uuid = "";
	for(i = 0; i < 32; i++)
		{
		uuid += Math.floor(Math.random() * 16).toString(16);
		}		
	// call the progress-updater every 1000ms 
	interval = window.setInterval(function(){ fetch(uuid); }, 1000);
	\$("#progress_form").hide();
	\$("#progress").show();
	
	\$("#CAD").attr('action','/sys/upload/task.cgi?X-Progress-ID='+uuid);
	\$("#CAD").attr('target', 'uploadframe');
	\$("#CAD").submit();
	return false;
	}	

// upload button fake ------------------------
var SITE = SITE || {};

SITE.fileInputs = function() 
	{
	var \$this = \$(this),
      \$val = \$this.val(),
      valArray = \$val.split('\\\\'),
      newVal = valArray[valArray.length-1],
      // \$button = \$('.button'),
      \$button = \$('#wrapper_button'),
      \$fakeFile = \$('.file-holder');
	if(newVal !== '') 
		{
		\$button.text('Arquivo Selecionado');
		if(\$fakeFile.length === 0) 		
		\$button.after('<span class="file-holder">'+ newVal +'</span>');
		else 
			\$fakeFile.text(newVal);

		// ajusta botao upload
		\$("#doc_add").show(); // .addClass("button");
		}
	};
*/