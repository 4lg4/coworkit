#!/usr/bin/perl

use File::Basename;

$nacess = "";
require "../cfg/init.pl"; #ou ../cfg/init.pl
$COD = &get('COD');
$MODO = &get('MODO');
$action = &get('action');
$arquivo = &get('arquivo');
$descrp_arq = &get('descrp');
$img = "";

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
#List files
if($action eq "list" && $COD ne "")
	{
	#Array de extensões para comparação
	@$ext_array=(".jpeg", ".png", ".jpg");
	
	$DB = &DBE(" select * from chamado_arquivo where chamado='$COD' and chamado is not null ");
				
	if($DB->rows()>0)
		{
		#Puxa todas as empresa e monta o grid
		while($DB_codigo = $DB->fetchrow_hashref)
			{
				
			$DB2 = &DBE(" select * from arquivo where md5='$DB_codigo->{arquivo}' ");
			
			if($DB2->rows()>0)
				{
				#Puxa todas as empresa e monta o grid
				while($arquivos = $DB2->fetchrow_hashref)
					{
					$nome_tam=length($arquivos->{nome});
					$nome=$arquivos->{nome};
					$tamanho=$arquivos->{tamanho}/100;
					
					if($nome_tam>30)
						{
						$nome=substr($arquivos->{nome},0,20)."...";
						}
					
					#Pega e extensão do arquivo e verifica se é imagem ou doc
					($name,$path,$ext) = fileparse($arquivos->{nome},qr"\..[^.]*$");
					if(grep(/$ext/, @$ext_array))
						{
						$img = "img:'/sys/cfg/DPAC/view_avatar.cgi?MD5=".$arquivos->{md5}."',";
						}
					else
						{
						$img="";
						}
						
					#variavel que recebe os dados para montagem do DTOUCHRADIO - array
					$arquivos_array .="{val:'".$arquivos->{md5}."', $img descrp:'<b>Nome:</b> ".$nome." <br> <b>Tamanho:</b> ".$tamanho." KB <br> <b>Tipo:</b> ".$arquivos->{tipo}." ' },";
					}	
				}
			}
		}
		
	$arquivos_array = substr($arquivos_array, 0,-1); # remove ultima virgula
	
	if($arquivos_array ne "")
		{
		print " <script>
				\$('#upload').fieldUpload('addItem',[$arquivos_array]);
			</script>
			";
		exit;
		}
	}
#delete file
elsif($action eq "delete" && $arquivo ne "")
	{
	
	#Se for dafault upload
	$DB1 = &DBE("delete from chamado_arquivo where arquivo='$arquivo' ");
		
	#Pega o id do arquivo
	$DB2 = &DBE("select * from arquivo where md5='$arquivo' ");
	$anexo_rs = $DB2->fetch;
	$anexo=@$anexo_rs[0];
	
	# remove da tabela arquivo
	$DB3 = &DBE("delete from arquivo where md5 = '$anexo' ");
	
	# remove o arquivo fisico
	if(length($anexo) == 1) # Controla os 9 primeiros registros
		{ 
		$DEL_DIR = substr($anexo,0,1);
		$DEL_DIR .= 0; 
		}
	else
		{ $DEL_DIR = substr($anexo,0,2); }
	
	$fileA = $dirUpload.''.$DEL_DIR.'/'.$anexo;
	unlink($fileA) or die("Erro ao Excluir arquivo do servidor ! $fileA ");	
	}

if($action eq "insert" && $arquivo ne "")
	{
	
	#Se for dafault upload
	$DB1 = &DBE("insert into chamado_arquivo (chamado,arquivo) values('$COD','$arquivo'); ");
	}

#[FIM]//////////////////////////////////////////////////////  Exemplo de lista  ///////////////////////////////////////////////////////////////#