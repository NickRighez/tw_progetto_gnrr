#! /usr/bin/perl

use strict;
use warnings;
use CGI::Carp 'fatalsToBrowser';

#use lib '/etc/perl:/usr/local/lib/perl/5.18.2:/usr/local/share/perl/5.18.2:/usr/lib/perl5:/usr/share/perl5:/usr/lib/perl/5.18:/usr/share/perl/5.18:/usr/local/lib/site_perl:';
use libreria::research;

#print "Content-type: text/html\n\n";
#print "<html><head> <title>Ciao mondo!!!!</title></head><body>";

#print "<h1>Fucking awesome!!!!!!!!!!!!!!!!</h1>";


#research::test_function();
print "Content-type: text/html\r\n\r\n";




my @params = ("anno &gt; 2000", "autore = 'King'");
my $out = research::query_users(@params);
#generic_xslt_query('libreria/style.xsl',@params);
#$out=~ s/<?xml version="1.0" encoding="UTF-8" standalone="yes"?>/ /;

print  $out;
#print "</body></html>";
