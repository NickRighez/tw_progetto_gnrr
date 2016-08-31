#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
use CGI ;
use CGI::Session qw/-ip-match/;
#use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);  
use lib "../libreria";
use sessione; 

my $q = new CGI;
sessione::distruzione();

print $q->redirect("http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_home.cgi");