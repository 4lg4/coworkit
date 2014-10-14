#!/usr/bin/perl

$nacess = '';
$MODO = "incluir";

require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');
$SHOW = &get('SHOW');
if($SHOW eq "usuarios")
	{
	$TABLE = "usuario";
	$CHAVE = "usuario";
	}
elsif($SHOW =~ /^sac_/)
	{
	$TABLE = "sac";
	$CHAVE = "codigo";
	}
else
	{
	$TABLE = $SHOW;
	$CHAVE = "codigo";
	}


print $query->header({charset=>utf8});


# Lista o nome das colunas para montar o formulário
$SQL = "select column_name, data_type, character_maximum_length, is_nullable, column_default from information_schema.columns where table_name = '$TABLE' $SQL order by ordinal_position";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	$cols = $sth->fetchall_arrayref();
	}

# Se for alteração, encontra os valores de cada coluna
if($MODO ne "incluir")
	{
	$SQL = "select * from $TABLE where $CHAVE = '$COD' order by $CHAVE limit 1";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		$value = $sth->fetchrow_hashref;
		}

	}

# Verifica se é um registro liberado de alteração pelos parceiros
$restrito = 0;
if($value->{'restrito'} eq '1' && $LOGEMPRESA ne "1")
	{
	$restrito = $value->{'restrito'};
	$MODO = "ver";
	}

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<style>
dl.form
	{
	width: 96%;
	margin: 7px 0;
	padding: 0;
	padding-top: 5px;
	padding-bottom: 5px;
	padding-right: 0px;
	}
	
dl.form dl
	{
 	margin: 0px;
	}

.form dt
	{
	width: 15%;
	float: left;
	margin: 0 0 0 0;
	padding: 3px;
	font-weight: normal;
	color:#FFF;
    clear:both;
	}

td.form
	{
	font-size: 12px;
	font-weight: bold;
	color: #FFF;
	}


.form dd
	{
	float: left;
	margin: 0 0 0 0;
	padding: 1px;
	font-weight: normal;
	width: 70%;
	color:#FFF;
	}
    
    
.hidden_class {
    display : none;
}



