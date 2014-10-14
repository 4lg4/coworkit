
<?php
    $output = shell_exec('tail -n 20 /var/log/apache2/aprendiz-error.log');
    echo "<pre>$output</pre>";
?>
