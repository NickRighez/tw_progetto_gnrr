#!/usr/bin/perl
#print "Content-Type: text/html; charset=UTF-8\n\n";

use strict;
use warnings;
use diagnostics;
use CGI qw(-utf8);
use CGI::Session qw/-ip-match/;
use CGI::Carp qw(fatalsToBrowser);
use libreria::data_registration;
use libreria::sessione;
use utf8;
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":utf8";
use Encode qw(decode_utf8);

my $cgi = new CGI;
my @s = sessione::creaSessione();
my $session = $s[0];


if(defined($session->param('nuova_regis'))) {
    my $aux = $session->param('nuova_regis');
    my %ute = %$aux;
    $session->param('username',$ute{'Username'});
    $session->param('loggedin','yes');
    $session->flush();
    $session->clear(['nuova_regis']);
    print $session->header(-location => "confermaRegistrazione.cgi");
}
elsif($cgi->request_method() eq "POST") {
    my $doc = data_registration::get_xml_doc();;
    my $username=$cgi->param('username');
    my $psw=$cgi->param('password');
    my @ute = $doc->findnodes("//SetUtenti/Utente[Username='$username' and Password='$psw']");
    my $n = @ute;
    if($n == 0) {
        my %problems = (
            LOGIN_ERR => "Combinazione username/password non corretta."
            );
        my %old_input = (
            USERNAME => $username,
            PASSWORD => $psw
            );
        $session->param('problems',\%problems);
        $session->param('old_input',\%old_input);
        print $session->header(-location => "login.cgi");
    }
    else {

        $session->param('username',$username);
        $session->param('loggedin','yes');
        $session->expires("+2h"); 
        $session->flush();
        data_registration::aggiorna_feedback_da_rilasciare();
        print $session->header(-location => "home.cgi");
    }
}
else {
     my %problems=(
          LOGIN_ERR => "Tentativo di effettuare il login in modalit&agrave; non permessa."
     );
     $session->param('problems',\%problems);
    print $session->header(-location => "login.cgi");
}
