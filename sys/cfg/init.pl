#!/usr/bin/perl
 
use CGI;
# use CGI::Carp qw( fatalsToBrowser );
use DBI;
use Array::Compare; # modulo para comparacao de arrays
#use DBD::Pg;
use Socket;
use Number::Format;
# use URI::Escape;

# DPAC
# export PERL5LIB=/var/www/eos/trunk/sys/       # instala path das bibliotecas EOS no perl
BEGIN
      {
      $this_pwd = $0;
      $this_pwd =~ s/\/sys\/.*/\/sys\//;
      }
use lib $this_pwd."cfg/";			# DPAC EOS Path 
use DPAC::DDialog;                  # DPAC -> DDialog 


#
# configuracao de conexao e do ambiente de trabalho
#
if($ENV{'HTTP_HOST'} =~ /freeze/) {
    require "/etc/done/conn.freeze";

# Demais ambientes
} else {
    require "/etc/done/conn.eos";
}


# 6000 = 100 minutos
$timeout = 6000;
$sname = $ENV{'SCRIPT_NAME'};
$pwd = $ENV{'DOCUMENT_ROOT'};
# $RSITE = "50.19.103.173";
$usuario_empresa = 0;
$usuario_tecnico = 0;
$usuario_cliente = 0;
$show_emp_apelido = 0;
$nome_sys = 'EOS';

$SYS{timeout}      = 6000;
$SYS{server}       = $ENV{'SCRIPT_NAME'};
$SYS{pdf_bg_image} = $ENV{'DOCUMENT_ROOT'}."/img/pdf/coworkit_bg_fade80.jpg"; #imagem bg de arquivos pdf

#$ajax_init = <<END;
#// Código especial para relogon de chamadas ajax
#top.lastcall(arguments.callee.name, arguments);
#END

# [INI] -------------------------------------------------------------------------------------------------------------------------------
# 	Folders
# 		Definicoes das pastas padroes
#
%dir = 
	(
	logon => '/sys/logon/',
	html => '/',
	menu => '/sys/menu/',
	cfg => '/sys/cfg/',
	css => '/css/',
	comum => '/comum/',
	img => '/img/',
	sys => '/sys/',
	relat => '/sys/relat/',
	cadastros => '/sys/cad/default/',
	empresas => '/sys/cad/empresa/',
	empresa => '/sys/cad/empresa/',
	contatos => '/sys/cad/empresa/',
	usuario_tipo => '/sys/cad/usuario_tipo/',
	import => '/sys/import/start.cgi',
	upload => '/sys/upload/',
	senha => '/sys/cad/usuarios/troacasenha.cgi',
	tipo_relacionamento => '/sys/cad/default/',
	chamado => '/sys/chamado/',
	chamadov2 => '/sys/chamadov2/',
	dashboard => '/sys/dashboard/',
	usuario => '/sys/cad/usuarios/',
	faturamento => '/sys/done/faturamento/',
	upload_view => '/sys/DPAC/upload/',
	
	# syscall import
	tipo_grupo_item => 'done/atributo/',
	grupo => 'done/grupo/',
	agrupo => 'done/agrupo/',
	grid => '/sys/done/grid/',
	procede => '/sys/cad/procede/',
	dados_user => 'done/dados_user/',
	dados_ti => 'done/dados_ti/',
	cron => 'done/cron/',
	img_syscall => '/img/syscall/',
	css_syscall => '/css/CSS_syscall/'
	);
# [END] Folders -----------------------------------------------------------------------------------------------------------------------

# variavel $DEV esta dentro de conn.eos se estiver populada ajusta ambiente para desenvolvimento
if($DEV ne "")
	{
	$timeout = 43200;
	}
else
	{
	if(checkislocal($ENV{'REMOTE_ADDR'}) == true)
		{
		# 43200 = 6 horas
		$timeout = 43200;
		}
	}

# Email Config. ------------------------------------	
$smtpServer = "smtp.gmail.com";
$smtpPort = "465"; # SSL
#$smtpPort = "587"; # TLS
$smtpMethod = 'SSL';

