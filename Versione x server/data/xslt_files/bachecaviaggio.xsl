<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com">
  <!-- <xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" omit-xml-declaration="yes"/> -->


  <xsl:template match="/"> 
    <h2>Bacheca dei messaggi</h2>
    <xsl:if test="count(ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Bacheca/ConversazioneBacheca)=0">
      <div class="contenitore"><p>Non ci sono messaggi per questo viaggio</p></div> 
    </xsl:if>
    <xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio[IDViaggio='[% VIAGGIO %]']/Bacheca/ConversazioneBacheca">
      <div class="contenitore">                                                               <xsl:text>&#xa;</xsl:text>
        <xsl:for-each select="Messaggio">
          <xsl:choose>
            <xsl:when test="Mittente=../../../Conducente">
              <div class="inviati">                                                          <xsl:text>&#xa;</xsl:text>
                <p class="intestazioneMsg"><span class="mittenteMsg"><xsl:value-of select="Mittente"/></span><xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/></p>                                                         <xsl:text>&#xa;</xsl:text>
                <p><xsl:value-of select="Testo"/></p>                                                         <xsl:text>&#xa;</xsl:text>
              </div>                                                         <xsl:text>&#xa;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
              <div class="ricevuti">                                                         <xsl:text>&#xa;</xsl:text>
                <p class="intestazioneMsg"><span class="mittenteMsg"><xsl:value-of select="Mittente"/></span><xsl:value-of select="Data"/> - <xsl:value-of select="Ora"/></p>                                                         <xsl:text>&#xa;</xsl:text>
                <p><xsl:value-of select="Testo"/></p>                                                         <xsl:text>&#xa;</xsl:text>
              </div>                                                         <xsl:text>&#xa;</xsl:text>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
        <xsl:if test="@User1='[% UTENTE %]' or @User2='[% UTENTE %]'">
          <form action="ricevitore_messaggio_pubblico.cgi" method="POST">                                                          <xsl:text>&#xa;</xsl:text>
            <xsl:choose>
<!-- non si ha mai il caso in cui l User1 sia il conducente del passaggio associato alla bacheca -->
              <xsl:when test="../../Conducente='[% UTENTE %]' and @User1='[% UTENTE %]'">
                <input>
                  <xsl:attribute name="type">hidden</xsl:attribute>
                  <xsl:attribute name="name">mittente</xsl:attribute>
                  <xsl:attribute name="value">[% UTENTE %]</xsl:attribute>
                </input>                                                         <xsl:text>&#xa;</xsl:text>
                <input>
                  <xsl:attribute name="type">hidden</xsl:attribute>
                  <xsl:attribute name="name">destinatario</xsl:attribute>
                  <xsl:attribute name="value"><xsl:value-of select="@User2"/></xsl:attribute>
                </input>                                                         <xsl:text>&#xa;</xsl:text>
              </xsl:when>
              <xsl:when test="../../Conducente='[% UTENTE %]' and @User2='[% UTENTE %]'">
                <input>
                  <xsl:attribute name="type">hidden</xsl:attribute>
                  <xsl:attribute name="name">mittente</xsl:attribute>
                  <xsl:attribute name="value">[% UTENTE %]</xsl:attribute>
                </input>                                                         <xsl:text>&#xa;</xsl:text>
                <input>
                  <xsl:attribute name="type">hidden</xsl:attribute>
                  <xsl:attribute name="name">destinatario</xsl:attribute>
                  <xsl:attribute name="value"><xsl:value-of select="@User1"/></xsl:attribute>
                </input>                                                         <xsl:text>&#xa;</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <input>
                  <xsl:attribute name="type">hidden</xsl:attribute>
                  <xsl:attribute name="name">mittente</xsl:attribute>
                  <xsl:attribute name="value">[% UTENTE %]</xsl:attribute>
                </input>                                                         <xsl:text>&#xa;</xsl:text>
                <input>
                  <xsl:attribute name="type">hidden</xsl:attribute>
                  <xsl:attribute name="name">destinatario</xsl:attribute>
                  <xsl:attribute name="value"><xsl:value-of select="../../Conducente"/></xsl:attribute>
                </input>                                                         <xsl:text>&#xa;</xsl:text>
              </xsl:otherwise>
            </xsl:choose>
            <input>
              <xsl:attribute name="type">hidden</xsl:attribute>
              <xsl:attribute name="name">passaggio</xsl:attribute>
              <xsl:attribute name="value">[% VIAGGIO %]</xsl:attribute>
            </input>                                                         <xsl:text>&#xa;</xsl:text>
            <input>
              <xsl:attribute name="type">hidden</xsl:attribute>
              <xsl:attribute name="name">partenza</xsl:attribute>
              <xsl:attribute name="value">[% NUM_PARTENZA %]</xsl:attribute>
            </input>                                                         <xsl:text>&#xa;</xsl:text>
            <input> 
              <xsl:attribute name="type">hidden</xsl:attribute>
              <xsl:attribute name="name">arrivo</xsl:attribute>
              <xsl:attribute name="value">[% NUM_ARRIVO %]</xsl:attribute>
            </input>                                                         <xsl:text>&#xa;</xsl:text>
            <textarea rows="0" cols="0" name="messaggio"> Inserisci un messaggio per il conducente.
            </textarea>                                                         <xsl:text>&#xa;</xsl:text>

            <div>                                                         <xsl:text>&#xa;</xsl:text>
              <input type="submit" value="Invia"></input>                                                         <xsl:text>&#xa;</xsl:text>
            </div>                                                         <xsl:text>&#xa;</xsl:text>
          </form>                                                         <xsl:text>&#xa;</xsl:text>
        </xsl:if>

      </div>                                                         <xsl:text>&#xa;</xsl:text>
    </xsl:for-each>
    
  </xsl:template>

</xsl:stylesheet>
