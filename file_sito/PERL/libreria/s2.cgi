#!/usr/bin/perl
use strict;
use warnings;

use CGI qw/:standard/;
use CGI::Session qw/-ip-match/;
use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);

my $cgi = new CGI;
my $session = CGI::Session->new(undef, undef, {Directory=>'/tmp'});

#setting session to expire in 1 hour
#$session->expire("+1h");

#store something
$session->param("value1","yakub");

#write to disk
$session->flush();

my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
 print $cgi->redirect('http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/libreria/s3.cgi');
 
