<?php

/**
 * @brief Function exit_program() prints error message for user
 * @param return_value	Return value for exit
 * @param message 		Message for user
 */
function exit_program($return_value, $message)
{
    fputs(STDERR, "$message\n");
    exit($return_value);
}

/**
 * @brief Function help_info() prints description of script
 */
function help_info()
{
    fputs(STDOUT, "This script is for automated testing of scripts parse.php\n");
    fputs(STDOUT, "and interpret.py, checks functionality of scripts, and\n");
    fputs(STDOUT, "prints HTML representation on standard output.\n");
    exit(0);
}

/**
 * @brief check_arg_help($arg, $argc) checks if called argument was --help
 * @param arg   called arguments
 * @param argc  count of arguments
 */
function check_arg_help($arg, $argc)
{
        if (isset($arg["help"]))
        {
            if ($argc > 2)
            {
                exit_program(10, "Invalid arguments used.");
            }
            help_info();
            exit(0);
        }
}

/**
 * @brief check_arg_count($arg, $argc) checks number of arguments
 * @param arg   called arguments
 * @param argc  count of arguments
 */
function check_arg_count($arg, $argc)
{
    if (count($arg) != $argc-1) {
        exit_program(10, "Invalid arguments used.");
    }
}

/**
 * @brief error_handling_parse($parse_file, $int_only) checks if parse.php exists, when argument --int-only was not used
 * @param parse_file    file for parser
 * @param int_only  boolean, if argument --int-only was used
 */
function error_handling_parse($parse_file, $int_only)
{
    if(file_exists($parse_file) == false)
    {
        if($int_only == 1)
        {
            exit_program(11, "Parse.php does not exist.\n");
        }
    }
}

/**
 * @brief error_handling_interpret($interpret, $parse_only) checks if interpret.py exists, when argument --parse-only was not used
 * @param interpret file for interpret
 * @param parse_only    boolean, if argument --parse-only was used
 */
function error_handling_interpret($interpret, $parse_only)
{
    if(file_exists($interpret) == false)
    {
        if($parse_only == 1)
        {
            exit_program(11, "Interpret.py does not exist.\n");
        }
    }
}

/**
 * @brief check_source_files($source_files) checks if there are any source files for testing
 * @param source_files  files for testing
 */
function check_source_files($source_files)
{
    if (empty($source_files))
    {
        echo("No files for testing found.\n");
        exit(0);
    }
}

/**
 * @brief intonly($arg) checks if argument --int-only was used
 * @param arg   arguments used
 */
function intonly($arg)
{
    if (isset($arg))
    {
        return 0;
    }
    else
        return 1;
}

/**
 * @brief intonly($arg) checks if argument --parse-only was used
 * @param arg   arguments used
 */
function parseonly($arg)
{
    if (isset($arg))
    {
        return 0;
    }
    else
        return 1;
}

/**
 * @brief intscript($arg) checks if argument --int-script was used
 * @param arg   arguments used
 */
function intscript($arg)
{
    if (isset($arg))
    {
        return $arg;
    }
    else
        return "./interpret.py";
}

/**
 * @brief parsescript($arg) checks if argument --parse-script was used
 * @param arg   arguments used
 */
function parsescript($arg)
{
    if (isset($arg))
    {
        return $arg;
    }
    else
        return "./parse.php";
}

/**
 * @brief rec($arg) checks if argument --recursive was used
 * @param arg   arguments used
 */
function rec($arg)
{
    if (isset($arg))
    {
        return 0;
    }
    else
        return 1;
}

/**
 * @brief dir($arg) checks if argument --directory was used
 * @param arg   arguments used
 */
