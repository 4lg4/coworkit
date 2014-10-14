#!/usr/bin/perl

$nacess = "203' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";

# Dados principais
$ousuario = &get('COD');
$login = lc(&get('login'));
$nome = &get('nome');
$email = &get('email');
$senha = &get('senha');
$empresa = &get('cliente');

$usuario_tipo = &get('tipo_usuario_radio_radios');
if($usuario_tipo eq "")
	{
	$usuario_tipo = "0";
	}
$radios = &get('RADIOS');

if($login eq "" || $nome eq "" || $empresa eq "")
	{
	print $query->header({charset=>utf8});
print<<HTML;
<script language='JavaScript'>
	alerta("Requisição inválida!");
</script>
HTML
	exit;
	}

print $query->header({charset=>utf8});


$dbh->begin_work;
if($ousuario ne "")
	{
	# Update Dados do usuário
	
	$SQL = "update usuario set usuario='$ousuario', login='$login', nome='$nome', email='$email', tipo='$usuario_tipo', empresa='$empresa'";
	if($senha ne "" && $senha ne "não trocar" && $senha ne "no change")
		{
		$SQL .= ", senha=password('$senha')";
		}
	$SQL .= " where usuario = '$ousuario' ";
	
	$rv = &DBE($SQL);
	}
else
	{
	# Insert Dados do usuário

	if($LOGEMPRESA eq "1")
		{
		#$senha = "trunc(((random() * (999999999)::double precision) + (1)::double precision))::varchar || '".$login."'";
		$senha = "trunc(((random() * (999999999)::double precision) + (1)::double precision)) || ".$login;
		$DB = &DBE("select password('$senha')");

		$row = $DB->fetch;
		$senha = @$row[0];
		
		if($senha eq "")
			{
print<<HTML;
<script language='JavaScript'>
	alerta("Falha ao gerar o ID!!!");
</script>
HTML
			$dbh->rollback;
			exit;
			}
		}
	

	$rv = &DBE("insert into usuario (login, nome, email, empresa, tipo, senha, data) values ('$login', '$nome', '$email', '$empresa', '$usuario_tipo', password('$senha'), now()) ");

	}
	
if($ousuario ne "")
	{
	# Exclui direitos
	$rv = &DBE("delete from usuario_menu where usuario = '$ousuario' ");

	for(my $i=1; $i<=$radios; $i++)
		{
		$radio[$i]=&get("radio".$i."_radios");
		$menu[$i]=&get("menu_".$i);
		if($menu[$i] ne "" && $radio[$i] ne "0" && $radio[$i] ne "")
			{
			# Insert o tipo usuario
			$tipo_usuario = &DBE("insert into usuario_menu (usuario, menu, direito) select distinct $ousuario, nacess, '$radio[$i]' from menu where codigo = '$menu[$i]' and nacess is not null ");
			}
		}	
	}


if($ousuario eq "")
	{
	# gera corpo da mensagem completa	
$MSGTEXT=<<END;
<html>
<head>
<title>EOS, boas vindas</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="0">
</head>
<body bgcolor="#dedede" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<center>

<table id="Table_01" width="600" height="736" border="0" cellpadding="0" cellspacing="0">
	<tr>
		<td>
			<img src="http://www.done.com.br/syscall/wizard/img/01.jpg" width="600" height="156" alt=""></td>
	</tr>
	<tr>
		<td>
			<img src="http://www.done.com.br/syscall/wizard/img/02.jpg" width="600" height="67" alt=""></td>
	</tr>
	<tr>
		<td>
			<a href='http://$ENV{'SERVER_NAME'}/sys/wizard/start.cgi?usuario=$usuario&chave=$senha'><img src="http://www.done.com.br/syscall/wizard/img/03.jpg" width="600" height="97" alt="" border=0></a></td>
	</tr>
	<tr>
		<td>
			<img src="http://www.done.com.br/syscall/wizard/img/04.jpg" width="600" height="128" alt=""></td>
	</tr>
	<tr>
		<td>
			<img src="http://www.done.com.br/syscall/wizard/img/05.jpg" width="600" height="129" alt=""></td>
	</tr>
	<tr>
		<td>
			<img src="http://www.done.com.br/syscall/wizard/img/06.jpg" width="600" height="73" alt=""></td>
	</tr>
	<tr>
		<td>
			<img src="http://www.done.com.br/syscall/wizard/img/07.jpg" width="600" height="86" alt=""></td>
	</tr>
</table>

<center>

</body>
</html>
END

	# dados remetente para conexao com servidor de envio
	@SENDER = ('NoReply', 'noreply@done.com.br', 'noreply@done.com.br', '204cacti1001');
	$SUBJECT = "Bem-vindo a Done";

	$result = SENDEMAIL(\@SENDER, $email, $SUBJECT, $MSGTEXT);
	

	if($result ne "")
		{
		$dbh->rollback;
		alerta("<br><br><br><center>ERRO: problemas ao enviar email ! <hr> <br> $result</center>");
		}
	else
		{
		$dbh->commit;
		$msg = "Atualização efetuada com sucesso!<br>E-mail enviado com sucesso para o usuário.";
		}

	# [END]  Envia Email   -------------------------------------------------------------------------------------------------------------
	}
else
	{
	$dbh->commit;
	$msg = "Atualização efetuada com sucesso!";
	}


if($result eq "")
	{
print<<HTML;
<script language='JavaScript'>
	DMessages('$msg', 'Cadastro de usuário');
</script>
HTML
	}
print<<HTML;
</body></html>
HTML


