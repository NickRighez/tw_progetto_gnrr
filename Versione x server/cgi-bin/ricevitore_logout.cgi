#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session qw/-ip-match/;
use CGI::Carp qw(fatalsToBrowser);
use libreria::sessione;
use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use Encode qw(decode_utf8);

my $q = new CGI;
sessione::distruzione();

print $q->redirect("home.cgi");
