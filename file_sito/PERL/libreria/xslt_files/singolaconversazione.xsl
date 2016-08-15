<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
	<!--<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" /> -->

		    		
	<xsl:template match="/">
		
	
  

		    	<xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@User1='[% UTENTE %]' and @User2='[% MYSELF %]']/Messaggio | ts:TravelShare/SetMessaggi/Conversazione[@User1='[% MYSELF %]' and @User2='[% UTENTE %]']/Messaggio"> <!-- FILTRI PERL 'u1' 'u2' -->
					<xsl:choose>
						<xsl:when test=" Mittente ='[% MYSELF %]'  ">
							<div class="inviati" >
								<p class="intestazioneMsg"><xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/></p>
								<p><xsl:value-of select="Testo"/></p>
							</div>
						</xsl:when>
						<xsl:otherwise>
							<div class="ricevuti" >  <!-- DIVISIONE FRA LETTI E NON LETTI -->
								<xsl:if test="@Letto = 'no'">
									<p>NUOVO MESSAGGIO</p>
								</xsl:if>
								<p class="intestazioneMsg"><xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/></p>
								<p><xsl:value-of select="Testo"/></p>
							</div>
						</xsl:otherwise>
					</xsl:choose>


	    		</xsl:for-each> 
	    		</xsl:template>	
</xsl:stylesheet>
