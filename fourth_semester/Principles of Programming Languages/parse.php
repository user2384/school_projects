<?php

/**
 * @brief Function help_info() prints description of script
 */ 
function help_info()
{
	fputs(STDOUT, "This script loads source code in IPPcode19 from standart input,\n");
	fputs(STDOUT, "checks lexical and syntax correctness and prints XML representation\n");
	fputs(STDOUT, "of the program on standart output.\n");
	exit(0);
}

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
 * @brief Function check_args() checks check is all input argumetns are correct and sets relevant flags
 * @param $argv     Argument list
 * @param $argc   	Argument count
 */
function check_arguments($argv, $argc)
{
	if($argc ==1)
		;
	else if($argc == 2)
	{
		if($argv[1] == "--help") /* one arguments --help */
			help_info();
		else
			exit_program(10, "None or invalid argument.");
	}
}

/* Array of instruction names - opcode names, with their value as input arguments*/
$ins_array = array("move"=>"vs",
"createframe"=>"",
"pushframe"=>"",
"popframe"=>"",
"defvar"=>"v",
"call"=>"l",
"return"=>"",
"pushs"=>"s",
"pops"=>"v",
"add"=>"vss",
"sub"=>"vss", 
"mul"=>"vss", 
"idiv"=>"vss",
"lt"=>"vss", 
"gt"=>"vss", 
"eq"=>"vss",
"and"=>"vss", 
"or"=>"vss", 
"not"=>"vs",
"int2char"=>"vs",
"stri2int"=>"vss",
"read"=>"vt",
"write"=>"s",
"concat"=>"vss",
"strlen"=>"vs",
"getchar"=>"vss", 
"setchar"=>"vss",
"type"=>"vs",
"label"=>"l", 
"jump"=>"l",
"jumpifeq"=>"lss", 
"jumpifneq"=>"lss",
"exit"=>"s",
"dprint"=>"s",
"break"=>"");

