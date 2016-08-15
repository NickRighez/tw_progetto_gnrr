#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;
use CGI ;
use CGI::Session qw/-ip-match/;
#use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser);  
use lib "../libreria";
use data_registration;

 my $cgi = new CGI;
 my %aux = data_registration::serializzazione_apertura();
my $doc = $aux{'doc'};
my $filehandle = $aux{'filehandle'};
my $username=$cgi->param('username');
my $psw=$cgi->param('password');
my @ute = $doc->findnodes("//SetUtenti/Utente[Username='$username' and Password='$psw']");
my $n = @ute;
if($n == 0) {
	data_registration::serializzazione_chiusura($filehandle,$doc);
	die("username/password non corretti");
}
else {
 #my $sid = $cgi->cookie("CGISESSID") || undef;
my $session    = new CGI::Session; #load CGI::Session(undef, $sid, {Directory=>'/tmp'});	
#print "Content-type: text/html\n\n";                      
$session->save_param($cgi);
$session->param('loggedin','yes');
$session->expires("+1h");
$session->flush();
print $session->header(-location => "http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/home.cgi");
 #print $cgi->redirect('http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/home.cgi');
}