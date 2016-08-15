#!/usr/bin/perl
use strict;
use warnings;


print "Content-type: text/html\n\n";
print "created Session\n";

print("
	<form action=\"http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/s2.cgi\" method=\"POST\" >
		<input type=\"text\" name=\"nome\" >nome</input>
		<input type=\"submit\" value=\"invia\" />
		</form>
	");





