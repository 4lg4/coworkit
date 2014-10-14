#!/usr/bin/perl


return true;

# [INI]  Funcoes para envio de email ---------------------------------------------------------------------------------------------
# 
#   Dependencias:
#		Implementar OO nesta funcao para ampliar possibilidades de configuracao
#
# 	Opcoes:
# 		$TO = destinatario1@done.com.br,destinatario2@done.com.br,destinatario3@done.com.br # destinatarios separados por virgula
# 		$SUBJECT = Titulo da mensagem
# 		$MSGTEXT = corpo da mensagem
#
# 		$ATTACH = implementar lista de anexos (suporte parcialmente implementado)
# 		$CCO = implementar copia oculta
#
#	Uso:
#		my ($TO, $SUBJECT, $MSGTEXT) = @_;
sub sendmail {
	my ($TO, $SUBJECT, $MSGTEXT) = @_;
	# my ($TO, $SUBJECT, $MSGTEXT, $ATTACH, $CCO) = @_;
	
	# Testa para ver se os dados para envio de e-mail estão completos
	if($USER->{'email'} eq "" || $SUBJECT eq "" || $MSGTEXT eq "" || $TO eq "")
		{
		# Não envia e-mail
		return true;
		}
	
	$MSGTEXT =~ s/'/&#39;/gm;
	
	# Insere no LOG de e-mails, para envio posterior
	$logmail = &DBE("insert into email_historico(usuario, email_conta, de, assunto, msg, status) values ('".$USER->{'usuario'}."', '1', '".$USER->{'email'}."', '$SUBJECT', '$MSGTEXT', '1')");
	
	# Insere os destinatários
	foreach(@$TO)
		{
		&DBE("insert into email_historico_destinatario(email_historico, email) values ('$logmail', '".$_."');");
		}
	
	return true;
	}
# [END]  Funcoes para envio de email  --------------------------------------------------------------------------------------------
