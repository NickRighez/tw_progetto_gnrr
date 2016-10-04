<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" >
	<!-- <xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" omit-xml-declaration="yes"/> -->

	<xsl:template match="/">
		<h1>Viaggi</h1>
		<h2>Viaggi Attivi</h2>
		<xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio[@passato='no' and Itinerario/*/Prenotazioni/Utente=[% UTENTE %]]">
			<div class="viaggio">
				<xsl:for-each select="Itinerario/*[Prenotazioni/Utente=[% UTENTE %]]">
				</xsl:for-each>
			</div>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet> 
