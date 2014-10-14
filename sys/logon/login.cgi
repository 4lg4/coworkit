#!/usr/bin/perl


$nacess = 'nocheck';
require "../cfg/init.pl";

# Variaves para relogin
$USER{USUARIO} = lc(&get("username"));
$SENHA         = &get("password");
$USER{EMPRESA} = &get("empresa_codigo");

$USER{fb_id}    = &get("fb_id");
$USER{fb_login} = &get("fb_login");

# suporte para login mobile
# $MOBILE = &get("MOBILE");

print $query->header({charset=>utf8});
require "./login_db.pl";

$ID = &check_login();

if($ID ne ""){ # Caso o login esteja correto
print<<HTML;
        <script>
			try {
				document.forms[0].ID.value = '$ID';
				document.forms[0].action   = document.forms[0].THIS.value;
				document.forms[0].submit();
                
			} catch(err) {
                // console.log(err);
                
				top.document.forms[0].ID.value    = '$ID';
				top.document.forms[0].LOGIN.value = '1';
				top.document.forms[0].action      = '$dir{menu}start.cgi';
                // top.document.forms[0].action      = '/coworkit';
				top.document.forms[0].target      = '_top';
				top.document.forms[0].submit();
			}
        </script>
HTML
}

exit;
