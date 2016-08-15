<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
	

	<xsl:template match="/">
	    	<html><head></head><body>	
	    		<xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@User1='[% UTENTE %]' or @User2='[% UTENTE %]']"> <!-- FILTRI PERL '[% UTENTE %]' -->						
							<xsl:choose>
	    						<xsl:when test="/ts:TravelShare/SetMessaggi/Conversazione[@User1='[% UTENTE %]']"> <!-- mostra 1 come mittente quando io sono 2 e viceversa -->
	    							<xsl:choose>
	    							<xsl:when test="Messaggio[1]/@Letto='no'">
	    								<div class="conversazione nuova">
	    									<a href="http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi" title="Nuovo messaggio" class="">
		    									<xsl:value-of select="/ts:TravelShare/SetMessaggi/Conversazione/@User2"/>
		    									<span class="data"></span><xsl:value-of select="Messaggio[1]/Data"/> - <xsl:value-of select="Messaggio[1]/Ora"/></a>
		    									<p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p>
		    							</div>
	    							</xsl:when>
	    							<xsl:otherwise>
	    								<div class="conversazione">
	    									<a href="http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi" title="Nuovo messaggio" class="">
		    									<xsl:value-of select="/ts:TravelShare/SetMessaggi/Conversazione/@User2"/>
		    									<span class="data"></span><xsl:value-of select="Messaggio[1]/Data"/> - <xsl:value-of select="Messaggio[1]/Ora"/></a>
		    									<p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p>
		    							</div>
	    							</xsl:otherwise>
		    						</xsl:choose>	
	    						</xsl:when>
	    						<xsl:otherwise>
	    							<xsl:choose>
	    							<xsl:when test="Messaggio[1]/@Letto='no'">
	    								<div class="conversazione nuova">
	    									<a href="http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi" title="Nuovo messaggio" class="">
	    									<xsl:value-of select="/ts:TravelShare/SetMessaggi/Conversazione/@User1"/>
	    									<span class="data"></span><xsl:value-of select="Messaggio[1]/Data"/> - <xsl:value-of select="Messaggio[1]/Ora"/></a>
	    									<p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p>
	    								</div>
	    							</xsl:when>
	    							<xsl:otherwise>
	    								<div class="conversazione">
	    									<a href="http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi" title="Nuovo messaggio" class="">
	    									<xsl:value-of select="/ts:TravelShare/SetMessaggi/Conversazione/@User1"/>
	    									<span class="data"></span><xsl:value-of select="Messaggio[1]/Data"/> - <xsl:value-of select="Messaggio[1]/Ora"/></a>
	    									<p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p>
	    								</div>
	    							</xsl:otherwise>
	    							</xsl:choose>
	    						</xsl:otherwise>
	    					</xsl:choose>							 
				</xsl:for-each>
			</body></html>
	</xsl:template>
</xsl:stylesheet>
