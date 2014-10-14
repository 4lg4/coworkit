#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;

$nacess = '';
require "../cfg/init.pl";

$ID = &get("ID");
$COD = &get("COD");
if($COD eq "")
	{
	$COD = &get("codigo");
	}
$arquivo = &get("cod_arq");
$doc_data = &timestamp("timestamp");
$doc_file = &get("file[]");
$doc_descrp = &get("fieldUploadDescrp");
$action = &get("action");
$doc_file_tmp = &timestamp("comparison");
$img = "";

#Array de extensões para comparação
@$ext_array=(".jpeg", ".png", ".jpg");
#Tabela ao qual será inserido o registro
$table = &get("FieldUploadTable");
#Campo/Coluna a qual pode ser usada para atualizar ou inserir um registro
$field = &get("FieldUploadField");
#Coluna que serve para inserir em uma tabela de vinculo
$colum = &get("FieldUploadColum");


$upload_dir =  $dirUpload;

print $query->header({charset=>utf8});

# # diretorio temporario se nao existir cria
# $TEMP_DIR = $upload_dir."tmp/";
# if(! -d $TEMP_DIR)
# 	{ mkdir $TEMP_DIR; }
# 
# print "<script>alert('@$doc_file');</script>";

# foreach my $file (@$doc_file)
# 	{
# 	
# 	$names .=$file[2];
	# faz upload do arquivo com nome temporario criado
# 	my $doc_file_hand = $query->upload(@$doc_file);
# 	open(UPLOADFILE, ">".$TEMP_DIR."".$doc_file_tmp) or die "$!";
# 	binmode UPLOADFILE;
# 	while ( <$doc_file_hand> )
# 		{
# 		print UPLOADFILE;
# 		}
# 	close UPLOADFILE;

# 	# pega file type (extension) ----------------------------------
# 	$fileA = $TEMP_DIR."".$doc_file_tmp; # junta caminho com nome do arquivo temporario
# 	$doc_type = `/usr/bin/file -i -b $fileA`; # pega tipo do arquivo	
# 
# 	$doc_data = &timestamp("timestamp"); # pega data
# 
# 	# pega o tamanho do arquivo
# 	$tamanho=((stat $fileA)[7]);
# 		if($tamanho==0 || $tamanho=="")
# 		{ $tamanho=0;}
# 		
# 	#Criptografa e Encoda
# 	$time=time();
# 	$cript=$fileA.$time;
# 	$doc_md5 = `echo "$cript" | md5sum -t | cut -d" " -f1`;
# 	$doc_md5 =~ s/\n//gm;
# 	$doc_md5 =~ s/\r//gm;
# 	$doc_md5 =~ s/^\s+//; # ltrim
# 	$doc_md5 =~ s/\s+$//; # rtrim
# 
# 
# 
# 	# [INI] Arquivo, Add  ----------------------------------------------------------------------------------------------------------
# 	$DB = &DBE("insert into arquivo(data, nome, tipo, descrp, md5, usuario,empresa,tamanho) values ('$doc_data', '$doc_file', '$doc_type', '$doc_descrp', '$doc_md5', '$USER->{usuario}','$USER->{'empresa'}','$tamanho')");
# 
# 	# Arquivo, get code (id)
# 	$DB = &DBE("select currval('arquivo_codigo_seq') ");
# 	$row = $DB->fetch;
# 	$doc_codigo = @$row[0];
# 	# [END] Arquivo, Add  ----------------------------------------------------------------------------------------------------------
# 
# 	#Se for para inserir na tabela do modulo
# 	if($table ne "" && $field ne "" && $COD ne "")
# 		{
# 		#excessão pois a tabela usuario a coluna: codigo=usuario
# 		if($table eq "usuario")
# 			{
# 			$DB = &DBE("update $table set $field='$doc_md5' where usuario=$COD");
# 			}
# 		#padrão
# 		elsif($table ne "default_avatar" && $table ne "empresa_arquivo")
# 			{
# 			$DB = &DBE("update $table set $field='$doc_md5' where codigo=$COD");
# 			}
# 		}
# 
# 
# 		# Cria diretorio se nao existir
# 		if(length($doc_codigo) == 1) # Controla os 9 primeiros registros
# 			{
# 			$folder = substr($doc_codigo,0,1);
# 			$folder .= 0;
# 			}
# 		else
# 			{ $folder = substr($doc_codigo,0,2); } # pega codigo do documento
# 
# 		if(! -d $upload_dir."".$folder) # se a pasta nao existir cria
# 			{ mkdir $upload_dir."".$folder; }
# 
# 	# Move arquivo e renomeia para pasta final
# 	rename($fileA, $upload_dir."".$folder."/".$doc_codigo)
# 	or die ("Erro ao mover o arquivo para pasta final !");
# 	}