</style>
  <script language='JavaScript'>
  
  
	
	//Ajuste o boxe
	\$("#box").DTouchBoxes({
		title:'Edição da tabela: $TABLE'
		});
		
	//Cria o elemento datepicker
	\$("#date").fieldDateTime(
			{ 
			type: "date",
			dateFormat: "dd/mm/yy"
			});
			
		
	function screenRefresh()
		{
		var cores = ["#dfdfdf", "#ffffff"];
		grids = getElementsByClass('navigateable');
		for(var gd=0;gd<grids.length;gd++)
			{
			linhas = grids[gd].getElementsByTagName('TR');
			for(var ln=1;ln<linhas.length;ln++)
				{
				cor_fundo = cores[ln % 2];
				linhas[ln].style.background = cor_fundo;
				}
			}
		}
	function DActionEdit()
		{
		Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "$dir{'cadastros'}del_submit.cgi",
			dataType: "html",
			data: \$("#CAD").serialize(),
			success: function(data)
				{
				\$("#main_div").html(data);
				\$("#resultado").html(data);
				unLoading();
				},
			error: errojx
			});
		}
	function ver()
		{
		parent.block(false);
		if(\$("#CAD input[name=COD]").val()=="")
			{
			callRegrid('$SHOW');
			}
		else
			{
			\$("#CAD input[name=MODO]").val('ver');
			\$("#CAD").submit();
			}
		}
	function imprimir()
		{
		alert('não implementado!');
		}
	function DActionAdd()
		{
		//top.ac_show(['icon_save','icon_cancel']);
        // top.eos.menu.action.show(['icon_save','icon_cancel']);
        
		\$("#CAD input[type=text]").each(function()
			{
			\$(this).val('');
			});
		\$("#CAD input[name=COD]").val('');
		\$("#CAD input[name=MODO]").val('incluir');
		\$("#CAD").submit();
		}
	function DActionDelete()
		{
		confirma('Você tem certeza que deseja excluir esse registro?<br>Essa ação é IRREVERSÍVEL!', 'excluir_confirm()', '');
		}
	function excluir_confirm()
		{
		parent.block(false);
		Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "$dir{'cadastros'}del_submit.cgi",
			dataType: "html",
			data: \$("#CAD").serialize(),
			success: function(data)
				{
				\$("#main_div").html(data);
				\$("#resultado").html(data);
				unLoading();
				},
			error: errojx
			});
		}
	function DActionBack()
		{
		callRegrid('$SHOW');
		}
	function DActionCancel()
		{
		confirma('Você tem certeza que deseja cancelar?<br>Todos os dados modificados serão perdidos!', 'callRegrid("$SHOW")', '');
		}
	function DActionSave()
		{
HTML
#Validação de cada coluna
foreach $row(@{$cols})
	{
	if(uc(@$row[3]) ne "YES" && @$row[4] !~ /^nextval/ && @$row[1] !~ /^boolean/ )
		{
		print "		if(\$(\"#CAD input[name=@$row[0]]\").val()=='')\n";
		print "			{\n";
		print "			alerta('Você não informou o ".ucfirst(@$row[0])."!', '\$(\"#CAD input[name=@$row[0]]\").focus()');\n";
		print "			return false;\n";
		print "			}\n";
		}
	}

print<<HTML;
		parent.block(false);
		Loading();
		
		
		\$('#CAD input[name=Ativo]').prop('name','status');
		
		if("$TABLE"=="plano")
			{
			var validDate = \$.datepicker.formatDate( "yy-mm-dd", \$('#date').datepicker('getDate'));
			\$('#date').val(validDate);
			}
		
		$ajax_init \$.ajax({
			type: "POST",
			url: "/sys/cad/default/edit_submit.cgi",
			dataType: "html",
			data: \$("#CAD").serialize(),
			success: function(data)
				{
				\$("#main_div").html(data);
				\$("#resultado").html(data);
				unLoading();
				},
			error: errojx
			});
		
		}
	function erro(x,y)
		{
		if(y.indexOf('[') > 0)
			{
			el = y.substring(0,y.indexOf('['));
			pos = y.substring(y.indexOf('[')+1, y.indexOf(']'));
			document.getElementsByName(el)[pos].style.borderColor = 'red';
			alerta(x,"main.document.getElementsByName(\\""+el+"\\")["+pos+"].focus()");
			}
		else
			{
			document.getElementsByName(y)[0].style.borderColor = 'red';
			alerta(x,\$('#CAD input[name='+y+']').focus());
			}
		}
	function limpa(y)
		{
		if(y)
			{
			document.getElementsByName(y)[0].style.borderColor = '';
			}
		}
	function START()
		{
            top.eos.menu.action.hideAll();
            /*
            top.eos.menu.action.new({ // novo
                id       : "icon_grid_edit_new",
                title    : "novo",
                subtitle : "",
                click    : function(){
                    DActionAdd();
                }
            });
  */
            top.eos.menu.action.new({ // cancel
                id       : "icon_grid_edit_cancel",
                title    : "cancelar",
                subtitle : "",
                click    : function(){
                    DActionCancel();
                }
            });
  
            top.eos.menu.action.new({ // save
                id       : "icon_grid_edit_save",
                title    : "salvar",
                subtitle : "",
                click    : function(){
                    DActionSave();
                }
            });
            
		
HTML
if($MODO eq "editar")
	{
print<<HTML;
		parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
HTML
if($restrito eq "1" && $LOGEMPRESA ne "1")
	{
print<<HTML;
		//top.ac_show(['icon_cancel','icon_save']);
        // top.eos.menu.action.show(['icon_cancel','icon_save']);
		parent.block(false);
HTML
	}
else
	{
print<<HTML;
		// top.ac_show
        // top.eos.menu.action.show(['icon_cancel', 'icon_save', 'icon_insert', 'icon_delete']);
HTML
	}
	
print<<HTML;
		// \$('.money').priceFormat({ 		clearPrefix: true 	}); 
		\$('.change_time').setMask();
HTML
	}
elsif($MODO eq "incluir")
	{
print<<HTML;
		parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
HTML

print<<HTML;
		//top.ac_show
        // top.eos.menu.action.show(['icon_cancel','icon_save']);
		parent.block(false);
HTML
	
print<<HTML;
		// \$('.money').priceFormat({ 		clearPrefix: true 	}); 
		\$('.change_time').setMask();
HTML
	}
else
	{
print<<HTML;
		linhas = document.body.getElementsByTagName('SELECT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			//linhas[ln].disabled=true;
			linhas[ln].setAttribute('onchange', '\$("#CAD").reset()');
			linhas[ln].style.backgroundColor='#cdcdcd';
			}
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].type.toLowerCase() != 'hidden')
				{
				//linhas[ln].disabled=true;
				linhas[ln].setAttribute('onchange', '\$("#CAD").reset()');
				if(linhas[ln].type.toLowerCase() != 'radio')
					{
					linhas[ln].style.backgroundColor='#cdcdcd';
					}
				}
			}
		linhas = document.body.getElementsByTagName('TEXTAREA');
		for(var ln=0;ln<linhas.length;ln++)
			{
			//linhas[ln].disabled=true;
			linhas[ln].setAttribute('onchange', '\$("#CAD").reset()');
			linhas[ln].style.backgroundColor='#cdcdcd';
			}
