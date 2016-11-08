#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session qw/-ip-match/;
#use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);
#use lib "../libreria";
use libreria::sessione;

my $q = new CGI;
sessione::distruzione();

print $q->redirect("home.cgi");
