#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;




my $q=CGI->new;
my $session = new CGI::Session;
$session->load();

if(!defined($session->param('loggedin'))) {
	die("not logged");
}
my $username = $session->param('username'); 

my %Prenotazione=(
	Username => $username,
	IDViaggio => $q->param('passaggio'),
	NumTappaPartenza => $q->param('part'),
	NumTappaArrivo => $q->param('arr')
	);

data_registration::inserisci_prenotazione(\%Prenotazione);