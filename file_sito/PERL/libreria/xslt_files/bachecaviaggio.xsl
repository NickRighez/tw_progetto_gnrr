<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

		    			
	<xsl:template match="/">
		<xsl:if test="count(ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Bacheca/ConversazioneBacheca)=0">
			<p>Non ci sono messaggi per questo viaggio</p>
		</xsl:if>
		<xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Bacheca/ConversazioneBacheca">
			<div class="contenitore">
				<xsl:for-each select="Messaggio">
					<xsl:choose>
						<xsl:when test="Mittente=../../../Conducente">
							<div class="inviati">
								<p class="intestazioneMsg"><span class="mittenteMsg"><xsl:value-of select="Mittente"/></span><xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/></p>
								<p><xsl:value-of select="Testo"/></p>
							</div>
						</xsl:when>
						<xsl:otherwise>
							<div class="ricevuti">
								<p class="intestazioneMsg"><span class="mittenteMsg"><xsl:value-of select="Mittente"/></span><xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/></p>
								<p><xsl:value-of select="Testo"/></p>
							</div>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
				<xsl:if test="@User1='[% UTENTE %]' or @User2='[% UTENTE %]'">
					<textarea rows="" cols="" name="messaggio"></textarea>
					<div><input type="submit" value="Invia"></input></div>
				</xsl:if>
			</div>
		</xsl:for-each>
	</xsl:template>

</xsl:stylesheet>
		
	