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
use lib "libreria";
use sessione;

 my $cgi = new CGI;
 my @s = sessione::creaSessione();  
 my $session = $s[0];
my $doc = data_registration::get_xml_doc();;
my $username=$cgi->param('username');
my $psw=$cgi->param('password');
my @ute = $doc->findnodes("//SetUtenti/Utente[Username='$username' and Password='$psw']");
my $n = @ute;
if($n == 0) {
	my %problems = (
		login_err => "Combinazione username/password non corretta."
		);
	my %old_input = (
		username => $username,
		password => $psw
		);
	$session->param('problems',\%problems);
	$session->param('old_input',\%old_input);
	#print $cgi->redirect('http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/accedi.cgi');
	print $session->header(-location => "../assemblatore_login.cgi");
}
else {
 #my $sid = $cgi->cookie("CGISESSID") || undef;
	
$session->param('username',$username);
$session->param('loggedin','yes');
#$session->expires("+1h");
$session->flush();
print $session->header(-location => "../assemblatore_home.cgi");
 #print $cgi->redirect('http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/home.cgi');
}