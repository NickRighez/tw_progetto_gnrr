<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" exclude-result-prefixes="ts" >
  <xsl:template match="/">

    <xsl:for-each select="ts:TravelShare/SetMessaggi/Conversazione[@User1='[% UTENTE %]' or @User2='[% UTENTE %]']"> <!-- FILTRI PERL '[% UTENTE %]' -->
      <xsl:choose>
        <xsl:when test="@User1='[% UTENTE %]'"> <!-- mostra 1 come mittente quando io sono 2 e viceversa -->
          <xsl:choose>
            <xsl:when test="Messaggio[1]/@Letto='no'">
              <div class="conversazione nuova">
                <xsl:call-template name="conversazione_nuova">
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
                <xsl:call-template name="conversazione_nuova">
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
[%  stag = "\[\%"
    etag = "\%\]"
%]
  <xsl:template name="conversazione" >
    <xsl:param name="utente" />
    <a>
      <xsl:attribute name="href">singola_conversaz.cgi?utente=<xsl:value-of select="$utente" /></xsl:attribute>
      <xsl:attribute name="title">Messaggio letto</xsl:attribute>
      <xsl:attribute name="class">linkMobile</xsl:attribute>
      <xsl:attribute name="tabindex">[% stag;  ' INDEX '; etag; %]</xsl:attribute>
      [% stag; ' INDEX = INDEX+1 '; etag;  %]
      <xsl:value-of select="$utente" />
      <span class="data">
        <xsl:call-template name="formatdate">
          <xsl:with-param name="datestr" select="Messaggio[1]/Data" />
          </xsl:call-template> -
          <xsl:call-template name="formathour">
            <xsl:with-param name="hourstr" select="Messaggio[1]/Ora" />
          </xsl:call-template>
      </span>
    </a>
    <p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p><xsl:text>&#x0A;</xsl:text>
    <p class="linkVaiConversazione">
      <a>
        <xsl:attribute name="href">singola_conversaz.cgi?utente=<xsl:value-of select="$utente" /></xsl:attribute>
        <xsl:attribute name="tabindex">[% stag;  ' INDEX '; etag; %]</xsl:attribute>
        [% stag; ' INDEX = INDEX+1 '; etag;  %]
        Vai alla conversazione <xsl:text disable-output-escaping="yes">&amp;raquo;</xsl:text>
      </a>
    </p><xsl:text>&#x0A;</xsl:text>
  </xsl:template>

  <xsl:template name="conversazione_nuova" >
    <xsl:param name="utente" />
    <a>
      <xsl:attribute name="href">singola_conversaz.cgi?utente=<xsl:value-of select="$utente" /></xsl:attribute>
      <xsl:attribute name="title">Nuovo messaggio</xsl:attribute>
      <xsl:attribute name="class">linkMobile</xsl:attribute>
       <xsl:attribute name="tabindex">[% stag;  ' INDEX '; etag; %]</xsl:attribute>
      [% stag; ' INDEX = INDEX+1 '; etag;  %]
      <xsl:value-of select="$utente" />
      <span class="data">
        <xsl:call-template name="formatdate">
          <xsl:with-param name="datestr" select="Messaggio[1]/Data" />
        </xsl:call-template>
        -
        <xsl:call-template name="formathour">
          <xsl:with-param name="hourstr" select="Messaggio[1]/Ora" />
        </xsl:call-template>

      </span>
    </a>
    <p class="ultimoMessaggio"><xsl:value-of select="Messaggio[1]/Testo"/></p><xsl:text>&#x0A;</xsl:text>
    <p class="linkVaiConversazione blacktext">
      <a>
        <xsl:attribute name="href">singola_conversaz.cgi?utente=<xsl:value-of select="$utente" /></xsl:attribute>
        <xsl:attribute name="tabindex">[% stag;  ' INDEX '; etag; %]</xsl:attribute>
        [% stag; ' INDEX = INDEX+1 '; etag;  %]
        Vai alla conversazione <xsl:text disable-output-escaping="yes">&amp;raquo; </xsl:text>
      </a>
    </p><xsl:text>&#x0A;</xsl:text>
  </xsl:template>

  <xsl:template name="formatdate">
    <xsl:param name="datestr" />
    <!-- input format yyyy-mm-dd -->
    <!-- output format dd-mm-yyyy -->

    <xsl:variable name="mm">
      <xsl:value-of select="substring($datestr,6,2)" />
    </xsl:variable>

    <xsl:variable name="dd">
      <xsl:value-of select="substring($datestr,9,2)" />
    </xsl:variable>

    <xsl:variable name="yyyy">
      <xsl:value-of select="substring($datestr,1,4)" />
    </xsl:variable>

    <xsl:value-of select="$dd" />
    <xsl:value-of select="'-'" />
    <xsl:value-of select="$mm" />
    <xsl:value-of select="'-'" />
    <xsl:value-of select="$yyyy" />
  </xsl:template>
  
  <xsl:template name="formathour">
    <xsl:param name="hourstr" />
    <!-- input format hh:mm:ss -->
    <!-- output format hh:mm -->

    <xsl:variable name="hh">
      <xsl:value-of select="substring($hourstr,1,2)" />
    </xsl:variable>

    <xsl:variable name="mm">
      <xsl:value-of select="substring($hourstr,4,2)" />
    </xsl:variable>

    <xsl:value-of select="$hh" />
    <xsl:value-of select="':'" />
    <xsl:value-of select="$mm" />
  </xsl:template>

</xsl:stylesheet>
