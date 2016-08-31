<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
	

	<xsl:template match="/">
	
	    		<xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@User1='[% UTENTE %]' or @User2='[% UTENTE %]']"> <!-- FILTRI PERL '[% UTENTE %]' -->						
							<xsl:choose>
	    						<xsl:when test="@User1='[% UTENTE %]'"> <!-- mostra 1 come mittente quando io sono 2 e viceversa -->
	    							<xsl:choose>
	    							<xsl:when test="Messaggio[1]/@Letto='no'">
	    								<div class="conversazione nuova">
	    									<xsl:call-template name="conversazione">
	    										<xsl:with-param name="utente" select="@User2" />
	    									</xsl:call-template>
		    							</div>
	    							</xsl:when>
	    							<xsl:otherwise>
	    								<div class="conversazione">
	    									<xsl:call-template name="conversazione">
	    										<xsl:with-param name="utente" select="@User2" />
	    									</xsl:call-template>
		    							</div>
	    							</xsl:otherwise>
		    						</xsl:choose>	
	    						</xsl:when>
	    						<xsl:otherwise>
	    							<xsl:choose>
	    							<xsl:when test="Messaggio[1]/@Letto='no'">
	    								<div class="conversazione nuova">
	    									<xsl:call-template name="conversazione">
	    										<xsl:with-param name="utente" select="@User1" />
	    									</xsl:call-template>
	    								</div>
	    							</xsl:when>
	    							<xsl:otherwise>
	    								<div class="conversazione">
	    									<xsl:call-template name="conversazione">
	    										<xsl:with-param name="utente" select="@User1" />
	    									</xsl:call-template>
	    								</div>
	    							</xsl:otherwise>
	    							</xsl:choose>
	    						</xsl:otherwise>
	    					</xsl:choose>							 
				</xsl:for-each>
	</xsl:template>

	<xsl:template name="conversazione" >
  		<xsl:param name="utente" />
  			<a>
	    		<xsl:attribute name="href">http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/assemblatori/assemblatore_singola_conversaz.cgi?utente=<xsl:value-of select="$utente" /></xsl:attribute>
		    	<xsl:attribute name="title"></xsl:attribute>
		    	<xsl:attribute name="class"></xsl:attribute>
		    	<xsl:value-of select="$utente" />
		    	<span class="data"></span><xsl:value-of select="Messaggio[1]/Data"/> - <xsl:value-of select="Messaggio[1]/Ora"/>
		    </a>
		    <p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p>
	</xsl:template>
</xsl:stylesheet>
