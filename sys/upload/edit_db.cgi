#!/usr/bin/perl

$nacess = "123";
require "../cfg/init.pl"; #ou ../cfg/init.pl
$tipo = &get('COD');
$MODO = &get('MODO');

print $query->header({charset=>utf8});

#[INI]/////////////////////////////////////////////////////////  Lembretes  ///////////////////////////////////////////////////////////////////#

# SELECT --> $DB1 = &DBE("select * from tabela where tabela is null order by campo");
# DELETE --> $DB2 = &DBE("delete from tabela where coluna='identificao'");
# INSERT --> $DB3 = &DBE("insert into tabela (campo1,campo2...) values ('".$variavel."') ");

#-------------------------------------------------------------------- While -------------------------------------------------------------------#

# while($row_title = $DB->fetchrow_hashref)
# 	{
# 	$modulos .="<li><a href='#t-$i'>$row_title->{'descrp'}</a></li>";
# 	$i++;
# 	}

#-------------------------------------------------------------------  FOR  --------------------------------------------------------------------#

#for($g=0; $g<$ncol; $g++)
# {
# $menu[$g] .= "<div class='menu menu_".$row->{'codigo'}."'>";
# }

#-----------------------------------------------  Pega o primeiro o id após inserção ou atualização -------------------------------------------#

# $codigo=$tipo_usuario->fetch;
# $DB4 = &DBE("update tabela set descrp='".ucfirstall($tipo_descrp)."' where codigo='@$codigo[0]'  ");

#--------------------------------------------  Recupera o ultida id cadastrado, somente após inserção  ----------------------------------------#

#[FIM]/////////////////////////////////////////////////////////  Lembretes  ///////////////////////////////////////////////////////////////////#

$DB = &DBE("select * from menu where pai is not null and descrp <> 'Default Upload'");

if($DB->rows()>0)
	{
	while($menus=$DB->fetchrow_hashref)
		{
		# monta array com todos os itens para adicionar no radio
		$menu_item .= "{val:$menus->{codigo},descrp:'$menus->{descrp}'},";
		}
	$menu_item = substr($menu_item, 0,-1); # remove ultima virgula
	}
else
	{
	$menu_item .= "{val:'',descrp:'Nenhum menu encontrado.'},";
	}
	
print "<script>
		\$('#modulos').DTouchRadio(
			{
			orientation:'vertical',
			addItem: [$menu_item],
			DTouchRadioClick: function()
						{
						//Acessa a função do objeto e passar o parâmetro
						var COD=\$(\"#modulos\").DTouchRadio('DTouchRadioGetValue');
						\$('#COD').val(COD);
						\$('#bloco_modulos').css('width','45%');
						\$('#bloco_upload').css('display','block');
						\$('#upload').fieldUpload('reset');
						\$('#upload').data('fieldUploadSettings')['UploadList'](COD);
						}
			});
	</script>"

#[FIM]//////////////////////////////////////////////////////  Exemplo de lista  ///////////////////////////////////////////////////////////////#