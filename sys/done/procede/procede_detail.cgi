#!/usr/bin/perl

$nacess = '206';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_emp');
if($COD eq "")
	{
	$COD = &get('COD');
	}
if($COD eq "undefinied")
	{
	$COD = "";
	}
$MODO = &get('MODO');
$CODPROCEDE = &get('procede');
$ENDERECO = &get('cod_endereco');
if($ENDERECO eq "undefinied")
	{
	$ENDERECO = "";
	}
$BOX = &get('box');
if($BOX eq "")
	{
	$BOX = $ENDERECO;
	}


if($LOGUSUARIO eq "admin")
	{
	$nacess_tipo = "s";
	}
if($nacess_tipo eq "a" || $nacess_tipo eq "s")
	{
	$MODO = "editar";
	}
else
	{
	$MODO = "ver";
	}

print $query->header({charset=>utf8});
$out=<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML

if($CODPROCEDE ne "")
	{
	$SQL = "select * from endereco_procedimentos where endereco_procedimentos.codigo = '$CODPROCEDE' ";
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	if($rv3 > 0)
		{
		$row3 = $sth3->fetchrow_hashref;
		$CODPROCEDE = $row3->{'codigo'};
		$TITULO = $row3->{'titulo'};
		$DESCRP = $row3->{'descrp'};
		$DESCRP=~ s/\n/ /gm;
		$DESCRP=~ s/"//gm;
		$DESCRP=~ s/\r/ /gm;
		&form;
		$out =~ s/<ICONEX>/<img src='\/img\/syscall\/incluir.png' border=0 alt='incluir' style='margin-top: 4px; cursor: pointer;' id='detail_icon_insert_$BOX' onClick='add("$ENDERECO")'><img src='\/img\/syscall\/excluir.png' border=0 alt='excluir' style='margin-top: 4px; cursor: pointer;' id='detail_icon_delete_$BOX' onClick='excluir("$CODPROCEDE", "$ENDERECO", "$COD")'><img src='\/img\/syscall\/cancelar.png' border=0 alt='cancelar' style='display: none; margin-top: 4px; cursor: pointer;' id='detail_icon_cancel_$BOX' onClick='document.forms[0].reset(); hide(\"detail_icon_save_$BOX\"); hide(\"detail_icon_cancel_$BOX\"); parent.block(false); show(\"detail_icon_insert_$BOX\"); show(\"detail_icon_delete_$BOX\");'>      <img src='\/img\/syscall\/salvar.png' border=0 alt='salvar' style='display: none; margin-top: 4px; cursor: pointer;' id='detail_icon_save_$BOX' onClick='hide("detail_icon_save_$BOX"); salvar("$CODPROCEDE", "$ENDERECO", "$COD");'>/gm;
		}
	else
		{
		&form;
		$out =~ s/<ICONEX>/<img src='\/img\/syscall\/cancelar.png' border=0 alt='cancelar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_cancel_$BOX' onClick='document.forms[0].reset(); hide(\"detail_icon_save_$BOX\"); hide(\"detail_icon_cancel_$BOX\"); parent.block(false); show(\"detail_icon_insert_$BOX\"); show(\"detail_icon_delete_$BOX\"); hide(\"cx2_$BOX\");'><img src='\/img\/syscall\/salvar.png' border=0 alt='salvar' style='margin-top: 10px; cursor: pointer;' id='procede_icon_save_$BOX' onClick='hide("procede_icon_save"); salvar("", "$ENDERECO", "$COD");'>/gm;
		}
	}
elsif($ENDERECO ne "")
	{
	&form;
	$out =~ s/<ICONEX>/<img src='\/img\/syscall\/cancelar.png' border=0 alt='cancelar' style='margin-top: 4px; cursor: pointer;' id='detail_icon_cancel_$BOX' onClick='document.forms[0].reset(); hide(\"detail_icon_save_$BOX\"); hide(\"detail_icon_cancel_$BOX\"); parent.block(false); show(\"detail_icon_insert_$BOX\"); show(\"detail_icon_delete_$BOX\"); hide(\"cx2_$BOX\");'><img src='\/img\/syscall\/salvar.png' border=0 alt='salvar' style='margin-top: 10px; cursor: pointer;' id='procede_icon_save' onClick='hide("procede_icon_save"); salvar("", "$ENDERECO", "$COD");'>/gm;

	$out .= "<script language='JavaScript'>";
	$out .= "	screenRefresh('tbitem_$ENDERECO', '0');";
	$out .= "</script>";
	}


$out.=<<HTML;
</body></html>
HTML

print $out;

exit;



sub form
	{
	$out.=<<END;
<!-- edicao do modelo -->
<div class="fake_aba" style="width:60%; margin-left: 0px;">
	<table style="margin:5px; margin-right:10px; margin-bottom:0px; width:90%; color:#fff;">
		<tr>
			<td width=10%><b>Titulo:</b></td>
			<td><input type='hidden' name="codprocede_$BOX" value='$CODPROCEDE'><input type='text' name="titulo_$BOX" id="titulo_$BOX" style='width:100%; margin-left:10px;' value='$TITULO' onKeyUp="checkChange('$BOX', this.value, '$TITULO')"></td>
		</tr>
	</table>
</div>
<div class="navigateable_box rounded" style="width: 100%; height: 301px; border: solid 1px #000000; border-top: none 0px; background: url(\/img\/syscall\/menu_fundo_actions.png) repeat-y #e5e5e5;">
	<div id='actions' style='position: absolute; left; 10px; width: 55px; height: 100%;'>
		<center>
		    <ICONEX>
		</center>
	</div>
	<div style='position: absolute; left: 62px; right: 12px;'>
		<textarea id="descricao_$BOX" name="descricao_$BOX" class="tinymce" style="height:296px; border:0px; margin:0px;">$DESCRP</textarea>
	</div>
</div>
<script language='JavaScript'>
descricao_vlr[$BOX] = '$DESCRP';
</script>
END
	}


