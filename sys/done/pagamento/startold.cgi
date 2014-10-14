#!/usr/bin/perl

$nacess = "80";
require "../../cfg/init.pl";

print $query->header({charset=>utf8});

print<<HTML;

<form>
    
    
    <h1>Meus Pagamentos</h1>
    
    <h1>Pagamentos</h1>
    
    <select>
        <option>
    </select>
</form>

- Autonomous 39 <br>
<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
    <input type="hidden" name="cmd" value="_s-xclick">
    <input type="hidden" name="hosted_button_id" value="CUWGNRVW5KEJ6">
    <input type="image" src="https://www.paypalobjects.com/pt_BR/BR/i/btn/btn_paynowCC_LG.gif" border="0" name="submit" alt="PayPal - A maneira mais fácil e segura de efetuar pagamentos online!">
    <img alt="" border="0" src="https://www.paypalobjects.com/pt_BR/i/scr/pixel.gif" width="1" height="1">
</form>

<script>
	
</script>


</body></html>


HTML

