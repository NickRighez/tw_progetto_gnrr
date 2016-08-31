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
							<form action="http://localhost/cgi-bin/tw_progetto_gnrr/file_sito/PERL/ricevitori/ricevitore_messaggio_pubblico.cgi" method="POST">
							<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">passaggio</xsl:attribute>
										<xsl:attribute name="value">[% VIAGGIO %]</xsl:attribute>
							</input>
							<xsl:choose>
								<xsl:when test="../../Conducente='[% UTENTE %]' and @User1='[% UTENTE %]'">
									<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">mittente</xsl:attribute>
										<xsl:attribute name="value">[% UTENTE %]</xsl:attribute>
									</input>
									<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">destinatario</xsl:attribute>
										<xsl:attribute name="value"><xsl:value-of select="../@User2"/></xsl:attribute>
									</input>
								</xsl:when>
								<xsl:when test="../../Conducente='[% UTENTE %]' and @User2='[% UTENTE %]'">
									<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">mittente</xsl:attribute>
										<xsl:attribute name="value">[% UTENTE %]</xsl:attribute>
									</input> 
									<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">destinatario</xsl:attribute>
										<xsl:attribute name="value"><xsl:value-of select="../@User1"/></xsl:attribute>
									</input>
								</xsl:when>
								<xsl:otherwise>
									<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">mittente</xsl:attribute>
										<xsl:attribute name="value">[% UTENTE %]</xsl:attribute>
									</input>
									<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">destinatario</xsl:attribute>
										<xsl:attribute name="value"><xsl:value-of select="../../Conducente"/></xsl:attribute>
									</input>
								</xsl:otherwise>
							</xsl:choose>
							<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">passaggio</xsl:attribute>
										<xsl:attribute name="value">[% VIAGGIO %]</xsl:attribute>
							</input> 
							<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">partenza</xsl:attribute>
										<xsl:attribute name="value">[% NUM_PARTENZA %]</xsl:attribute>
									</input>
							<input>
										<xsl:attribute name="type">hidden</xsl:attribute>
										<xsl:attribute name="name">arrivo</xsl:attribute>
										<xsl:attribute name="value">[% NUM_ARRIVO %]</xsl:attribute>
									</input>		
								<textarea rows="" cols="" name="messaggio"></textarea>
								<div><input type="submit" value="Invia"></input></div>
							</form>
				</xsl:if>
						
			</div>
		</xsl:for-each>
	</xsl:template>

</xsl:stylesheet>
		
	