<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" exclude-result-prefixes="ts" >
  <!-- <xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes' doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" omit-xml-declaration="yes"/> -->

   <xsl:variable name="Anno_n">
    <xsl:value-of select="ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/AnnoNascita" />
  </xsl:variable>

  <xsl:variable name="eta">
    <xsl:value-of select=" [% ANNO_C %] - $Anno_n" />
  </xsl:variable>

  <xsl:template match="/">
    <xsl:for-each select="ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']" >  <!--  FILTRO PERL -->
      <div class="contenitore">
        <p>Sesso: <xsl:value-of select="Sesso"/> <span class="destra"> <xsl:value-of select="$eta" /> anni</span></p><xsl:text>&#x0A;</xsl:text>

        <div class="descrizione">
        <p>Descrizione:
          <xsl:choose>
            <xsl:when test="DescrizionePers[not(normalize-space(.))]">
              L&#39;utente non ha inserito una descrizione.
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="DescrizionePers" />
          </xsl:otherwise>
          </xsl:choose>
        </p><xsl:text>&#x0A;</xsl:text>
      </div>
        <xsl:choose>
          <xsl:when test="count(Profilo/Patente)=0">

              <p>L&#39;utente non ha impostato informazioni sulla patente.</p><xsl:text>&#x0A;</xsl:text>
              <p>L&#39;utente non ha impostato informazioni sull&#39;auto.</p><xsl:text>&#x0A;</xsl:text>
              <p>L&#39;utente non ha impostato informazioni sulle proprie preferenze.</p><xsl:text>&#x0A;</xsl:text>

          </xsl:when>
          <xsl:otherwise>
            <p>Anno di rilascio della patente: <xsl:value-of select="Profilo/Patente"/></p><xsl:text>&#x0A;</xsl:text>
            <p>Automobile: <xsl:value-of select="Profilo/Auto"/></p><xsl:text>&#x0A;</xsl:text>
            <p>Preferenze:</p><xsl:text>&#x0A;</xsl:text>
            <div class="preferenzeGroup">
              <xsl:choose>
                <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Chiacchiere=0">
                  <img src="../Immagini/BLA0.png" class="preferenze4Img" alt="Silenzioso" title="Silenzioso"></img>
                </xsl:when>
                <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Chiacchiere=1">
                  <img src="../Immagini/BLA1.png" class="preferenze4Img" alt="Poche Chiacchiere" title="Poche Chiacchiere"></img>
                </xsl:when>
                <xsl:otherwise>
                  <img src="../Immagini/BLA2.png" class="preferenze4Img" alt="Chiacchierone" title="Chiacchierone"></img>
                </xsl:otherwise>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Musica=0">
                  <img src="../Immagini/musica0.png" class="preferenze4Img" alt="Non ascolto musica" title="Non ascolto musica"></img>
                </xsl:when>
                <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Musica=1">
                  <img src="../Immagini/musica1.png" class="preferenze4Img" alt="Ascolto musica" title="Ascolto musica"></img>
                </xsl:when>
                <xsl:otherwise>
                  <img src="../Immagini/musica2.png" class="preferenze4Img" alt="Ascolto spesso musica" title="Ascolto spesso musica"></img>
                </xsl:otherwise>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Animali=0">
                  <img src="../Immagini/animali0.png" class="preferenze4Img" alt="No animali" title="No animali"></img>
                </xsl:when>
                <xsl:otherwise>
                  <img src="../Immagini/animali1.png" class="preferenze4Img" alt="Accetto animali" title="Accetto animali"></img>
                </xsl:otherwise>
              </xsl:choose>
              <xsl:choose>
                <xsl:when test="/ts:TravelShare/SetUtenti/Utente[Username='[% UTENTE %]']/Profilo/Preferenze/Fumatore=0">
                  <img src="../Immagini/fumo0.png" class="preferenze4Img" alt="No fumatori" title="No fumatori"></img>
                </xsl:when>
                <xsl:otherwise>
                  <img src="../Immagini/fumo1.png" class="preferenze4Img" alt="Accetto fumatori" title="Accetto fumatori"></img>
                </xsl:otherwise>
              </xsl:choose>
            </div>
          </xsl:otherwise>
        </xsl:choose>
      </div>
      <h2>Feedback</h2>
      <div class="contenitore">
        <p>Passaggi offerti: <xsl:value-of select="Profilo/NumPassaggiOff"/> </p><xsl:text>&#x0A;</xsl:text>
        <p>Passaggi partecipati: <xsl:value-of select="Profilo/NumPassaggiPart"/> </p><xsl:text>&#x0A;</xsl:text>
        <p>Punteggio medio: <xsl:value-of select="format-number(Profilo/Valutazione/PunteggioMedio,'0.0')"/> su <xsl:value-of select="Profilo/NumFeedbRicevuti"/> feedback ricevuti</p><xsl:text>&#x0A;</xsl:text>
        <p>Compagnia: <xsl:value-of select="format-number(Profilo/Valutazione/Compagnia,'0.0')"/> </p><xsl:text>&#x0A;</xsl:text>
        <p>Puntualità: <xsl:value-of select="format-number(Profilo/Valutazione/Puntualita,'0.0')"/> </p><xsl:text>&#x0A;</xsl:text>
        <p>Pulizia: <xsl:value-of select="format-number(Profilo/Valutazione/Pulizia,'0.0')"/> </p><xsl:text>&#x0A;</xsl:text>
        <p>Guida: <xsl:value-of select="format-number(Profilo/Valutazione/Guida,'0.0')"/> </p><xsl:text>&#x0A;</xsl:text>
      </div>
    </xsl:for-each>
    <div id="commenti"> <!--serve il div?-->
      <h3>Commenti degli utenti</h3>
      <xsl:if test="count(ts:TravelShare/SetFeedback/Feedback[@IDDest='[% UTENTE %]']/Commento)=0">
        <div class="contenitore"><p>L&#39;utente non ha ricevuto nessun commento.</p><xsl:text>&#x0A;</xsl:text></div>
      </xsl:if>
      <xsl:for-each select="ts:TravelShare/SetFeedback/Feedback[@IDDest='[% UTENTE %]']/Commento" >
        <div class="commentoUtente">
          <p class="intestazioneMsg"><span class="mittenteMsg"><xsl:value-of select="@IDMitt"/></span></p><xsl:text>&#x0A;</xsl:text>
          <p><xsl:value-of select="Commento" /></p><xsl:text>&#x0A;</xsl:text>
        </div>
      </xsl:for-each>
    </div>
  </xsl:template>
</xsl:stylesheet>