$nome_emp = "EOS";
$show_emp_apelido = 1;
$usuario_empresa = 1;
$usuario_tecnico = 1;
$usuario_cliente = 1;
# $conndb = "/etc/done/conn.eos";
$cor1 = "#bfbfbf";
$cor2 = "#f2f2f2";
$dirUpload = "/var/anexos/eos/";
# $homescreen = "201"; # cadastro de clientes
$homescreen = "2"; # Dashboard

# [INI] -------------------------------------------------------------------------------------------------------------------------------
#	ISSUE Config
#		Configuracoes necessarias para uso do modulo issue
# 
$conndbdone = "/etc/done/conn.done";
$dir{'upload_done'} = "/var/anexos/syscall/";
if($pwd =~ /eos/)
	{
	$SISTEMA = "eos";
	}
# [END] ISSUE Config ------------------------------------------------------------------------------------------------------------------
	
# [INI] -------------------------------------------------------------------------------------------------------------------------------
#	Sys MSG
#		Mensagens parao do sistema
#
$msg{salvar} = "O(s) campo(s) devem ser <br> <nobr>preenchido(s) / selecionado(s):</nobr> ";
$msg{excluir} = "Deseja realmente Excluir?  <br><br> Essa opção é irreversível ?";
$msg{cancelar} = "Você tem certeza que deseja cancelar? <br><br> Todos os dados modificados serão perdidos!";
$msg{db_insert} = "Falha ao Inserir";
$msg{db_select} = "Falha ao Selecionar";
$msg{db_update} = "Falha ao Alterar";
$msg{db_delete} = "Falha ao Deletar";
# $msg{} = "";
# [END] Sys MSG -----------------------------------------------------------------------------------------------------------------------

# datas translate  -------------------------------
# Meses do ano
$DATA_MES[1] = "Janeiro";
$DATA_MES[2] = "Fevereiro";
$DATA_MES[3] = "Março";
$DATA_MES[4] = "Abril";
$DATA_MES[5] = "Maio";
$DATA_MES[6] = "Junho";
$DATA_MES[7] = "Julho";
$DATA_MES[8] = "Agosto";
$DATA_MES[9] = "Setembro";
$DATA_MES[10] = "Outubro";
$DATA_MES[11] = "Novembro";
$DATA_MES[12] = "Dezembro";

$DATA_MES_MIN[1] = "Jan";
$DATA_MES_MIN[2] = "Fev";
$DATA_MES_MIN[3] = "Mar";
$DATA_MES_MIN[4] = "Abr";
$DATA_MES_MIN[5] = "Mai";
$DATA_MES_MIN[6] = "Jun";
$DATA_MES_MIN[7] = "Jul";
$DATA_MES_MIN[8] = "Ago";
$DATA_MES_MIN[9] = "Set";
$DATA_MES_MIN[10] = "Out";
$DATA_MES_MIN[11] = "Nov";
$DATA_MES_MIN[12] = "Dez";

$DATA_SEMANA[1] = "Segunda-Feira";
$DATA_SEMANA[2] = "Terça-Feira";
$DATA_SEMANA[3] = "Quarta-Feira";
$DATA_SEMANA[4] = "Quinta-Feira";
$DATA_SEMANA[5] = "Sexta-Feira";
$DATA_SEMANA[6] = "Sábado";
$DATA_SEMANA[7] = "Domingo";

# monta estrutura de diretorios locais ------ 
%ldir = ();
while(my ($key, $value) = each(%dir))
	{
	$ldir{$key} = $pwd.$value;
	}
$ldir{'upload'} = $dirUpload; # override local dir for upload

require $ldir{'cfg'}."db.pl";
require $ldir{'logon'}."valida.pl";

