<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" >
	<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

	<xsl:template match="/">
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it" >
			<head>
				<meta http-equiv="content-type" content="text/html; charset=utf-8" />
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
			          div.ute {
			          	border:2px solid red;
			          }
			          span {
			          	margin-right: 10px;
			          }
	  			</style>
	    	</head>
	    	<body>
	    		<xsl:for-each select="ts:TravelShare/SetUtenti/Utente[IDUte='[% UTENTE %]']" >  <!--  FILTRO PERL -->
	    			<div id="contenuto">
	    				<div class="info">
	    					
	    					<h2><span id="nome"><xsl:value-of select="Nome"/></span><span id="cognome"><xsl:value-of select="Cognome"/></span> </h2>
	    					<p>Sesso : <xsl:value-of select="Sesso"/> </p>
	    					<p>Anno di nascita : <xsl:value-of select="AnnoNascita"/> </p>
	    				</div>
	    				<div class="descrizione">
	    					<p>Descrizione : <xsl:value-of select="Profilo/DescrizionePers" /></p>
	    					<p>Anno di rilascio della patente: </p>
	    						<xsl:choose>
		    						<xsl:when test="count(Profilo/Patente)=0">
		    							<p> L utente non ha impostato informazioni sulla patente. </p>
		    						</xsl:when>
		    						<xsl:otherwise>
		    							<p><xsl:value-of select="Profilo/Patente/@DataRilascio"/></p>
		    						</xsl:otherwise>
		    					</xsl:choose>
		    				<div id="auto">
			    				<p>Auto:</p>
			    					<xsl:choose>
			    						<xsl:when test="count(Profilo/Auto)=0">
			    							<p> L utente non ha impostato informazioni sull auto. </p>
			    						</xsl:when>
			    						<xsl:otherwise>
			    							<p>Marca: <xsl:value-of select="Profilo/Auto/Marca"/></p>
			    							<p>Modello: <xsl:value-of select="Profilo/Auto/Modello"/></p>
			    							<p>Tipologia: <xsl:value-of select="Profilo/Auto/Tipologia"/></p>
			    						</xsl:otherwise>
			    					</xsl:choose>
			    				</div>

	    					<div id="feedback">
	    						<h5>Feedback</h5>
		    					<p>Feedback ricevuti : <xsl:value-of select="Profilo/NumFeedbRicevuti"/> </p> 
		    					<p>Passaggi offerti : <xsl:value-of select="Profilo/NumPassaggiOff"/> </p>
		    					<p>Passaggi partecipati : <xsl:value-of select="Profilo/NumPassaggiPart"/> </p>

		    					<h5>Valutazione</h5>
		    					<p>Punteggio medio : <xsl:value-of select="Profilo/valutazione/Punteggiomedio"/> </p>
		    					<p>Compagnia : <xsl:value-of select="Profilo/Valutazione/Compagnia"/> </p>
		    					<p>Puntualità : <xsl:value-of select="Profilo/Valutazione/Puntualita"/> </p>
		    					<p>Pulizia : <xsl:value-of select="Profilo/Valutazione/Pulizia"/> </p>
		    					<p>Guida : <xsl:value-of select="Profilo/Valutazione/Guida"/> </p>
		    				</div>

	    					<h5>Preferenze</h5>
	    					<xsl:choose>
	    						<xsl:when test="count(Profilo/Preferenze)=0">
	    							<p> L utente non ha impostato le preferenze. </p>
	    						</xsl:when>
	    						<xsl:otherwise>
	    							<xsl:for-each select="Profilo/Preferenze/*">
	    								<xsl:choose>
	    									<xsl:when test="current()=0">
	    										<p> <xsl:value-of select="name()" /> : Mai  </p>
	    									</xsl:when>
	    									<xsl:when test="current()=1">
	    										<p> <xsl:value-of select="name()" /> : Occasionalmente  </p>
	    									</xsl:when>
	    									<xsl:otherwise>
	    										<p> <xsl:value-of select="name()" /> : Spesso/Sempre  </p>	    										
	    									</xsl:otherwise>
	    								</xsl:choose>
	    							</xsl:for-each>
	    						</xsl:otherwise>
	    					</xsl:choose>
	    				</div>
	    			</div>
	    		</xsl:for-each>
	    	</body>
	    </html>
	</xsl:template>
</xsl:stylesheet>
