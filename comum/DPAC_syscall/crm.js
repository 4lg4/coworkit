
function chPrazo()
	{
	dtini = $("#dt_ini").datepicker("getDate");
	var y = dtini.getFullYear();
	var m = dtini.getMonth();
	var d = dtini.getDate();
	var qtd = "";
	var qtd = document.forms[0].PRAZO.options[document.forms[0].PRAZO.selectedIndex].value;
	if(qtd == '365 days')
		{
		dtfim = new Date(y+1, m, d);
		}
	else if(qtd == '30 days')
		{
		dtfim = new Date(y, m+1, d);
		}
	else if(qtd.search(/days$/i) > 0)
		{
		qtd = qtd.replace("days", "");
		qtd = parseInt(qtd);
		dtfim = new Date(y, m, d + qtd);
		}
	else
		{
		dtfim = "";
		}
	if(dtfim == "")
		{
		$("#dt_fim").val("");
		$("#shw_dtfim").css({display: 'none'});
		}
	else
		{
		$("#dt_fim").val(dtfim.getDate()+"/"+(dtfim.getMonth()+1)+"/"+dtfim.getFullYear());
		$("#shw_dtfim").css({display: 'inline'});
		}
	}

