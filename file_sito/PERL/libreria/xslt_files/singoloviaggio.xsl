<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

		    			
	<xsl:template match="/">
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it" >
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
				<title>Info Singolo Passaggio </title>
				<meta name="title" content="VISUALIZZAZIONE VIAGGIO XSLT" />
	  			<style type="text/css" media="all">
	  				.lab {
	            		color:red;
			          }
			          div {
			            border:2px solid black;
			            margin: 2px;
			          }
			          p {
			            margin: 4px;
			          }
			          div.pas {
			          	border:2px solid red;
			          }
			          div.risp {
			          	border:2px solid green;
			          }
			          div.mess {
			          	border:2px solid blue;
			          }

	  			</style>
	    	</head>
	    	<body>
	    		<xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='v2' and */*/@Numero=0]" > <!-- 2 FILTRI PERL -->
	    			<div class="pas">
	    				<h3>Informazioni generali : </h3>
	    				
	    				<p>Conducente : <xsl:call-template name="conducente">
	    									<xsl:with-param name="cond"><xsl:value-of select="Conducente"/></xsl:with-param>
	    								</xsl:call-template> 
	    				</p>	    					
	    				<p>Prezzo : <xsl:value-of select="PrezzoTot"/> Euro </p>
	    				<p>Posti disponibili ??? </p>  <!-- da sistemare -->
	    				<p>Dettagli : <xsl:value-of select="Dettagli"/> </p>
	    				<h3>Partenza : </h3>
	    				<p>Luogo : <xsl:value-of select="Itinerario/*[@Numero=0]/Comune"/>(<xsl:value-of select="Itinerario/*[@Numero=0]/Provincia"/>) </p>
	    				<p>Data/Ora : <xsl:value-of select="Itinerario/*[@Numero=0]/Data"/> - <xsl:value-of select="Itinerario/*[@Numero=0]/Ora"/> </p>
	    				<p>Posti disponibili : <xsl:value-of select="Itinerario/*[@Numero=0]/PostiDisp"/> </p>
	    				<h3>Arrivo : </h3>
	    				<p>Luogo : <xsl:value-of select="Itinerario/*[@Numero=1]/Comune"/>(<xsl:value-of select="Itinerario/*[@Numero=1]/Provincia"/>) </p>
	    				<p>Data/Ora : <xsl:value-of select="Itinerario/*[@Numero=1]/Data"/> - <xsl:value-of select="Itinerario/*[@Numero=1]/Ora"/> </p>
	    				<p>Posti disponibili : <xsl:value-of select="Itinerario/*[@Numero=1]/PostiDisp"/> </p>
	    				<div class="bacheca">
	    					<h3>Bacheca Messaggi</h3>
	    					<xsl:apply-templates select="*/MessaggioBacheca" />
	    				</div>
	    			</div>
	    		</xsl:for-each>
	    	</body>
	    </html>
	</xsl:template>

	<xsl:template match="*/MessaggioBacheca">
		<div class="mess">
  		<p> Mittente :	<xsl:call-template name="conducente">
  	    				<xsl:with-param name="cond"><xsl:value-of select="Mittente"/></xsl:with-param>
  	    			</xsl:call-template>  </p>
  	  	<p>Data/Ora : <xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/> </p>
  	  	<p>Testo : <xsl:value-of select="Testo"/> </p>
  	  	<xsl:if test="count(Risposte)!=0">
  	    		<div class="risp">
  	    			<h3>Risposte</h3>
  	    			<xsl:apply-templates select="*/MessaggioBacheca"/>
  	    		</div>
  		</xsl:if>
	  </div>
	</xsl:template>

	<xsl:template name="conducente" >
		<xsl:param name="cond"/>
		<span><xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[IDUte=$cond]/Nome"/></span>
	  <span><xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[IDUte=$cond]/Cognome"/></span>
	</xsl:template>

	
</xsl:stylesheet>
