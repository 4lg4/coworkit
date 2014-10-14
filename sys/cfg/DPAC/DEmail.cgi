#!/usr/bin/perl
require "../init.pl";

#
#   DEmail
#       DEmail.cgi
#
#       envio de emails
#

# pega variaveis
$ID           = &get("ID");    # ID do usuario logado
$destinatario = &get("destinatario");
$title        = &get("title");
$message      = &get("message");

$sender[0] = $USER->{'nome'};
$sender[1] = $USER->{'email'};
$sender[2] = '1';


# header 
# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

debug();
exit;

# se nao tiver ID
if(!$ID){
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "error", ';
    $R .= '     "message" : "Você não pode enviar emails" ';
    $R .= '}  ';
    print $R;
    
    exit;
}

# template mensagem
# require "../template/users.pl";


# lista todos os campos para o debug
@campo = $query->param();
for($f=0;$f<@campo;$f++) {
	$campos .= "#".$campo[$f]." => ".&get($campo[$f])." <br>";
}

# adiciona variaveis de ambiente 
$message .= "<hr style='background:red; border:red;'>".(timestamp("human"))." -> ".$text."<hr style='background:red; border:red;'>".$campos."<hr style='background:red; border:red;'>";


$message =~ s/(\n|\r)/<br>/gm;

# 
#   Finaliza
#
if(! SENDEMAIL(\@sender, $destinatario, $title, $message)){ # erro desfaz tudo
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "error", ';
    $R .= '     "message" : "Erro ao enviar o email" ';
    $R .= '}  ';
    print $R;
    
    exit;
} 

# mensagem
$R  = '{ ';
$R .= '     "status"  : "success", ';
$R .= '     "message" : "Email enviado" ';
$R .= '}  ';
print $R;

exit;




# [INI]  Funcoes para envio de email ---------------------------------------------------------------------------------------------
# 
#   Dependencias:
#		Implementar OO nesta funcao para ampliar possibilidades de configuracao
#
# 	Opcoes:
#		$SENDER = @SENDER = ( Remetente, E-mail, Conta SMTP ); # array com dados de SMTP para envio
# 		$TO = destinatario1@done.com.br,destinatario2@done.com.br,destinatario3@done.com.br # destinatarios separados por virgula
# 		$SUBJECT = Titulo da mensagem
# 		$MSGTEXT = corpo da mensagem
#
# 		$ATTACH = implementar lista de anexos (suporte parcialmente implementado)
# 		$CCO = implementar copia oculta
#
#	Uso:
#		my ($SENDER, $TO, $SUBJECT, $MSGTEXT) = @_;
sub SENDEMAIL {
	my ($SENDER, $TOT, $SUBJECT, $MSGTEXT) = @_;
	# my ($SENDER, $TO, $SUBJECT, $MSGTEXT, $ATTACH, $CCO) = @_;
		
	$FROMNOME    = $SENDER[0];
	$FROM        = $SENDER[1];
	$CONTA    = $SENDER[2];
	
	# Se não estiver no novo padrão, envia como No-Reply Done
	if($CONTA != /^\d+$/)
	      {
	      $CONTA = '1';
	      }
	
	# Converte lista de e-mails para matriz
	if($TOT =~ /,/)
	      {
	      $TOT =~ s/,/;/gm;
	      }
	if($TOT =~ /\s+/)
	      {
	      $TOT =~ s/\s+//gm;
	      }
	@TO = split(";",$TOT);

	
	# inicia SQls execs
	$dbh->begin_work;
	
	# Insere no LOG de e-mails, para envio posterior
	$logmail = &DBE("insert into email_historico(usuario, conta, de, assunto, msg, status) values ('$USER->{'usuario'}', '$CONTA', '$FROM', '$SUBJECT', '".&get($MSGTEXT, 'HTML')."')");
	
	# Insere os destinatários
	foreach(@TO)
		{
		&DBE("insert into email_historico_destinatario(email_historico, email) values ('$logmail', '".$_."');
		}
	
	# finaliza SQLs
	$dbh->commit;	

	return true;
	}
# [END]  Funcoes para envio de email  --------------------------------------------------------------------------------------------





package DEmail;

sub new {
    
    my $opt  = shift; 
    my $self = {
        destinatario => shift || 'alert',
        message      => shift || 'Teste: Janela de Dialogo',
		title        => shift || 'Aviso'
    };
    
    bless $self, $opt; # popula variaveis
        
    # monta janela de dialogo
	print " <script>                
                \$.DDialog({ 
                    type      : \"$self->{type}\",
                    message   : \"$self->{message}\",
                    title     : \"$self->{title}\",
            		resizable : \"$self->{resizeable}\",
            		draggable : \"$self->{draggable}\"
                });
            </script>";
    
    # se for para interromper o script	
	if($self->{stop} eq true) { 
		exit; 
	}
}

1;