function dir_arg($arg)
{
    if (isset($arg))
    {
        return $arg;
    }
    else
        return ".";
}
$recur = 1;
$int_only = 1;
$parse_only = 1;
$parse_file = "./parse.php";
$interpret = "./interpret.py";
$directory = ".";
$longopt = array("help","directory:","recursive","parse-script:","int-script:", "parse-only", "int-only");
$arguments = getopt("", $longopt);
check_arg_count($arguments, $argc);
if ($argc != 1) {
    check_arg_help($arguments, $argc);
    $directory = dir_arg($arguments["directory"]);
    $recur = rec($arguments["recursive"]);
    $parse_file = parsescript($arguments["parse-script"]);
    $interpret = intscript($arguments["int-script"]);
    $parse_only = parseonly($arguments["parse-only"]);
    $int_only = intonly($arguments["int-only"]);
}
if($recur == 0)
{
    $iter = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($directory));
    foreach ($iter as $file) {
        if (is_dir($file) != false) {
            continue;
        }
        $files[] = $file->getPathname();
        $files = array_diff($files, [".",".."]);
    }
}
else
    {
        $directory = glob($directory.'/*.*');
    foreach($directory as $file){
        $files[] = $file;
    }
}

foreach ($files as $src) {
    if(preg_match('/.+.src$/', $src)){
        $source_files [] = $src;
    }
}
check_source_files($source_files);

for ($i = 0; $i < count($source_files); $i++)
{
    $test_names[$i] = preg_replace('/.src$/', "", $source_files[$i]);
}

error_handling_parse($parse_file, $int_only);
error_handling_interpret($interpret, $parse_only);