# funcao para pegar variaveis de formulario e transformar em locais
sub get
	{
	my ($key,$type) = @_;
	
	# TYPE for vazio pega variaveis get ou post 
	if($type eq "")	{ $key = $query->param($key); }
		
	if($key =~ /["'\\;]/)
		{
		$key =~ s/"/&quot;/gm;
		$key =~ s/'/&#39;/gm;
		$key =~ s/\\/&#92;/gm;
        # $key =~ s/;/\*\*\*\*/gm;
		}
	# transforma quebras de linha em <br> para salvar no banco
	if(lc($type) eq "html")	
		{ $key =~ s/\r|\n/<br>/gm; }
	elsif($type eq "NEWLINE") 
		{ $key =~ s/\r|\n//gm; }
	elsif($type eq "NEWLINE_SHOW") 
		{ $key =~ s/\r|\n/ /gm; }
		
	# corrige erro Undefined javascript
	if($key eq "undefined")
		{ $key = ""; }
		
	return $key;
	}
	
# funcao para pegar ARRAY variaveis de formulario e transformar em locais	
sub get_array
	{
	my ($key) = @_;
	@key_array = $query->param($key);
	for(@key_array)
		{
		s/"/&quot;/gm;
		s/'/&#39;/gm;
		s/\\/&#92;/gm;
		}
	return @key_array;
	}
	
# funcao para traducao
# modificar elseif em array ou case ! (future) :p
sub traduz
	{
	my ($key) = @_;
	if($key eq "codigo")
	    {
	    return "Código";
	    }
	elsif($key eq "descrp")
	    {
	    return "Descrição";
	    }
	elsif($key eq "dt_open")
	    {
	    return "Data Abertura";
	    }
	elsif($key eq "usuario")
	    {
	    return "Usuário";
	    }
	elsif($key eq "tecnico")
	    {
	    return "Técnico";
	    }
	elsif($key eq "dt_close")
	    {
	    return "Data Conclusão";
	    }
	elsif($key eq "uf")
	    {
	    return "Estado";
	    }
	else
	    {
	    return ucfirst($key);
	    }
	}
	
# Vefirica se o IP é do escritório da Done
sub checkislocal
	{
	my ($ip) = @_;
	
	eval 
		{
		$addr_done[0] = inet_ntoa(inet_aton('office.done.com.br'));
		$addr_done[1] = inet_ntoa(inet_aton('office.donedns.com.br'));
		$addr_done[2] = inet_ntoa(inet_aton('sdone.donedns.com.br'));
		
		for($f=0;$f<@addr_done;$f++)
			{
			if($ip eq $addr_done[$f])
				{
				return true;
				}
			}
		};
	return false;
	}

# [INI]  Funcoes para envio de email ---------------------------------------------------------------------------------------------
# 
#   Dependencias:
#		Implementar OO nesta funcao para ampliar possibilidades de configuracao
#
# 	Opcoes:
#		$SENDER = @SENDER = ( Remetente, E-mail, Usuario SMTP, Senha SMTP ); # array com dados de SMTP para envio
# 		$TO = destinatario1@done.com.br,destinatario2@done.com.br,destinatario3@done.com.br # destinatarios separados por virgula
# 		$SUBJECT = Titulo da mensagem
# 		$MSGTEXT = corpo da mensagem
#
# 		$ATTACH = implementar lista de anexos (suporte parcialmente implementado)
# 		$CCO = implementar copia oculta
#
#	Uso:
#		my ($SENDER, $TO, $SUBJECT, $MSGTEXT) = @_;
sub SENDEMAIL
	{
	my ($SENDER, $TO, $SUBJECT, $MSGTEXT) = @_;
	# my ($SENDER, $TO, $SUBJECT, $MSGTEXT, $ATTACH, $CCO) = @_;
		
	$FROMNOME    = $SENDER[0];
	$FROM        = $SENDER[1];
	$smtpUser    = $SENDER[2];
	$smtpUserPwd = $SENDER[3];
    
    # ajusta password sender
    if(lc($FROMNOME) eq "noreply") {
        $FROM        = "noreply\@done.com.br";
        $smtpUser    = "noreply\@done.com.br";
        $smtpUserPwd = "204cacti1001";
    }
    
	# debug("$FROMNOME - $FROM - $smtpUser - $smtpUserPwd");
    # return;
	
	# carrega extensao necessaria para funcionamento
	if($smtpMethod eq "TLS") 
		{ 
		use Net::SMTP::TLS; 
		if(not $mailer = new Net::SMTP::TLS($smtpServer, Port=>$smtpPort, Timeout => 30, Debug => 1))
			{
			return "Não foi possível se conectar no servidor";
			}
		}
	else
		{
		use Net::SMTP::SSL; 
		if(not $mailer = new Net::SMTP::SSL($smtpServer, Port=>$smtpPort, Timeout => 30, Debug => 1))
			{
			return "Não foi possível se conectar no servidor";
			}
		}

	# Autentica no servidor SMTP
	if(not $mailer->auth($smtpUser, $smtpUserPwd))
		{
		return "Erro na autenticanção do usuário $smtpUser<br>$@";
		}

	# Definindo o remetente
	if(not $mailer->mail($FROM))
		{
		return "Erro no remetente $FROM<br>$@";
		}

	$TO =~ s/;/,/gm;
	$TO =~ s/,\s+/,/gm;
	my @to = split(",",$TO);

	# Definindo o destinatário
	if(not $mailer->to(@to))
		{
		return "Erro no destinatario $TO<br>$@";
		}

	# Iniciando comunicação
	if(not $mailer->data())
		{
		return "Erro ao inicializar mensagem<br>$@";
		}

	# Definindo os cabeçalhos do e-mail
	$mailer->datasend("From: $FROMNOME <".$FROM.">\n");
	$mailer->datasend("To: $TO\n");
	$mailer->datasend("Reply-To: $FROM\n");
	$mailer->datasend("Errors-To: $FROM\n");
	$mailer->datasend("Subject: $SUBJECT\n");
	$mailer->datasend("Content-Type: text/html\n");
	$mailer->datasend("\n");

	# Enviando texto
	if(not $mailer->datasend("$MSGTEXT \n"))
  		{
		return "Erro ao anexar mensagem<br>$@";
		}

	# Encerrando conexão
	$mailer->dataend();
	$mailer->quit;
    
	return;
	}
# [END]  Funcoes para envio de email  --------------------------------------------------------------------------------------------

#
#   Array unico
#       remove duplicados de um array
#
sub uniq {
    return keys %{{ map { $_ => 1 } @_ }};
}

# --------------------------------------------------------------------------------------------------------------------------------
#   Funcoes para ajuste de hora 
# --------------------------------------------------------------------------------------------------------------------------------

# Pega time stamp atual -----------------------------			
# timestamp("timestamp") 
#	= 2011-10-21 12:27:43
# $TES = timestamp("date");
#	= 2011-10-21
# $TEST = timestamp("time");
#	= 12:27:43
# $POG = timestamp();
# 	$POG->{hour}
#		= 12
sub timestamp
	{ 
	my ($db_save) = @_;
	
	($sec,$min,$hour,$day,$mo,$year,$wday,$YD,$ISDST)=localtime(time);
	$year += 1900; # ajusta ano corrente
	$mo ++; # ajusta mes corrente
	if($hour < 10) { $hour = "0".$hour; }
	if($min < 10) { $min = "0".$min; }
	if($sec < 10) { $sec = "0".$sec; }
	if($mo < 10) { $mo = "0".$mo; }
	if($day < 10) { $day = "0".$day; }
	
	$timestamp->{hour} = $hour;
	$timestamp->{minute} = $min;
	$timestamp->{second} = $sec;		
	$timestamp->{day} = $day;
	$timestamp->{month} = $mo;
	$timestamp->{year} = $year;
	$timestamp->{wday} = $wday;
	
	# ajusta para lower case
	$db_save = lc($db_save);
	
	if($db_save eq "timestamp" || $db_save eq "")
		{
		$datenow = $timestamp->{year}."-".$timestamp->{month}."-".$timestamp->{day}." ".$timestamp->{hour}.":".$timestamp->{minute}.":".$timestamp->{second};
		return $datenow;
		}
	elsif($db_save eq "comparison") 
		{
		$datenow = $timestamp->{year}."".$timestamp->{month}."".$timestamp->{day}."".$timestamp->{hour}."".$timestamp->{minute}."00";
		return $datenow;
		}
	elsif($db_save eq "time") 
		{
		$datenow = $timestamp->{hour}.":".$timestamp->{minute}.":".$timestamp->{second};
		return $datenow;
		}
	elsif($db_save eq "date") 
		{
		$datenow = $timestamp->{year}."-".$timestamp->{month}."-".$timestamp->{day};
		return $datenow;
		}
	elsif($db_save eq "yearmonth") 
		{
		return $timestamp->{year}."-".$timestamp->{month};
		}
	elsif($db_save eq "yearmonth-br") 
		{
		return $timestamp->{month}."/".$timestamp->{year};
		}
	elsif($db_save eq "year") 
		{
		return $timestamp->{year};
		}
	elsif($db_save eq "month") 
		{
		return $timestamp->{month};
		}
	elsif($db_save eq "day") 
		{
		return $timestamp->{day};
		}
	elsif($db_save eq "week") 
		{
		# implementar retorno do dia inicial e do dia final da semana ex 0112 (janeiro dia 12)
		# $hoje = $timestamp->{day};		
		# $dom = $hoje - $timestamp->{wday};
		# $datenow = {'INI' => $ini, 'FIM' => $fim };
		return $timestamp->{wday};
		}
	elsif($db_save eq "br" || $db_save eq "human") 
		{
		$datenow = $timestamp->{day}."/".$timestamp->{month}."/".$timestamp->{year}." ".$timestamp->{hour}.":".$timestamp->{minute};
		return $datenow;
		}
		
	return $timestamp;
	}
	
	
# Ajusta data para salvar -----------------------------			
sub dateToSave
	{ 
	my ($data,$only) = @_;
	
	$data =~ s/^\s+//; # ltrim
	$data =~ s/\s+$//; # rtrim	
	$size = length($data); # pega tamanho
	# print "<hr> $size *** ".$data;  # DEBUG ------------------------	
	if($size == 0)  # vazio
		{ $data = NULL; }
	elsif($size == 5)  # somente tempo
		{ $data .= ":00"; }
    elsif($size == 7){ # mes ano
	    $m = substr($data, 0, 2);
	    $a = substr($data, 3, 4);        
        $data = $a."-".$m;
    }   
	elsif($size == 10)  # somente data
		{
		$d = substr($data, 0, 2);
		$m = substr($data, 3, 2);
		$a = substr($data, 6, 4);
		
		$data = $a."-".$m."-".$d;
		
		# se for para mostrar somente a data formatada para salvar no banco
		if(uc($only) ne "DATE")
			{ $data .= " 00:00:00"; }
		}
	elsif($size > 10)  # time stamp
		{
		$d = substr($data, 0, 2);
		$m = substr($data, 3, 2);
		$a = substr($data, 6, 4);
		$h = substr($data, 11, 5);	
		$data = $a."-".$m."-".$d." ".$h.":00";
		}
		
	if(uc($only) eq "YEARMONTH")
		{ $data = $a."-".$m; }
	# adiciona container (aspas) na data para salvamento no banco de dados ex '2013-00-00 00:00:00' se nao for vazio
	elsif(uc($only) eq "CONTAINER")
		{
		if($size > 0)
			{
			$data = "'$data'";	
			}
		}
		
	# print "<hr> $size *** ".$data;  # DEBUG ------------------------
	return $data;
	}

# Ajusta data para mostrar -----------------------------			
sub dateToShow
	{ 
	my ($data,$only) = @_;
	
	$data =~ s/^\s+//; # ltrim
	$data =~ s/\s+$//; # rtrim	
	$data = substr($data, 0,-3); # remove segundos da data	
	# print "<hr>".$data; # DEBUG ----------------------------	
	$size = length($data); # pega tamanho		
	
    $only = uc($only);
    
	if($size > 15)  # time stamp
		{
		$a = substr($data, 0, 4);
		$m = substr($data, 5, 2);
		$d = substr($data, 8, 2);
		$h = substr($data, 11, 5);	
		$hs = substr($data, 11, 2);	
		$mi = substr($data, 14, 2);	
		$data = $d."/".$m."/".$a;
		$yearmonth = $m."/".$a;
		if($only eq "") 
			{ $data .= " ".$h; }
		elsif($only eq "COMPARISON") # $data =~ s/\s//g; # remove spaces
			{ $data = $a.$m.$d.$hs.$mi."00"; }
		elsif($only eq "HOUR")
			{ $data = $hs; }
		elsif($only eq "MINUTE")
			{ $data = $m; }
		elsif($only eq "DATE")
			{ $data = $data; }
		elsif($only eq "YEAR")
			{ $data = $a; }
		elsif($only eq "MONTH")
			{ $data = $m; }
		elsif($only eq "DAY")
			{ $data = $d; }
		elsif($only eq "YEARMONTH" || $only eq "MONTHYEAR")
			{ $data = $yearmonth; }
		}
	# trata tempo vindo do banco
	elsif($size	== 8 || $size	== 5)
		{
		$h = substr($data, 0, 2);	
		$hs = substr($data, 3, 2);
		$data = $h.":".$hs;
		}
	# retorna mascara se for definido
	else
		{
		if($only eq "TIME")
			{
			if($size == 9 || $size == 6)
				{
				$h = substr($data, 0, 3);	
				$hs = substr($data, 4, 2);
				$data = $h.":".$hs;				
				}
			else
				{
				$data = "00:00";
				}
			}
		}
	# elsif($data eq "")
	#	{
	#	$data = "0";
	#	}
	# print "<hr> $size *** ".$data;  # DEBUG ------------------------	
	return $data;
	}
	
# pega data do banco se necessario
sub dateFromDB
	{ 
	my ($periodo,$sinal,$mask,$qtd,$data) = @_;
	
	# Data, se nao setada data pega data atual do banco de dados
	if($data eq "")
		{ $data = "(CURRENT_TIMESTAMP(0))"; }
	else
		{ $data = "'$data'"; }
	
	# Mascara, se nao setado ajusta para 'YYYY-MM-DD 00:00:00'
	if($mask eq "")
		{ $mask = "YYYY-MM-DD 00:00:00"; }
		
	# quantidade, se nao setado ajusta para 1 a quantidade do periodo
	if($qtd eq "")
		{ $qtd = 1; }
	
	
	
	$sth = &select("select to_char(date ".$data." $sinal interval '$qtd $periodo', '$mask') as data_");
	$x = $sth->fetchrow_hashref;
	return $x->{data_};
	}

# [INI] Money Format  -----------------------------------------------------------------------------------------------------
sub money
	{ 
	my ($val,$calc) = @_;
	# corrige quantidade para 2 casas apos virgula
	# $val = sprintf("%.2f", $val);
	$val =~ s/R\$//g;

	if($calc eq "")
		{
		# configura apresentacao do numero
		my $real = new Number::Format(
			-thousands_sep   => '.',
		    -decimal_point   => ',',
			-decimal_digits	 => 2,
			-int_curr_symbol => 'R\$ ');
		
	 	# retorna numero formatado
		# return $real->format_number($val);
	
		$val = $real->format_picture($val,'R\$ ###.###.###,##');	
		}
	elsif($calc eq "xls")
		{
		return $val;
		}
	else
		{
		$val =~ s/\.//g;
		$val =~ s/\,/\./g;
		}	
		
	return $val;
	}
# [END] Money Format  -----------------------------------------------------------------------------------------------------

# [INI] Percentage Format  -----------------------------------------------------------------------------------------------------
sub percentage
	{ 
	my ($val,$casas,$sep) = @_;

	if($casas eq "") { $casas = ","; }
	if($sep eq "") { $sep = 2; }

	my $format = new Number::Format(
	    -decimal_point   => $casas,
		-decimal_digits	 => $sep
		);
		
	return $format->format_number($val);
	}
# [END] Percentage Format  -----------------------------------------------------------------------------------------------------

# [INI] isNumber  -----------------------------------------------------------------------------------------------------
#
# true / false
# ---------------------------------------------------------------------------------------------------------------------
sub isNumber
	{
	my ($num,$type) = @_;
	
	if($num =~ /^\d+$/)
		{ 
		return true;
		}
	else
		{ 
		return false;
		}
		
	# if (/\D/)            { print "has nondigits\n" }
	# if (/^\d+$/)         { print "is a whole number\n" }
	# if (/^-?\d+$/)       { print "is an integer\n" }
	# if (/^[+-]?\d+$/)    { print "is a +/- integer\n" }
	# if (/^-?\d+\.?\d*$/) { print "is a real number\n" }
	# if (/^-?(?:\d+(?:\.\d*)?&\.\d+)$/) { print "is a decimal number\n" }
	# if (/^([+-]?)(?=\d&\.\d)\d*(\.\d*)?([Ee]([+-]?\d+))?$/)
	#                      { print "a C float\n" }	
	}
# [END] isNumber  -----------------------------------------------------------------------------------------------------

# [INI] ucfirstall  -------------------------------------------------------------------------------------------------------
#  ucfirstall = Uper Case all First = Transforma todas as primeiras letras da string em MAIUSCULAS
# ** adicionar inteligencia ex. se for de nao usar De se for a nao usar A entre palavras (conjuncoes)
# -------------------------------------------------------------------------------------------------------------------------
sub ucfirstall
	{ my ($str) = @_;
	$str = lc($str);
	$str =~ s/\b(\w+)\b/ucfirst($1)/ge;
	return $str;
	}
	
sub slimit
	{ my ($str, $qtd, $spacer) = @_;
	
	# quebra string e adiciona final com ...
	if(length($str) > $qtd)
		{
		$str = substr($str, 0, $qtd);
		
		if($spacer eq "")
			{
			$str .= "...";
			}
		else
			{
			$str .= $spacer;
			}
		}
		
	return $str; 
	}
# [END] ucfirstall  -------------------------------------------------------------------------------------------------------

# [INI] Alerta ---------------------------------------------------------------------------------------
# 		usado em conjunto com ui.js / alerta 
# 	$text = texto do alerta (HTML)
# 	$stop = para execucao do script se selecionado
# ----------------------------------------------------------------------------------------------------
sub alerta
	{ my ($text,$stop) = @_;
		
	print "<script>alerta(\"".$text."\");</script>";
		
	if($stop ne "")
		{ 
		exit; 
		}
	}
# [END] Alerta ---------------------------------------------------------------------------------------

# [INI] Debug enviroment  -------------------------------------------------------------------------------------------------
sub debug
	{ my ($text,$stop) = @_;
	
    $text =~ s/\r|\n/ /gm; # remove quebras de linhas
    
	print "<hr style='background:red; border:red;'>".(timestamp("human"))." -> ".$text."<hr style='background:red; border:red;'>".$campos."<hr style='background:red; border:red;'>";
	print "<script>console.log(\"".(timestamp("human"))." -> ".$text."\");</script>";
    
    if($stop ne "nofields"){
    	# lista todos os campos para o debug
    	@campo = $query->param();
    	for($f=0;$f<@campo;$f++)
    		{
    		$campos .= "#".$campo[$f]." => ".&get($campo[$f])." <br>";
    		}
	
    	print "<script>console.log(\"".(timestamp("human"))." -> ".$campos."\");</script>";
    }
    
    if($stop eq "nofields"){
        $stop = "";
    }
		
	if($stop ne "")
		{ exit; }
	}
# [END] Debug enviroment  -------------------------------------------------------------------------------------------------

# [INI] Log Salva  --------------------------------------------------------------------------------------------------------
sub logger
	{ ($TABELA,$ACAO,$DESCRP) = @_;
		
	# ajusta aspas para salvar no banco
	$DESCRP =~ s/"/&quot;/gm;
	$DESCRP =~ s/'/&#39;/gm;
	
	# insere dados
	$dbh->do("insert into logger(data, usuario, tabela, acao, descrp) values ('".&timestamp("timestamp")."', '$USER->{usuario}', '$TABELA', '$ACAO', '$DESCRP')");
	
	# se erro
	if($dbh->err ne ""){ &erroDBH($msg{db_insert}." Logger !"); $dbh->rollback; exit; }
	}
# [INI] Log Salva  --------------------------------------------------------------------------------------------------------

# [INI] URL ENCODE/DECODE  -------------------------------------------------------------------------------------------------------
#
# 	Passa um string em md5 e criptografa codigos para passar em URL
#
# -------------------------------------------------------------------------------------------------------------------------

#Decodifica
sub URLDecode
	{
	my $theURL = $_[0];
	$theURL =~ tr/+/ /;
	$theURL =~ s/%([a-fA-F0-9]{2,2})/chr(hex($1))/eg;
	$theURL =~ s/<!--(.|\n)*-->//g;
	return $theURL;
	}
	
#Codifica
sub URLEncode 
	{
	my $theURL = $_[0];
	$theURL =~ s/([\W])/"%" . uc(sprintf("%2.2x",ord($1)))/eg;
	return $theURL;
	}
# [END] URL ENCODE/DECODE  ----------------------------------------------------------------------------------------------------------

# [INI] Vars Check  -------------------------------------------------------------------------------------------------------
#
# 	Teste de consistencia dos dados do formulario
#
# -------------------------------------------------------------------------------------------------------------------------
sub varsCheck
	{ ($valida) = @_;
	
	if(!$valida)
		{
		if($COD eq "" && $MODO ne "incluir")
			{ $valida = 1; }
		else
			{ $valida = 0; }
		}
		
	if($valida eq 1)
		{
		print $query->header({charset=>utf8});
		print "	<script>
					top.alerta('Requisição inválida!');
					top.unLoading();
				</script>";
		exit;
		}
	}
# [END] Vars Check  ----------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------
#   geraLista / gera select apartir da tabela especifica
# --------------------------------------------------------------------------------------------------------------------------------
# imprime na tela o array ja pronto
# print geraLista("caixa_tipo","descrp","tipo_caixa");
# 
# popula em uma variavel para posterior impressao
# $caixa_tipo = geraLista("caixa_tipo","descrp","tipo_caixa");
#		
# sub geraLista
# 	{ ($table,$chave,$select) = @_;
# 
# 	$n = 0;
# 	$SQL = "select * from $table order by $chave asc";
# 	$sth = &select($SQL);
# 	$rv = $sth->rows();
# 	# cria array  
# 	$R = " \n var ".$select."_cod = new Array(); \n var $select = new Array(); \n";
# 	while($row = $sth->fetchrow_hashref)
# 		{
# 		$R .= $select."_cod[$n] = \"$row->{'codigo'}\"; \n";
# 		$R .= $select."[$n] = \"".ucfirst($row->{$chave})."\"; \n";
# 		$n++;
# 		}
# 	return $R;
# 	}




# funcoes touch
# require "./DPAC/DTouchRadio.pl";

# [INI] DTouchRadio ----------------------------------------------------------------------------------------------------------------------
#	Usada juntamente com a funcao jquery DTouchRadio (/comum/DPAC/DTouchRadio.js)
#	Cria elementos radio com imagens e touch
#	
#	uso
#		$chamado_tipo .= DTouchRadio($t->{codigo},Nome do Campo,$t->{img},$t->{descrp});
# 	retorno
# 		"<div><input type='radio' name='chamado_tipo' value='$t->{codigo}' /><img src='$t->{img}' /><span>$t->{descrp}</span></div>"

sub DTouchRadio
	{ my ($field,$codigo,$descrp,$imagem) = @_;
	
	# Vertical (se nao tiver imagem)
	if($imagem eq "")
		{
		$retorno = "<div><input type='radio' name='".$field."' value='".$codigo."' /><span>".$descrp."</span></div>";
		}
		
	# Horizontal
	else
		{
		$retorno = "<div><input type='radio' name='".$field."' value='".$codigo."' /><img src='".$imagem."' /><span>".$descrp."</span></div>";
		}
	
	return $retorno;
	}

sub DTouchList
	{ my ($field,$codigo,$descrp,$imagem) = @_;
	
	# Vertical (se nao tiver imagem)
	if($imagem eq "")
		{
		$retorno = "<div><input type='text' name='DTouchList_".$field."' value='".$codigo."' /><span>".$descrp."</span></div>";
		}
		
	# Horizontal
	else
		{
		$retorno = "<div><input type='text' name='DTouchList_".$field."' value='".$codigo."' /><img src='".$imagem."' /><span>".$descrp."</span></div>";
		}
	
	return $retorno;
	}
# [END] DTouchRadio ----------------------------------------------------------------------------------------------------------------------


#
#   Run
#       run javascript code
#
sub Js {
    my ($code) = @_;
    
    print $code;
}


