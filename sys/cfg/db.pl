#!/usr/bin/perl

&connect;

# pega numero de erro do postgresql
# $dbh->state();
# ex. 22P02 = INVALID TEXT REPRESENTATION
# http://www.postgresql.org/docs/8.2/static/errcodes-appendix.html


sub connect {
	$dbh = DBI->connect("DBI:Pg:dbname=$db;host=$server",$user,$pass) || die "Erro na conexão!!! $!\n\n";
    
    # seta tratamento de datas para portugues
    $dbh->do("SET lc_time = 'pt_BR.UTF8';");
}

sub doneConnect
	{
	my ($opt) = @_;
	
	# abre conexao se for vazio 
	if($opt eq "")
		{
		$DONEDB = DBI->connect("DBI:Pg:dbname=$db;host=$server",$user,$pass) || die "Erro na conexão!!! $!\n\n";
		}
	# fecha conexao se nao for vazio 
	else 
		{
		$DONEDB->disconnect;
		}
	}


# [INI] DB EXEC ------------------------------------------------------------------------------------------------------------------------
# 
#    DBE, funcao para executar sql generico
# 
#    DBE($sql,$error_user)
#		$sql = instrucao sql
# 		$error_user = descricao do erro para report do usuario (nao obrigatorio)
#  
sub DBE
	{
	my ($sql,$error_user,$noerror) = @_;
	my $error = "";
	my $acao = "";
	# my $filter = " empresa = ".$USER->{empresa};
	
    # print "<hr> $sql <hr>";
    
	# se a busca vier vazia
	if($sql eq "")
		{
		erroDBcommon("Instrução SQL, é necessária para o funcionamento !!! <br><br> ");
		exit;
		}
	else # se tudo estiver OK, verifica o que deve ser feito
		{
		$sql_test = lc($sql); # tudo minusculo
		
		# ajusta para execucao do select
		if($sql_test =~ /insert/)
			{ $acao = "insert"; }
		elsif($sql_test =~ /update/)
			{ $acao = "update"; }
		elsif($sql_test =~ /delete/)
			{ $acao = "delete"; }
		elsif($sql_test =~ /select/)
			{ $acao = "select"; }
			
		# adiciona filtros por empresa
		# adiciona camada adicional para filtro
		# if($sql =~ /select * from usuario order by nome asc/)
		#	{
		#		
		# if($sql =~ /where/)
		#	{
		#	if($sql =~ /order/)
		#		{
		#		$sql =  substr $sql, index($sql, 'order'), 5, 'and $filter order';
		#		}
		#	else
		#		{
		#		$sql .=  " and $filter";
		#		}
		#	}
		# else
		#	{
		#	$sql .=  " where $filter";
		#	}
		#	
		#	}
		#	debug($sql);
		}
    	
	if($acao eq "select")
		{ 
		&DBE_select($sql,$error_user,$noerror); 
		}
	else
		{ 
		&DBE_do($sql,$acao,$error_user,$noerror); 
		}
	}
	
# executa selects
sub DBE_select
	{
	my ($sql,$error_user,$noerror) = @_;
	my $error = "";
	 
	# ajusta mensagem user friendly
	$error = $msg{db_select}." ".$error_user." <br><br> ";
	
	# prepara para execucao	
	my $DB = $dbh->prepare($sql);
	$DB->execute();
			
	# se houverem erros 
	if($dbh->err ne "")
		{		
		if($noerror eq "")
			{
			# gera tela com erro
			erroDBcommon($error);		
			exit;
			}
		else
			{
			return false;
			}
		}
	else
		{
		# mensagem de retorno de nada
		if($DB->rows() < 1)
			{
			$alerta = "Nenhum registro encontrado !!";
			}	
		
		return $DB;
		}
	}
	
# executa Insert / Update / Delete
sub DBE_do {
	my ($sql,$acao,$error_user,$noerror) = @_;
	my $error = "";
	
	# ajusta mensagem user friendly
	$error = $msg{"db_$acao"}." ".$error_user." <br><br> ";
	
	# prepara para execucao	
	my $DB = $dbh->do($sql);
			
	# se houverem erros 
	if($dbh->err ne "") {
		if($noerror eq "") {		
			# gera tela com erro
			erroDBcommon($error);
			
			# desfaz atualizacao
			$dbh->rollback;	
		
			exit;
	    } else {
			return false;
		}
	} else {
        
        $sql =~ s/\r|\n/ /gm; # remove quebras de linhas
        
        # retorna codigo sequencial do ultimo inserido
        if($acao eq "insert" && $sql !~ /\)\s*[,|;]\s*\(/m) {
            
            $sql =~ /^.*(into)\s+(\w*)/; # pega mome da tabela
            
            # correcao de retorno do auto increment se for tabela usuarios
            if($2 eq "usuario") {
                $cod = "usuario";
            } else {
                $cod = "codigo";
            }
            
			$D_B_E_  = &DBE("SELECT 0 FROM pg_class where relname = '".$2."_".$cod."_seq'");
			if($D_B_E_->rows() > 0) {
                $D_B_E_  = &DBE("select currval('".$2."_".$cod."_seq')");
                $row = $D_B_E_->fetch;
                return @$row[0];
            }
            
        } else {
		    return $DB;
        }
	}
}
# [END] DB EXEC ------------------------------------------------------------------------------------------------------------------------


