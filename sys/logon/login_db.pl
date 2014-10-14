#!/usr/bin/perl


return true;

sub say
	{
	($msg, $field) = @_;

	# suporte para login mobile
	if($MOBILE ne "")
		{
		print "alert('$msg');";
		}
	else
		{
		print "	top.unLoading();\n";
		
		# se for definido o campo de focus, move para ele
		if($field ne "")
			{
print<<HTML;
<script>
				try
					{
					if(document.forms[0].$field.value)
						{
						top.alerta('<br>$msg', 'document.forms[0].$field.focus(); document.forms[0].$field.select();');
						}
					}
				catch(err)
					{
					try
						{
						if(top.document.forms[0].$field.value)
							{
							// top.alerta('<br>$msg', 'top.document.forms[0].$field.focus(); top.document.forms[0].$field.select();');
                            top.DDialog('$msg', '$field');
							}
						}
					catch(err)
						{
						try
							{
							if(corpo.document.logon.$field.value)
								{
								top.alerta('<br>$msg', 'corpo.document.logon.$field.focus(); corpo.document.forms[0].$field.select();');
								}
							}
						catch(err)
							{
							try
								{
								if(\$('#relogin_form input[name=$field]').val())
									{
									alerta('<br>$msg', '\$("#relogin_form input[name=$field]").focus(); \$("#relogin_form input[name=$field]").select();');
									}
								}
							catch(err)
								{
								// sem foco no campo
								try
									{
									top.alerta('$msg');
									}
								catch(err)
									{
									alert('$msg');
									}
								}
							}
						}
					}
</script>
HTML
			}
		else
			{
			print "top.alerta('<br>$msg');";
			}
		}
	}


# verifica usuario 
sub check_login {
    
    if($USER{fb_id} && $USER{fb_login}) {
        
        $sql = "select * from usuario_login as ul join usuario as u on u.usuario = ul.usuario where ul.login = '$USER{fb_login}' and ul.id = '$USER{fb_id}'";
        
        
    } else {
    
    
    	# Inicia a montagem do SQL
    	$sql = "select * from usuario where (login = '$USER{USUARIO}' ";
  
    	# Atendendo pedido de só precisar informar primeira parte do e-mail, quando o cliente estiver selecionada
    	if($USER{USUARIO} !~ /\@/)
    		{
    		if($USER{EMPRESA} ne "")
    			{
    			$sql .= " or login ilike '$USER{USUARIO}\@%' ";
    			}
    		}
    	# else
    	#	{
    	#	$sql .= " or email = '$USER{USUARIO}' ";
    	#	}
    	$sql .= " ) ";

    	# Não permite acesso a usuários bloqueados
    	$sql .= " and (bloqueado is null or bloqueado = '0') ";

    	# Restringe a empresa, caso esteja selecionada
    	if($USER{EMPRESA} ne "")
    		{
    		$sql .= " and empresa = $USER{EMPRESA} ";
    		}
    	# Se não escolher a empresa verifica se tem mais de um usuário com o mesmo login
    	else
    		{
    		$sth = &DBE($sql);
    		if($sth->rows() > 1)
    		      {
    		      # No caso de retornar mais de um usuário
    		      &say("Não foi possível determinar o seu usuário!<br>Por favor, informe o seu e-mail completo no usuário...", "username");
    		      return "";
    		      }
    		}


    	# Verifica se está usando a senha master. Se não estiver, verifica a senha do banco
    	if($SENHA ne $MASTERPASS)
    		{
    		$sql .= " and senha = password('$SENHA') ";
    		}
    }
    
	# Testa se o usuário e a senha estão corretos, pelo SQL montado
	$sth = &DBE($sql);


	# verifica a quantidade de linhas retornadas
	$rv = $sth->rows();
	if($rv == 1)
		{
		$row = $sth->fetchrow_hashref;
		# seta nome completo do usuario
		$USER{USUARIO} = $row->{'usuario'};
		$USER{NOME}    = $row->{'nome'};
		$USER{EMPRESA} = $row->{'empresa'};

		# Atualiza o idioma utilizado (não utilizando atualmente)
		# if($IDIOMA ne "")
		# 	{
		# 	if($SENHA ne $MASTERPASS)
		# 		{
		# 		$rv = $dbh->do("update usuario set idioma='$IDIOMA' where login = '$FRMUSUARIO' and senha = password('$SENHA')");
		# 		}
		# 	if($dbh->err ne "")
		# 		{
		# 		&say("Falha ao atribuir idioma no Login!!!");
		# 		}
		# 	}

		# Verifica se o ID está setado
		if($ID ne "") {
            
			$sth = &DBE("
                select 
                    id 
                from 
                    usuario_logado 
                where 
                    usuario = '$USER{USUARIO}' and 
                    id      = '$ID' and 
                    ip      = '$IP' 
                order by 
                    fim 
                desc 
            ");
            
			if($rv = $sth->rows > 0) {
                
				$row = $sth->fetchrow_hashref;
				$ID = $row->{'id'};
				$rv = $dbh->do("update usuario_logado set fim=now() where id='$ID' and ip = '$IP'");
				if($dbh->err ne "") {
					&say("Falha em atualizar o log no Login!!!");
				}
    
		    } else {
                
				# Verifica se é um dos IPs do escritório
				if(checkislocal($ENV{'REMOTE_ADDR'}) == true) {
                    
					$sth = &DBE("select id from usuario_logado where usuario='$USER{USUARIO}' and id='$ID' order by fim desc ");
					if($rv = $sth->rows > 0) {
						$row = $sth->fetchrow_hashref;
						$ID = $row->{'id'};
						$rv = $dbh->do("update usuario_logado set fim=now() where id='$ID' and ip = '$ENV{'REMOTE_ADDR'}'");
						if($dbh->err ne "") {
							&say("Falha em atualizar o log no Login!!!");
                        }
                        
					} else {
						$ID = "";
					}
				} else {
					# update timeout se trocou o IP (gera um novo ID)
					$ID = "";
				}
			}
		}

        # Login
		# se o ID não estiver setado, gera
		if($ID eq "") {
			$ID = time;
			$ID .= int(rand 99999)+1;
			if($SENHA eq $MASTERPASS) {
				$rv = $dbh->do("insert into usuario_logado (usuario, empresa, ini, fim, ip, id, req) values ('$USER{USUARIO}', '$USER{EMPRESA}', now() , now(), '$IP', '$ID', 'MASTER Logou no sistema')");
			} else {
				$rv = $dbh->do("insert into usuario_logado (usuario, empresa, ini, fim, ip, id, req) values ('$USER{USUARIO}', '$USER{EMPRESA}', now() , now(), '$IP', '$ID', 'Logou no sistema')");
			}
            
			if($dbh->err ne "") {
				&say("Falha em criar o log de acesso!!!");
			}

		}
		
		# retorna o código do ID do usuário logado
		return $ID;
		}
	elsif($rv > 1)
		{
		# No caso de retornar mais de um usuário
		&say("Por favor, informe o seu e-mail completo", "username");
		return "";
		}
	else
		{
		&say('Usuário ou senha inválidos', 'password');
		return "";
		}
}