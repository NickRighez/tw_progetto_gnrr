<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
	<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

		    		
	<xsl:template match="/">
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it" >
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
				<title>Singola Conversazione </title>
				<meta name="title" content="VISUALIZZAZIONE SINGOLA CONVERSAZIONE" />
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
			          p.mess {
			          	border:2px solid green;
			          }
			          div.mess {
			          	border:2px solid blue;
			          }
			          span {
			          	margin-right: 10px;

			          }

	  			</style>
	    	</head>
	    	<body>
		    	<xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@IDUte1='u2' and @IDUte2='u1']/Messaggio"> <!-- FILTRI PERL 'u1' 'u2' -->
		    		<div class="mess">
		    			<p>Mittente : <xsl:call-template name="mittente">
		    							        <xsl:with-param name="mitt"><xsl:value-of select="Mittente"/></xsl:with-param>
		    						        </xsl:call-template> <span><xsl:value-of select="Data"/></span><span><xsl:value-of select="Ora"/></span></p>
		    			<p class="mess"><xsl:value-of select="Testo"/></p>
		    		</div>
	    		</xsl:for-each> 
	    	</body>
	    </html>
	</xsl:template>

	<xsl:template name="mittente" >
		<xsl:param name="mitt"/>
		<span><xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[IDUte=$mitt]/Nome"/></span>
	   <span><xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[IDUte=$mitt]/Cognome"/></span>
	</xsl:template>

	
</xsl:stylesheet>
