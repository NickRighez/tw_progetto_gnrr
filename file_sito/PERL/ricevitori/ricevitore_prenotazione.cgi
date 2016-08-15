#! /usr/bin/perl -w

use strict;
use warnings;
use diagnostics;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use lib "../libreria";
use data_registration;

my $q=CGI->new;

my %Prenotazione=(
	Username => $q->param('Username'),
	IDviaggio => $q->param('IDViaggio'),
	NumTappaPartenza => $q->param('NumTappaPartenza'),
	NumTappaArrivo => $q->param('NumTappaArrivo')
	);

data_registration::inserisci_prenotazione(\%Prenotazione);