$test_total = count($source_files);
$test_fail = 0;
$test_ok = 0;
$html = "";
if ($parse_only == 0) {
    foreach ($source_files as $test) {
        $test_name = str_replace(".src", "", $test);
        if (in_array($test_name . ".rc", $files)) {
            $ret_rc = file_get_contents($test_name . ".rc", $test);
        } else {
            $rc_file = fopen($test_name . ".rc", "w");
            if (!$rc_file) {
                exit_program(11, "Cannot open file.");
            }
            fwrite($rc_file, "0\n");
            $ret_rc = 0;
            fclose($rc_file);
        }
        if (in_array($test_name . ".in", $files)) {
            $in_file = fopen($test_name . ".in", "c+");
            if (!$in_file) {
                exit_program(11, "Cannot open file.");
            }
        } else {
            $in_file = fopen($test_name . ".in", "c+");
            if (!$in_file) {
                exit_program(11, "Cannot open file.");
            }
        }
        if (in_array($test_name . ".out", $files)) {
            $out_file = fopen($test_name . ".out", "c+");
            if (!$out_file) {
                exit_program(11, "Cannot open file.");
            }
        } else {
            $out_file = fopen($test_name . ".out", "c+");
            if (!$out_file) {
                exit_program(11, "Cannot open file.");
            }
        }
        fclose($in_file);
        fclose($out_file);
        $out = $test_name . ".tmp";
        $input_inter = $test_name . ".in";
        exec("php7.3 $parse < $test", $parse_out, $parse_ret);
        if ($parse_ret != 0) {
            if ($ret_rc != $parse_ret) {
                $test_fail++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            } else { //
                $test_ok++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            }
        }
        elseif ($parse_ret == 0){
            if ($ret_rc == $parse_ret){
                $test_ok++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            }
            else {
                $test_fail++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            }
        }

    }
    if (1) {
        echo "<!DOCTYPE html>
    <html>
      <head>
         <title>IPPcode19</title>
         <meta charset=\"UTF-8\">
         <style type=\"text/css\">
         </style>
      </head>
      <body>
        <h1 style=\"text-align: center;\">Automated testing of script parse.php </h1>
       <p style=\"text-align: center;\"><em>IPPcode19</em></p>
<table style=\"height: 51px; width: 349px; border-color: grey; margin-left: auto; margin-right: auto;\" border=\"4\">
<tbody>
<tr>
<td style=\"width: 287.75px;\">
<h3><span style=\"color: #008000;\">Successful:</span></h3>
</td>
<td style=\"width: 61.25px;\">$test_ok</td>
</tr>
<tr>
<td style=\"width: 287.75px;\">
<h3><span style=\"color: #ff0000;\">Failed:</span></h3>
</td>
<td style=\"width: 61.25px;\">$test_fail</td>
</tr>
<tr>
<td style=\"width: 287.75px;\">
<h3>Total:</h3>
</td>
<td style=\"width: 61.25px;\">$test_total</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>";
        echo "$html";
        echo "</body></html>";
    }
}
elseif ($int_only == 0){
    foreach ($source_files as $test) {
        $test_name = str_replace(".src", "", $test);
        if (in_array($test_name . ".rc", $files)) {
            $ret_rc = file_get_contents($test_name . ".rc", $test);
        } else {
            $rc_file = fopen($test_name . ".rc", "w");
            if (!$rc_file) {
                exit_program(11, "Cannot open file.");
            }
            fwrite($rc_file, "0\n");
            $ret_rc = 0;
            fclose($rc_file);
        }
        if (in_array($test_name . ".in", $files)) {
            $in_file = fopen($test_name . ".in", "c+");
            if (!$in_file) {
                exit_program(11, "Cannot open file.");
            }
        } else {
            $in_file = fopen($test_name . ".in", "c+");
            if (!$in_file) {
                exit_program(11, "Cannot open file.");
            }
        }
        if (in_array($test_name . ".out", $files)) {
            $out_file = fopen($test_name . ".out", "c+");
            if (!$out_file) {
                exit_program(11, "Cannot open file.");
            }
        } else {
            $out_file = fopen($test_name . ".out", "c+");
            if (!$out_file) {
                exit_program(11, "Cannot open file.");
            }
        }
        fclose($in_file);
        fclose($out_file);
        if (file_exists($interpret) == false) {
            echo "11: Skript interpret.py nenájdený v adresári.\n";
            exit_program(11, "Cannot open file.");
        }
        $in_file = $test_name . ".in";
        exec("python3.6 " . $interpret . " --source=". $test . " < ".$in_file, $int_out, $int_ret);
        if ($int_ret != $ret_rc) { //
            $test_fail++;
            $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $int_ret</h3>
<p>&nbsp;</p>";
        } else {
            if ($int_ret == 0) {
                $out_file = $test_name . ".out";
                exec("diff $int_out $out_file", $diff, $rc_diff);
                if (count($diff) == 0) {
                    $test_ok++;
                    $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $int_ret</h3>
<p>&nbsp;</p>";
                } else {
                    $test_fail++;
                    $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $int_ret</h3>
<p>&nbsp;</p>";
                }
            } else {
                $test_ok++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $int_ret</h3>
<p>&nbsp;</p>";
            }
        }

    }
    if (1) {
        echo "<!DOCTYPE html>
    <html>
      <head>
         <title>IPPcode19</title>
         <meta charset=\"UTF-8\">
         <style type=\"text/css\">
         </style>
      </head>
      <body>
        <h1 style=\"text-align: center;\">Automated testing of script interpret.py</h1>
       <p style=\"text-align: center;\"><em>IPPcode19</em></p>
<table style=\"height: 51px; width: 349px; border-color: grey; margin-left: auto; margin-right: auto;\" border=\"4\">
<tbody>
<tr>
<td style=\"width: 287.75px;\">
<h3><span style=\"color: #008000;\">Successful:</span></h3>
</td>
<td style=\"width: 61.25px;\">$test_ok</td>
</tr>
<tr>
<td style=\"width: 287.75px;\">
<h3><span style=\"color: #ff0000;\">Failed:</span></h3>
</td>
<td style=\"width: 61.25px;\">$test_fail</td>
</tr>
<tr>
<td style=\"width: 287.75px;\">
<h3>Total:</h3>
</td>
<td style=\"width: 61.25px;\">$test_total</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>";
        echo "$html";
        echo "</body></html>";
    }
}
else{
    foreach ($source_files as $test) {
        $test_name = str_replace(".src", "", $test);
        if (in_array($test_name . ".rc", $files)) {
            $ret_rc = file_get_contents($test_name . ".rc", $test);
        } else {
            $rc_file = fopen($test_name . ".rc", "w");
            if (!$rc_file) {
                exit_program(11, "Cannot open file.");
            }
            fwrite($rc_file, "0\n");
            $ret_rc = 0;
            fclose($rc_file);
        }
        if (in_array($test_name . ".in", $files)) {
            $in_file = fopen($test_name . ".in", "c+");
            if (!$in_file) {
                exit_program(11, "Cannot open file.");
            }
        } else {
            $in_file = fopen($test_name . ".in", "c+");
            if (!$in_file) {
                exit_program(11, "Cannot open file.");
            }
        }
        if (in_array($test_name . ".out", $files)) {
            $out_file = fopen($test_name . ".out", "c+");
            if (!$out_file) {
                exit_program(11, "Cannot open file.");
            }
        } else {
            $out_file = fopen($test_name . ".out", "c+");
            if (!$out_file) {
                exit_program(11, "Cannot open file.");
            }
        }
        fclose($in_file);
        fclose($out_file);
        $out = $test_name . ".tmp";
        $input_inter = $test_name . ".in";
        exec("php7.3 $parse < $test", $parse_out, $parse_ret);
        if ($parse_ret != 0) {
            if ($ret_rc != $parse_ret) {
                $test_fail++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            } else { //
                $test_ok++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            }
        } else {
            if (file_exists($interpret) == false) {
                echo "11: Skript interpret.py nenalezen v daném adresáři.\n";
                exit_program(11, "Cannot open file.");
            }
            $parse_out = implode("\n", $parse_out);
            $temp = tmpfile();
            fwrite($temp, $parse_out);
            exec("python3.6 " . $interpret . " --source=" . stream_get_meta_data($temp)['uri'] . " < " . $input_inter . " > " . $out, $int_out, $int_ret);
            fclose($temp);
            if ($int_ret != $ret_rc) {
                $test_fail++;
                $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
            } else {
                if ($int_ret == 0) {
                    $out_file = $test_name . ".out";
                    exec("diff $out $out_file", $diff, $rc_diff);
                    if (count($diff) == 0) {
                        $test_ok++;
                        $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
                    } else {
                        $test_fail++;
                        $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
                    }
                } else {
                    $test_ok++;
                    $html .= "<h3>Name: $test</h3>
<h3>Expected return code: $ret_rc</h3>
<h3>Actual return code: $parse_ret</h3>
<p>&nbsp;</p>";
                }
            }
            unlink($out);
        }
    }
    if (1) {
        echo "<!DOCTYPE html>
    <html>
      <head>
         <title>IPPcode19</title>
         <meta charset=\"UTF-8\">
         <style type=\"text/css\">
         </style>
      </head>
      <body>
        <h1 style=\"text-align: center;\">Automated testing of scripts parse.php and interpret.py</h1>
       <p style=\"text-align: center;\"><em>IPPcode19</em></p>
<table style=\"height: 51px; width: 349px; border-color: grey; margin-left: auto; margin-right: auto;\" border=\"4\">
<tbody>
<tr>
<td style=\"width: 287.75px;\">
<h3><span style=\"color: #008000;\">Successful:</span></h3>
</td>
<td style=\"width: 61.25px;\">$test_ok</td>
</tr>
<tr>
<td style=\"width: 287.75px;\">
<h3><span style=\"color: #ff0000;\">Failed:</span></h3>
</td>
<td style=\"width: 61.25px;\">$test_fail</td>
</tr>
<tr>
<td style=\"width: 287.75px;\">
<h3>Total:</h3>
</td>
<td style=\"width: 61.25px;\">$test_total</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>";
        echo "$html";
        echo "</body></html>";
    }
}
?>