#Se for exclusão
if($action eq "list" && $COD ne "" && $COD ne "null")
	{	
	$campo=$colum;
	
	if($table eq "usuario"){$campo="usuario";}
	$DB = &DBE(" select * from $table where $campo='$COD' and $field is not null ");
	
	$arquivos_array="";
	
	if($DB->rows()>0)
		{

		#Puxa todas as empresa e monta o grid
		while($DB_codigo = $DB->fetchrow_hashref)
			{
			if($table eq "usuario")
				{
				$codigo=$DB_codigo->{img};
				}
			else
				{
				$codigo=$DB_codigo->{arquivo};
				}
				
			$DB2 = &DBE(" select * from arquivo where md5='$codigo' ");
			
			if($DB2->rows()>0)
				{
				#Puxa todas as empresa e monta o grid
				while($arquivos = $DB2->fetchrow_hashref)
					{
					$nome_tam=length($arquivos->{nome});
					$nome=$arquivos->{nome};
					$tipo=substr($arquivos->{tipo},6,4);
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
					$arquivos_array .="{val:'".$arquivos->{md5}."', $img descrp:'<b>Nome:</b> ".$nome." <br> <b>Tamanho:</b> ".$tamanho." KB <br> <b>Tipo:</b> ".$tipo." ' },";
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
		}
	}
#Se for exclusão
elsif($action eq "delete")
	{

	#Remove vínculo com a tabela usuario
	if($table eq "usuario")
		{
		#Atualiza a tabela
		$DB1 = &DBE("update $table set $field=null where $field='$arquivo' ");
		}
	#Deleta o vínculo
	else
		{
		$DB1 = &DBE("delete from $table where $field='$arquivo' ");
		}
		
	#Pega o id do arquivo
	$DB2 = &DBE("select * from arquivo where md5='$arquivo' ");
	$anexo_rs = $DB2->fetch;
	$anexo=@$anexo_rs[0];
	
	# remove da tabela arquivo
	$DB3 = &DBE("delete from arquivo where md5 = '$arquivo' ");
	
	# remove o arquivo fisico
	if(length($anexo) == 1) # Controla os 9 primeiros registros
		{ 
		$DEL_DIR = substr($anexo,0,1);
		$DEL_DIR .= 0; 
		}
	else
		{ $DEL_DIR = substr($anexo,0,2); }
	
	$fileA = $upload_dir.''.$DEL_DIR.'/'.$anexo;
	unlink($fileA) or die("Erro ao Excluir arquivo do servidor ! select * from arquivo where md5='$arquivo'  ");
	}
else
	{

# diretorio temporario se nao existir cria
	$TEMP_DIR = $upload_dir."tmp/";
	if(! -d $TEMP_DIR)
		{ mkdir $TEMP_DIR; }

# 	$EMP_DIR = $upload_dir."$USER->{'empresa'}";
# 	if(! -d $EMP_DIR)
# 		{ mkdir $EMP_DIR; }	

	#Se não tiver descrição usar o nome do arquivo.
	if($doc_descrp eq ""){$doc_descrp=$doc_file;}
		
	# faz upload do arquivo com nome temporario criado
	my $doc_file_hand = $query->upload("file[]");
	open(UPLOADFILE, ">".$TEMP_DIR."".$doc_file_tmp) or die "$!";
	binmode UPLOADFILE;
	while ( <$doc_file_hand> )
		{
		print UPLOADFILE;
		}
	close UPLOADFILE;

	# pega file type (extension) ----------------------------------
	$fileA = $TEMP_DIR."".$doc_file_tmp; # junta caminho com nome do arquivo temporario
	($name,$path,$type_doc) = fileparse($doc_file,qr"\..[^.]*$");

	$doc_data = &timestamp("timestamp"); # pega data
	
	# pega o tamanho do arquivo
	$tamanho=((stat $fileA)[7]);
		if($tamanho==0 || $tamanho=="")
		{ $tamanho=0;}
		
	#Criptografa e Encoda
	$time=time();
	$cript=$fileA.$time;
	$doc_md5 = `echo "$cript" | md5sum -t | cut -d" " -f1`;
	$doc_md5 =~ s/\n//gm;
	$doc_md5 =~ s/\r//gm;
	$doc_md5 =~ s/^\s+//; # ltrim
	$doc_md5 =~ s/\s+$//; # rtrim
	
	

	# [INI] Arquivo, Add  ----------------------------------------------------------------------------------------------------------
	$DB = &DBE("insert into arquivo(data, nome, tipo, descrp, md5, usuario,empresa,tamanho) values ('$doc_data', '$doc_file', '$type_doc', '$doc_descrp', '$doc_md5', '1','1','$tamanho')");

	# Arquivo, get code (id)
	$DB = &DBE("select currval('arquivo_codigo_seq') ");
	$row = $DB->fetch;
	$doc_codigo = @$row[0];
	# [END] Arquivo, Add  ----------------------------------------------------------------------------------------------------------

	#Se for para inserir na tabela do modulo
	if($table ne "" && $field ne "" && $COD ne "" && $action eq "")
		{
		#excessão pois a tabela usuario a coluna: codigo=usuario
		if($table eq "usuario")
			{
			$DB = &DBE("update $table set $field='$doc_md5' where usuario=$COD");
			}
		else
			{
			$DB = &DBE("insert into $table ($colum,$field) values ($COD,'$doc_md5') ");
			}
		}
	
	
		# Cria diretorio se nao existir
		if(length($doc_codigo) == 1) # Controla os 9 primeiros registros
			{
			$folder = substr($doc_codigo,0,1);
			$folder .= 0;
			}
		else
			{ $folder = substr($doc_codigo,0,2); } # pega codigo do documento

		if(! -d $upload_dir."".$folder) # se a pasta nao existir cria
			{ mkdir $upload_dir."".$folder; }

	# Move arquivo e renomeia para pasta final
	rename($fileA, $upload_dir."".$folder."/".$doc_codigo)
	or die ("Erro ao mover o arquivo para pasta final !");

	$nome_tam=length($doc_descrp);
	$nome=$doc_descrp;
	$tamanho=$tamanho/100;
	
	#Verifica o tamanho do nome do arquivo para fazer o slice
	if($nome_tam>30)
		{
		$nome=substr($doc_descrp,0,20)."...";
		}
	#Verifica se for tipo img ou doc
	if(grep(/$type_doc/, @$ext_array))
		{
		$img = "img:'/sys/cfg/DPAC/view_avatar.cgi?MD5=".$doc_md5."',";
		}
		
	$arquivo_upado ="{val:'".$doc_md5."', $img descrp:'<b>Nome:</b> ".$nome." <br> <b>Tamanho:</b> ".$tamanho." KB <br> <b>Tipo:</b> ".$type_doc." ' }";

	if($table eq "usuario")
		{
		$user_img_troca="\$('#user_menu_float_avatar').html(\"<img src='/sys/cfg/DPAC/view_avatar.cgi?MD5=".$doc_md5."'>\");";
		}
	print " <script>
			\$('#upload').fieldUpload('addItem',[$arquivo_upado]);
			
			var FieldUpload = new Array();
			FieldUpload['MD5']='".$doc_md5."';
			FieldUpload['tamanho']='".$tamanho."';
			FieldUpload['tipo']='".$type_doc."';
			FieldUpload['nome']='".$nome."';
			
			$user_img_troca
			
		</script>
		";
	}