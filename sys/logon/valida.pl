#!/usr/bin/perl

$query = new CGI;
$IP    = $ENV{'REMOTE_ADDR'};
$THIS  = $ENV{'SCRIPT_NAME'};
$ID    = &get("ID");
$COD   = &get("COD");
$MODO  = &get("MODO");

if($nacess eq "nocheck") {
    
	# Só aceita requisições do próprio servidor, por segurança     # && $ENV{'REMOTE_ADDR'} ne "$RSITE" )
	if($ENV{'HTTP_REFERER'} !~ /^(http|https):\/\/$ENV{'SERVER_NAME'}/ && $ENV{'HTTP_REFERER'} !~ /^(http|https):\/\/(www\.)?done\.com\.br\// ) {
		print $query->header({charset=>utf8});
		print "<h2><a href='/'>ACESSO NEGADO!</a></h2>";
		print "	<script>
					alert('Acesso Negado !'); 
					window.location.replace('/');
				</script>";
		exit;
	}
        
} elsif($ID ne "") {
    
	$sth = &DBE("select usuario, substring(req, 1, 6) as usuario_ini, empresa from usuario_logado where id = '$ID' and ip = '$IP' and now() < (FIM + interval '$timeout seconds') ");
	$row = $sth->fetchrow_hashref;
	if(!$row) {
            
		# DONE IPS else pede relogon
		if(checkislocal($IP) == true) {
			$rv = $dbh->do("update usuario_logado set fim=now(), ip = '$IP' where id='$ID' ");
			if($dbh->err ne "") {
				&say("Falha em atualizar o log no Login!!!");
			}
		}
        
		$sth = &DBE("select usuario, substring(req, 1, 6) as usuario_ini, empresa from usuario_logado where id = '$ID' and ip = '$IP' and now() < (FIM + interval '$timeout seconds') ");
		$row = $sth->fetchrow_hashref;
	}
	
	if($row)
		{
		# [INI] gera variaveis de ambiente do usuario -------------------------
		$sth2 = &DBE("select * from usuario_view where usuario = '".$row->{'usuario'}."'");
		$USER = $sth2->fetchrow_hashref;
		$LOGUSUARIO = $USER->{'usuario'};
		$LOGEMPRESA = $USER->{'empresa'};
		
        # print $query->header({charset=>utf8});
        
        
        
		# User CFG, busca todas as configuracoes do usuario 
		$CFG = &DBE("
                    select 
                        uc.*, 
                        cfg.internal_descrp as internal_descrp 
                    from 
                        usuario_cfg as uc 
                    left join 
                        cfg on cfg.codigo = uc.cfg 
                    where 
                        uc.usuario = $USER->{usuario}
        ");
		while($C = $CFG->fetchrow_hashref) {
			$USER->{$C->{internal_descrp}} = $C->{valor};
			$USER->{$C->{cfg}} = $C->{valor};
		}
		# [END] gera variaveis de ambiente do usuario -------------------------
		
        
        #foreach $k (keys %{ $USER }) {
         #   $R .= $k." - ".$USER->{$k}." | ";
        #}
        
        #print "<scrip>console.log(\"$R\")</script>";
        
		if($req eq "") {
			$req = $THIS;
		}
            
		if($row->{'usuario_ini'} eq "MASTER") {
			$req = "MASTER ".$req;
		}
		
		$rv = $dbh->do("update usuario_logado set fim=now(), req='$req' where id='$ID' and ip = '$IP'");
		if($dbh->err ne "")
			{
			print $query->header({charset=>utf8});
			&erroDBH();
			}
		$rv = $dbh->do("insert into usuario_historico (usuario, empresa, dt, ip, req) values ('".$USER->{'usuario'}."', '$USER->{empresa}', now(), '$IP', '$req') ");
		if($dbh->err ne "")
			{
			print $query->header({charset=>utf8});
			&erroDBH();
			}
  
		if($nacess ne "")
			{
			# Verifica direitos
            # debug("select * from usuario_menu where usuario_menu.usuario = '".$USER->{'usuario'}."' and usuario_menu.menu = '$nacess' $nacess_more ");
            
            #    adicionar nacess multiplo usando array
            #print $query->header({charset=>utf8});
            #if(@nacess) {
            #    foreach $na (@nacess) {
            #        debug("works ".$na);
            #    }
            #} else {
            #    debug(@nacess." # ".$nacess);
            #}
            
			$sth = &DBE("select * from usuario_menu where usuario_menu.usuario = '".$USER->{'usuario'}."' and usuario_menu.menu = '$nacess' $nacess_more ");
			if($rv = $sth->rows > 0)
				{
				$row = $sth->fetchrow_hashref;
				$nacess_tipo = $row->{'direito'};
				
				# Testa se tem acesso ao modulo solicitaco
				#if($MODO eq "editar" || $MODO eq "ver" || $MODO eq "excluir")
				#	{
				#	# se edicao codigo nao pode ser vazio
				#	if($COD eq "")
				#		{
				#		print $query->header({charset=>utf8});
				#		print "<script language='JavaScript'>top.alerta('Requisição inválida! \\n Código não preenchido');top.unLoading();</script>";
				#		exit;
				#		}
				#	# testa tipo de acesso
				#	if($nacess_tipo ne "a" && $nacess_tipo ne "s")
				#		{
				#		$MODO = "ver";
				#		}
				#	}
				#elsif($MODO eq "incluir")
				#	{
					# se inclusao codigo deve ser vazio
					#if($COD ne "")
					#	{
					#	print $query->header({charset=>utf8});
					#	print "<script language='JavaScript'>top.alerta('Requisição inválida! \\n Código deve ser vazio');top.unLoading();</script>";
					#	exit;
					#	}
					# testa tipo de acesso
				#	if($nacess_tipo ne "a" && $nacess_tipo ne "s")
				#		{
				#		$MODO = "ver";
				#		print $query->header({charset=>utf8});
				#		print "<script language='JavaScript'>top.alerta('Acesso Negado 1!');</script>";
				#		exit;
				#		}
				#	}
				}
			else
				{
				print $query->header({charset=>utf8});
print<<END;
		<script language='JavaScript'>
		  top.alerta("Acesso Negado! <br> Você não tem direito de acesso a este módulo", "top.unLoading()");
		</script>
END
				exit;
				}
			}
            
} else {
    
		if($LOGUSUARIO eq "" || $LOGEMPRESA eq "")
			{
			# Caso de timeout
			$sth = &DBE("select usuario_view.* from usuario_logado join usuario_view on usuario_logado.usuario = usuario_view.id where usuario_logado.id = '$ID' and usuario_logado.ip = '$IP' ");
			if($rv = $sth->rows > 0)
				{
				$USER = $sth->fetchrow_hashref;
				$LOGLOGIN = $USER->{'login'};
				$LOGUSUARIO = $USER->{'usuario'};
				$LOGEMPRESA = $USER->{'empresa'};
				
				# User CFG, busca todas as configuracoes do usuario 
				$CFG = &DBE("select uc.*, cfg.internal_descrp as internal_descrp from usuario_cfg as uc left join cfg on cfg.codigo = uc.cfg where uc.usuario = $USER->{usuario}");
				while($C = $CFG->fetchrow_hashref)
					{
					$USER->{$C->{internal_descrp}} = $C->{valor};
					$USER->{$C->{cfg}} = $C->{valor};
					}
				}
			else
				{
				# No caso de troca de IP
				$sth = &DBE("select usuario_view.* from usuario_logado join usuario_view on usuario_logado.usuario = usuario_view.id where usuario_logado.id = '$ID' ");

				if($rv = $sth->rows > 0)
					{
					$USER = $sth->fetchrow_hashref;
					$LOGLOGIN = $USER->{'login'};
					$LOGUSUARIO = $USER->{'usuario'};
					$LOGEMPRESA = $USER->{'empresa'};
					
					# User CFG, busca todas as configuracoes do usuario 
					$CFG = &DBE("select uc.*, cfg.internal_descrp as internal_descrp from usuario_cfg as uc left join cfg on cfg.codigo = uc.cfg where uc.usuario = $USER->{usuario}");
					while($C = $CFG->fetchrow_hashref)
						{
						$USER->{$C->{internal_descrp}} = $C->{valor};
						$USER->{$C->{cfg}} = $C->{valor};
						}
					}
				else
					{
					$LOGLOGIN = "";
					$LOGUSUARIO = "";
					$LOGEMPRESA = "";
					}
				}
			}
			
		print $query->header({charset=>utf8});
print<<END;
		<script language='JavaScript'>
END
		$cgikey = "THIS: '$THIS', ";
		@campo = $query->param();
		for($f=0;$f< scalar(@campo);$f++)
			{
			if($campo[$f] ne "username" && $campo[$f] ne "password" && $campo[$f] ne "ID" && $campo[$f] ne "THIS")
				{
				$cgikey .= $campo[$f].": '".&get($campo[$f])."', ";
				}
			}
		$cgikey =~ s/[,][ ]$//;
		print "top.cgikey = { ";
		print $cgikey;
		print " };\n";
print<<END;
			if(top.blastcall == false)
				{
				top.blastcall = true;
				if(window.name == "main")
					{
					top.slastcall = "document.login.submit()";
					top.relogin('$LOGLOGIN', '$LOGEMPRESA');
					}
				else
					{
					relogin('$LOGLOGIN', '$LOGEMPRESA');
					}
				}
		</script>
END
		exit;
		}
}

return true;