# [INI] Select -------------------------------------------------------------------------------------------------------------------------
# 	 DEPRECATED - USAR FUNCAO DBE
#    Select, funcao para executar selects 
#
sub select
	{
	my ($sql) = @_;

	# se a busca vier vazia
	if($sql eq "")
		{
		erroDBcommon("Instrução SQL, é necessária para o funcionamento !!! <br><br> ");
		exit;
		}
	else
		{ 
		&DBE($sql); 
		}
	}
# [END] Select -------------------------------------------------------------------------------------------------------------------------


sub get_cfg
	{
	my ($chave) = @_;
	
	$sth = &DBE("select valor from usuario_cfg where usuario_cfg.usuario = '$LOGUSUARIO' and usuario_cfg.cfg = '$chave' limit 1");
	$sth->execute();
	$row = $sth->fetch;
		{
		return @$row[0];
		}
	}

sub erroDBS
	{
	my ($msg) = @_;
	print "<script language='JavaScript'>\n";
	&erroDBcommon($msg);	
	print "</script>\n";
	exit;
	}

sub erroDB
	{
	my ($msg) = @_;
	&erroDBcommon($msg);
	exit;
	}

sub erroDBH
	{
	my ($msg_int) = @_;
	
	# ajuste da mensagem de aviso
	if($msg ne "")
		{
		$msg .= "\n";
		}
		
	
    $IFFAIL  = "<div class='DDialog_box_middle'> Estamos trabalhando pra MUDAR a  <br> TI do Brasil !!  </div>";
    $IFFAIL .= "<div class='DDialog_box_img'><img src='/img/bugs/construction.png'></div>";
    $IFFAIL .= "<div class='DDialog_box_bottom'> um email com erro será enviado para o suporte Obrigado..</div>";    
	$msg .= $IFFAIL;
	
	# adiciona 
	if($dbh->errstr ne "")
		{
		$msg_int .= "\n$IFFAILEN: ".$dbh->err."\n$IFFAILED: ".$dbh->errstr;
		}
	else
		{
		$msg_int .= "\n$!";
		}
	$msg =~ s/\n/<br>/gm;
	print "<html><body><font style='color: red'>$msg **** $USER->{usuario} | $USER->{empresa} ****</font></body></html>";
	}

sub erroDBcommon
	{
	my ($msg_int) = @_;
	if($msg ne "") {
		$msg .= "\n";
	}
        
    $IFFAIL  = "<div class='DDialog_box_middle'> Estamos trabalhando pra MUDAR a  <br> TI do Brasil !!  </div>";
    $IFFAIL .= "<div class='DDialog_box_img'><img src='/img/bugs/construction.png'></div>";
    $IFFAIL .= "<div class='DDialog_box_bottom'> um email com erro será enviado para o suporte Obrigado..</div>";
        
	$msg .= $IFFAIL;
	if($dbh->errstr ne "")
		{
		$msg_int .= "\n$IFFAILEN: ".$dbh->err."\n$IFFAILED: ".$dbh->errstr;
		}
	else
		{
		$msg_int .= "\n$!";
		}
	
    $msg =~ s/(\n|\r)/\\n/gm;
	$msg =~ s/\"/\\"/gm;
    
    $msg_int =~ s/(\n|\r)/\\n/gm;
	$msg_int =~ s/\"/\\"/gm;
	
print<<HTML;
		<script>
		    try
				{
				top.unLoading();
				}
		    catch(err)
				{
				// ignora erros
				}
			
			// Tenta executar mensagem de erro com o modal senao usa javascript puro
			try
				{
				// top.alerta("$msg");
                
                    \$.DDialog({
                        type    : "error",
                        title   : "Desculpe o transtorno",
                        message : "$msg",
                        btnOK   : function(){
                            \$.DIssue({
                                type    : "bug",
                                source  : "postgres",
                                message : "$msg_int"
                            });
                        }
                    });
                
				}
			catch(err)
				{ console.log(err);
				alert("$msg");
				}	
		    
		</script>
HTML
	}





# objeto para gerar
# package DBEO;
# 
#	sub new
#		{
#	    my $class = shift;
#	    my $self = 
#			{
#	        _firstName => shift,
#	        _lastName  => shift,
#	        _ssn       => shift,
#	    	};
#	    # Print all the values just for clarification.
#	    print "First Name is $self->{_firstName}\n";
#	    print "Last Name is $self->{_lastName}\n";
#	    print "SSN is $self->{_ssn}\n";
#	    bless $self, $class;
#	    return $self;
#		}
#
#	sub setFirstName 
#		{
#	    my ( $self, $firstName ) = @_;
#	    $self->{_firstName} = $firstName if defined($firstName);
#	    return $self->{_firstName};
#		}
#
#	sub getFirstName 
#		{
#	    my( $self ) = @_;
#	    return $self->{_firstName};
#		}
# 1;

return true;