/* Check input arguments */
check_arguments($argv, $argc);
/* Static variables initialization */
STATIC $flag_ippcode_comes = false;
GLOBAL $xml;
/* Initialization of XML */
$xml = xmlwriter_open_memory(); 
xmlwriter_set_indent($xml, 1); 
xmlwriter_set_indent_string($xml,'    '); //4 spaces
xmlwriter_start_document($xml, '1.0', 'UTF-8');
/* Regular expressions as patterns to check arguments*/
$empty_line = '/^\s+$/';
$comment_line = '/(^#+\X*$)|(^\s+#+\X*$)/';
$header_line = "/^.ippcode19\s*(#*|#+\X*)\s*$/i";
$symbol_pattern = '/((LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(int@((\+|\-)?\d+)$|(bool@(true|false)$)|nil@nil$|(string@(([^#|\s\\)])*(\\\d\d\d))*(([^#|\s\\)])*))$)/';
/* Start reading lines from stdin */
while($line = fgets(STDIN))
{
	$line = trim($line); /* Cut whitespaces from beg and end */
	
	if (empty($line)) /* If line is empty */
	{
		continue;
	}
	else if(preg_match($comment_line, $line)) /* If line is comment */
	{
		;
	}
	else if (preg_match($empty_line, $line))
	{
		continue;
	}
	else if(preg_match($header_line, $line)) /* If line is header .IPPcode19 */
	{
		xmlwriter_start_element($xml, 'program'); 
		xmlwriter_start_attribute($xml, 'language');
		xmlwriter_text($xml, 'IPPcode19');
		xmlwriter_end_attribute($xml);
    	if($flag_ippcode_comes == true) /* If header .IPPcode19 has been defined already */
    	{
    		exit_program(21, "IPPcode refined.");
    	}
    	$flag_ippcode_comes = true; /* Set flag to true .IPPcode19 is defined */
    }
    else
    {
    	if($flag_ippcode_comes == false) /* If head .IPPcode19 hasnt been defined */
    	{
    		exit_program(21, "IPPcode19 non defined.");
    	}
    	else
    	{
    		$linesplit = preg_split('/#/', $line); /* Split line on two parts - comment and the rest */
    		$linesplit = preg_split('/\s+/', $linesplit[0]); /*Split the rest by whitespaces */
    		$opcode = strtolower($linesplit[0]); 
  		
    		$opcodefound = 1;
    		foreach ($ins_array as $keyword => $key) /* Check if instruction is in keywords array*/
    		{
    			if($keyword == $opcode)
    			{
    				$opcodefound = 0;
    				/* Adds XML element instruction */
    				xmlwriter_start_element($xml, 'instruction');
 					xmlwriter_start_attribute($xml, 'order');
					xmlwriter_text($xml, $loc_count);
					xmlwriter_end_attribute($xml);
					xmlwriter_start_attribute($xml, 'opcode');
					xmlwriter_text($xml, strtoupper($opcode));
					xmlwriter_end_attribute($xml);
    				break;
    			}
    		}
    		if($opcodefound == 1) /* If opcode hasnt been found */
    			exit_program(22, "Unknown instruction.");
    		else
    		{
    			if ($key == "v")
    			{
    				$pattern = '/^(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)([[:alnum:]]|_|-|\$|&|%|\*)*$/'; //var pattern
    				$type = "var";
    				$value = $linesplit[1];
    			}
    			else if ($key == "l")
    			{
    				$pattern = '/^([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/'; //label pattern
    				$type = "label";
    				$value = $linesplit[1];
    			}
    			else if ($key == "s")
    			{
    				$pattern = '/((LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(int@((\+|\-)?\d+)$|(bool@(true|false)$)|nil@nil$|(string@(([^#|\s\\)])*(\\\d\d\d))*(([^#|\s\\)])*))$)/'; //symb pattern
    				if(preg_match('/^int@((\+|\-)?\d+)$/', $linesplit[1]))
					{
						$type = "int";
						$value = explode("@", $linesplit[1], 2);
						$value = $value[1];
					}
					else if(preg_match('/^nil@nil$/', $linesplit[1]))
					{
						$type = "nil";
						$value = explode("@", $linesplit[1], 2);
						$value = $value[1];
					}
					else if(preg_match('/^bool@(true|false)$/', $linesplit[1]))
					{
						$type = "bool";
						$value = explode("@", $linesplit[1], 2);
						$value = $value[1];
					}
					else if(preg_match('/^string@([^#\s\x5C]|\x5C[0-9]{3})*$/', $linesplit[1]))
					{
						$type = "string";
						$value = explode("@", $linesplit[1], 2);
						$value = $value[1];
					}
					else if(preg_match('/(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/', $linesplit[1]))
					{
						$type = "var";
						$value = $linesplit[1];
					}
					else
					{
						exit_program(23, "Non valid argument of the instruction.");
					}
    			}
    			else if ($key == "vs")
    			{
    				$pattern1 = '/^(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)([[:alnum:]]|_|-|\$|&|%|\*)*$/'; //var pattern
    				$pattern2 = '/((LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$)|(int@((\+|\-)?\d+)$|(bool@(true|false)$)|nil@nil$|(string@(([^#|\s\\)])*(\\\d\d\d))*(([^#|\s\\)])*))$)/'; //symb pattern
    				$type1 = "var";	
    				$value1 = $linesplit[1];
					if(preg_match('/^int@((\+|\-)?\d+)$/', $linesplit[2]))
					{
						$type2 = "int";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^nil@nil$/', $linesplit[2]))
					{
						$type2 = "nil";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^bool@(true|false)$/', $linesplit[2]))
					{
						$type2 = "bool";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^string@([^#\s\x5C]|\x5C[0-9]{3})*$/', $linesplit[2]))
					{
						$type2 = "string";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/', $linesplit[2]))
					{
						$type2 = "var";
						$value2 = $linesplit[2];
					}
					else
					{
						exit_program(23, "Non valid argument of the instruction.");
					}
    			}
    			else if ($key == "vt")
    			{
    				$pattern1 = '/^(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)([[:alnum:]]|_|-|\$|&|%|\*)*$/'; //var pattern
					$pattern2 = '/^int$|^string$|^bool$/'; //type pattern
					$type1 = "var";	
					$value1 = $linesplit[1];
					$type2 = "type"; 
					$value2 = $linesplit[2];
    			}
    			else if ($key == "vss")
    			{
    				$pattern1 = '/^(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)([[:alnum:]]|_|-|\$|&|%|\*)*$/'; //var pattern 
					$type1 = "var";	
					$value1 = $linesplit[1];
					if(preg_match('/^int@((\+|\-)?\d+)$/', $linesplit[2]))
					{
						$type2 = "int";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^nil@nil$/', $linesplit[2]))
					{
						$type2 = "nil";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^bool@(true|false)$/', $linesplit[2]))
					{
						$type2 = "bool";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^string@([^#\s\x5C]|\x5C[0-9]{3})*$/', $linesplit[2]))
					{
						$type2 = "string";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/', $linesplit[2]))
					{
						$type2 = "var";
						$value2 = $linesplit[2];
					}
					else
					{
						exit_program(23, "Non valid argument of the instruction.");
					} 
					if(preg_match('/^int@((\+|\-)?\d+)$/', $linesplit[3]))
					{
						$type3 = "int";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/^nil@nil$/', $linesplit[3]))
					{
						$type3 = "nil";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/^bool@(true|false)$/', $linesplit[3]))
					{
						$type3 = "bool";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/^string@([^#\s\x5C]|\x5C[0-9]{3})*$/', $linesplit[3]))
					{
						$type3 = "string";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/', $linesplit[3]))
					{
						$type3 = "var";
						$value3 = $linesplit[3];
					}
					else
					{
						exit_program(23, "Non valid argument of the instruction.");
					}
    			}
    			else if ($key == "lss")
    			{
    				$pattern1 = '/^([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/'; //label pattern
					$type1 = "label"; 
					$value1 = $linesplit[1];
					if(preg_match('/^int@((\+|\-)?\d+)$/', $linesplit[2]))
					{
						$type2 = "int";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^nil@nil$/', $linesplit[2]))
					{
						$type2 = "nil";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^bool@(true|false)$/', $linesplit[2]))
					{
						$type2 = "bool";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/^string@([^#\s\x5C]|\x5C[0-9]{3})*$/', $linesplit[2]))
					{
						$type2 = "string";
						$value2 = explode("@", $linesplit[2], 2);
						$value2 = $value2[1];
					}
					else if(preg_match('/(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/', $linesplit[2]))
					{
						$type2 = "var";
						$value2 = $linesplit[2];
					}
					else
					{
						exit_program(23, "Non valid argument of the instruction.");
					} 
					if(preg_match('/^int@((\+|\-)?\d+)$/', $linesplit[3]))
					{
						$type3 = "int";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/^nil@nil$/', $linesplit[3]))
					{
						$type3 = "nil";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/^bool@(true|false)$/', $linesplit[3]))
					{
						$type3 = "bool";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/^string@([^#\s\x5C]|\x5C[0-9]{3})*$/', $linesplit[3]))
					{
						$type3 = "string";
						$value3 = explode("@", $linesplit[3], 2);
						$value3 = $value3[1];
					}
					else if(preg_match('/(LF|TF|GF)@([[:alpha:]]|_|-|\$|&|%|\*)(\w|_|-|\$|&|%|\*)*$/', $linesplit[3]))
					{
						$type3 = "var";
						$value3 = $linesplit[3];
					}
					else
					{
						exit_program(23, "Non valid argument of the instruction.");
					}
    			}
    			if(strlen($key) == 1)
    			{
					xmlwriter_start_element($xml,"arg1");
					xmlwriter_start_attribute($xml,'type');
					xmlwriter_text($xml,$type);
					xmlwriter_end_attribute($xml);
					xmlwriter_text($xml, $value);
					xmlwriter_end_element($xml);
					 
					if(empty($linesplit[1]))
						exit_program(23, "First argument missing.");
					if(!preg_match($pattern, $linesplit[1]))
						exit_program(23, "First argument invalid.");
					if(!empty($linesplit[2]))
    					exit_program(23, "Too much arguments used.");
				}
				else if(strlen($key) == 2)
				{
					xmlwriter_start_element($xml,"arg1");
					xmlwriter_start_attribute($xml,'type');
					xmlwriter_text($xml,$type1);
					xmlwriter_end_attribute($xml);
					xmlwriter_text($xml, $value1);
					xmlwriter_end_element($xml);
					
					xmlwriter_start_element($xml,"arg2");
					xmlwriter_start_attribute($xml,'type');
					xmlwriter_text($xml,$type2);
					xmlwriter_end_attribute($xml);
					xmlwriter_text($xml, $value2);
					xmlwriter_end_element($xml);
					
					if (empty($linesplit[1]))
						exit_program(23, "One argument missing.");
					if (empty($linesplit[2]))
						exit_program(23, "One argument missing.");
					if(!preg_match($pattern1, $linesplit[1]))
						exit_program(23, "Invalid first argument of the instruction.");
					if(!preg_match($pattern2, $linesplit[2]))
						exit_program(23, "Invalid second argument of the instruction.");
					if(!empty($linesplit[3]))
    					exit_program(23, "Too much arguments used.");
				}
				else if(strlen($key) == 3)
				{
					xmlwriter_start_element($xml,"arg1");
					xmlwriter_start_attribute($xml,'type');
					xmlwriter_text($xml,$type1);
					xmlwriter_end_attribute($xml);
					xmlwriter_text($xml, $value1);
					xmlwriter_end_element($xml);
					
					xmlwriter_start_element($xml,"arg2");
					xmlwriter_start_attribute($xml,'type');
					xmlwriter_text($xml,$type2);
					xmlwriter_end_attribute($xml);
					xmlwriter_text($xml, $value2);
					xmlwriter_end_element($xml);
					
					xmlwriter_start_element($xml,"arg3");
					xmlwriter_start_attribute($xml,'type');
					xmlwriter_text($xml,$type3);
					xmlwriter_end_attribute($xml);
					xmlwriter_text($xml, $value3);
					xmlwriter_end_element($xml);
					
					if (empty($linesplit[1]))
						exit_program(23, "One argument missing.");
					if (empty($linesplit[2]))
						exit_program(23, "One argument missing.");
					if (empty($linesplit[3]))
						exit_program(23, "One argument missing.");
					if (!preg_match($pattern1, $linesplit[1]))
						exit_program(23, "Invalid first argument of the instruction.");
					if (!preg_match($symbol_pattern, $linesplit[2]))
						exit_program(23, "Invalid second argument of the instruction.");
					if (!preg_match($symbol_pattern, $linesplit[3]))
						exit_program(23, "Invalid third argument of the instruction.");
					if (!empty($linesplit[4]))
						exit_program(23, "Too much arguments used.");
				}
				else
					if (!empty($linesplit[1]))
						exit_program(23, "No arguments were expected.");
    			xmlwriter_end_element($xml);
    			$opcodefound = 1;
    		}
    	}
    }
}
if($flag_ippcode_comes == false)
	exit_program(21, "IPPcode19 non defined.");
xmlwriter_end_element($xml);/*ends program*/
xmlwriter_end_document($xml); /*ends document*/
/* Print XML representation of .IPPcode19 */
echo xmlwriter_output_memory($xml);

?>