HTML
if($restrito eq "1" && $LOGEMPRESA ne "1")
	{
print<<HTML;
		// top.ac_show
        // top.eos.menu.action.show(['icon_cancel', 'icon_insert']);
HTML
	}
else
	{
print<<HTML;
		// top.ac_show
        // top.eos.menu.action.show(['icon_cancel', 'icon_edit', 'icon_insert', 'icon_delete']);
HTML
	}
print<<HTML;
		// \$('.money').priceFormat();
		\$('.change_time').setMask();
HTML
	}
print<<HTML;
		unLoading();
		}

	\$(document).ready(function() 
		{
		START();
		});
  </script>
</head>
<body style="overflow-x: hidden; overflow-y: auto;">

<form name='CAD' id='CAD' method='post'  onSubmit='return false;'>


<div style='width: 95%; margin: 2%; margin-right: 3%;'>
HTML
print<<HTML;
		<div id="box" style=" width:90%; overflow-y: auto; height:auto; color: #FFF !important; padding: 10px;">

			<dl class=form style="width: 80%; margin-top: 0px;">
				<div>
HTML
foreach $row(@{$cols})
	{ 
    # campo parceiro já vem preenchido e escondido 
    $hidden    = "";
    # $show_text = "";
    if(lc(@$row[0]) eq "parceiro") {
        $hidden = "hidden_class";
        if(!$COD) {
            $value->{@$row[0]} = $USER->{empresa};
            # $show_text = $USER->{empresa_nome};
        }
    } elsif(lc(@$row[0]) eq "pai"  || lc(@$row[0]) eq "obrigatorio" || lc(@$row[0]) eq "restrito" || lc(@$row[0]) eq "exportar") { 
        $hidden = "hidden_class";
    }
    
    
	if(@$row[0] ne "restrito" || $LOGEMPRESA eq "1")
		{
		# Verifica se tem chave estrangeira
		$sth2 = &select("SELECT ccu.table_name AS references_table, ccu.column_name AS references_field FROM information_schema.table_constraints tc LEFT JOIN information_schema.key_column_usage kcu ON tc.constraint_catalog = kcu.constraint_catalog AND tc.constraint_schema = kcu.constraint_schema AND tc.constraint_name = kcu.constraint_name LEFT JOIN information_schema.referential_constraints rc ON tc.constraint_catalog = rc.constraint_catalog AND tc.constraint_schema = rc.constraint_schema AND tc.constraint_name = rc.constraint_name LEFT JOIN information_schema.constraint_column_usage ccu ON rc.unique_constraint_catalog = ccu.constraint_catalog AND rc.unique_constraint_schema = ccu.constraint_schema AND rc.unique_constraint_name = ccu.constraint_name WHERE tc.table_name = '$TABLE' and tc.constraint_type ilike 'foreign key' and kcu.column_name = '@$row[0]'  ");
		$rv2 = $sth2->rows();
		if($rv2 > 0)
			{
			print "					  <dt><span class='$hidden'>".&traduz(@$row[0])."</span></dt>\n";
			print "					  <dd><select name='@$row[0]' class='$hidden'>";
			while($row2 = $sth2->fetch)
				{
				# Traz os dados da tabela estrangeira se o campo for descrição
				$sth3 = $dbh->prepare("select ".@$row2[1].", descrp from @$row2[0] ");
				$sth3->execute();
				$rv3 = $sth3->rows();
				if($rv3 > 0)
					{
					while($row3 = $sth3->fetch)
						{
						print "<option value='".@$row3[0]."'";
						if($value->{@$row[0]} eq @$row3[0])
							{
							print "selected";
							}
						print ">@$row3[1]</option>";
						}
					}
				else
					{
					# Traz os dados da tabela estrangeira se o nome do campo for nome (algumas tabelas não são descrição)
					$sth3->finish;
					$sth3 = $dbh->prepare("select ".@$row2[1].", nome from @$row2[0] ");
					$sth3->execute();
					$rv3 = $sth3->rows();
					if($rv3 > 0)
						{
						while($row3 = $sth3->fetch)
							{
							print "<option value='".@$row3[0]."'";
							if($value->{@$row[0]} eq @$row3[0])
								{
								print "selected";
								}
							print ">@$row3[1]</option>";
							}
						}
					}
				}
			print "</select></dd>";
			}
		else
			{
			if(@$row[4] =~ /^nextval/ )
				{ 
				print "					  <dt>".&traduz(@$row[0])."</dt>\n";
				print "					  <dd><input type='text' name='@$row[0]' value='$value->{@$row[0]}'";
				if(@$row[2] eq "")
					{
					if(@$row[1] =~ /^timestamp/)
						{
						print " style='width: 170px' class='change_time' alt='time2' ";
						}
					elsif(@$row[1] =~ /^date/)
						{
						print " style='width: 170px' id='date' ";
						}
					elsif(@$row[1] =~ /^time/)
						{
						print " style='width: 50px' class='change_time' alt='time2' ";
						}
					else
						{
						print " style='width: 100px' ";
						}
					}
				elsif(@$row[2] < 10)
					{
					print " style='width: ".(@$row[2]*20)."px' ";
					}
				elsif(@$row[2] ne "")
					{
					print " style='width: ".(@$row[2]*3)."px' ";
					}
				print " disabled></dd>\n";
				}
			else
				{ 
                    
				if($TABLE eq "prod_servicos" && @$row[1] =~ /^boolean/ && @$row[0] eq "status")
					{ @$row[0]="Ativo";	}
				print "					  <dt><span class='$hidden'>".&traduz(@$row[0])."</span></dt>\n";
				if(@$row[1] =~ /^boolean/)
					{
					print "					<dd><span style='margin-right: 20px' class='$hidden'><input type='radio' name='@$row[0]' value='true' class='$hidden'";
					if($value->{@$row[0]} eq "1")
						{
						print " checked";
						}
					print "> Sim</span> <input type='radio' name='@$row[0]' value='false' class='$hidden' ";
					if($value->{@$row[0]} ne "1")
						{
						print " checked";
						}
					print "> <span class='$hidden'>Não</span></dd>";
					}
				else
					{
					if(@$row[2] > 250)
						{
						print "					<dd><textarea name='@$row[0]' ";
						}
					else
						{
						if(@$row[1] =~ /^timestamp/)
							{
							$value->{@$row[0]}=dateToShow($value->{@$row[0]});
							}
						elsif(@$row[1] =~ /^date/)
							{
							$value->{@$row[0]}=dateToShow($value->{@$row[0]},'DATE');
							}
                        
                            
                        # campo edicao    
						print "					  <dd>$show_text<input type='text' name='@$row[0]' value='$value->{@$row[0]}' class='$hidden' ";
						}
					if(@$row[2] eq "")
						{
						if(@$row[1] =~ /^timestamp/)
							{
							print " style='width: 170px' id='date' ";
							}
						elsif(@$row[1] =~ /^date/)
							{
							print " style='width: 170px' id='date' ";
							}
						elsif(@$row[1] =~ /^time/)
							{
							print " style='width: 60px' class='change_time' alt='time2' ";
							}
							
						elsif(@$row[1] =~ /^money/)
							{
							print " style='width: 100px; text-align: right;' class='money' ";
							}
						else
							{
							print " style='width: 100px' ";
							}
						}
					elsif(@$row[2] < 10)
						{
						print " style='width: ".(@$row[2]*12)."px' ";
						}
					elsif((@$row[2]*3) > 1000)
						{
						print " style='width: 100%'";
						}
					elsif(@$row[2] ne "")
						{
						print " style='width: ".(@$row[2]*3)."px' ";
						}
					if(@$row[2] > 250)
						{
						print ">$value->{@$row[0]}</textarea></dd>\n";
						}
					else
						{
						print "></dd>\n";
						}
					}
				}
			}
		}
	}
print<<HTML;
				</div>
			<br clear=all></dl><br>
HTML
if($restrito eq '1' && $LOGEMPRESA ne "1")
	{
	print "<div id='message' style='text-align: left; font-family: Tahoma, sans-serif; font-size: 13px; font-weight: bold; color: #31517a; margin-left: 4px;'>Você não tem permissão para editar esse registro</div><br>";
	}
print<<HTML;
		</div>
	</div>
</div>

<script>
    \$("input[type=text]:visible").each(function(){
        eos.template.field.text(\$(this));
    });
</script>

<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='$MODO'>
<input type='hidden' name='SHOW' value='$SHOW'>
</form>

HTML
