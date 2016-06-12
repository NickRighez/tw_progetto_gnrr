<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
	<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

	<xsl:template match="/">
		
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it" >
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
				<title>Info Utente</title>
				<meta name="title" content="RICERCA XSLT" />
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
			          span {
			          	margin-right: 10px;
			          }
	  			</style>
	    	</head>
	    	<body>
	    		<h1>Messaggi</h1> 
	    		
	    		<xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@IDUte1='u1' or @IDUte2='u1']"> <!-- FILTRI PERL 'u1' -->
					<div class="conversazione">
						<a href="singolaConversazione.html" title="Nuovo messaggio" class="">
							<xsl:choose>
	    						<xsl:when test="/ts:TravelShare/SetMessaggi/Conversazione[@IDUte1='u1']"> <!-- FILTRO PERL 'u1' -->
	    							<xsl:call-template name="utente">
										<xsl:with-param name="idute"><xsl:value-of select="/ts:TravelShare/SetMessaggi/Conversazione/@IDUte2"/></xsl:with-param>
									</xsl:call-template>
	    						</xsl:when>
	    						<xsl:otherwise>
	    							<xsl:call-template name="utente">
										<xsl:with-param name="idute"><xsl:value-of select="/ts:TravelShare/SetMessaggi/Conversazione/@IDUte1"/></xsl:with-param>
									</xsl:call-template>
	    						</xsl:otherwise>
	    					</xsl:choose>							
							<span class="data"><xsl:value-of select="Messaggio[1]/Data"/></span>
						 	<span class="ora"><xsl:value-of select="Messaggio[1]/Ora"/></span>
						</a> 
						<p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p>
					</div>
				</xsl:for-each>
	    	</body>
	    </html>
	</xsl:template>

	<xsl:template name="utente">
		<xsl:param name="idute" />
		<p><span class="nome"><xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[IDUte=$idute]/Nome"/></span>
		    <span class="cognome"><xsl:value-of select="/ts:TravelShare/SetUtenti/Utente[IDUte=$idute]/Cognome"/></span>
		</p>
	</xsl:template>
</xsl:stylesheet>
