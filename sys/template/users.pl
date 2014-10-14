#!/usr/bin/perl

#
# insert de usuario
#
$USERMSGTITLE{new} = "Bem vindo ao CoworkIT";
$USERMSGNEW=<<HTML;
<html>
    <head>
        <title>CoworkIT, boas vindas</title>
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
HTML

#
# update de usuario
#
$USERMSGTITLE{update} = "CoworkIT, usuário modificado !";
$USERMSGUPDATE=<<HTML;
<html>
    <head>
        <title>CoworkIT, updates</title>
        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
        <meta http-equiv="pragma" content="no-cache">
        <meta http-equiv="cache-control" content="no-cache">
        <meta http-equiv="expires" content="0">
    </head>
    
    <body bgcolor="#dedede" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
        <center>

            Atualizado, usuario com sucesso

        <center>
    </body>
</html>
HTML

return true;
