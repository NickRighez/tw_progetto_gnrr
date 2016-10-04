<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:ts="http://www.dominio.com" >



  <xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'
              doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
              doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

  <xsl:template match="/" >
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Ricerca passaggio</title>
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
        </style>
      </head>
      <body>
        <xsl:for-each select="ts:TravelShare/SetPassaggi/Passaggio">
          <xsl:for-each select="Itinerario/*" >    <!-- select="Itinerario" non produce nessun risultato  -->
            <xsl:if test="Provincia = '[% PARTENZA %]' and PostiDisp>0" > <!-- FILTRO PERL -->
              <xsl:variable name="ProvPart"> <xsl:value-of select="Provincia" /> </xsl:variable>
              <xsl:variable name="ComPart">  <xsl:value-of select="Comune" /> </xsl:variable>
              <xsl:variable name="Data">  <xsl:value-of select="Data" /> </xsl:variable>
              <xsl:variable name="Ora">  <xsl:value-of select="Ora" /> </xsl:variable>
              <xsl:choose>
                <xsl:when test="following-sibling::*[position()=1]/Provincia=&apos;ProvinciaArrivo&apos; and
                                following-sibling::*[position()=1]/PostiDisp>0" > <!-- FILTRO PERL -->
                  <xsl:call-template name="InfoPassaggio">
                    <xsl:with-param name="pos">1</xsl:with-param>
                    <xsl:with-param name="ProvPart"><xsl:value-of select="$ProvPart"/></xsl:with-param>
                    <xsl:with-param name="ComPart"><xsl:value-of select="$ComPart"/></xsl:with-param>
                    <xsl:with-param name="Data"><xsl:value-of select="$Data"/></xsl:with-param>
                    <xsl:with-param name="Ora"><xsl:value-of select="$Ora"/></xsl:with-param>
                  </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:if test="following-sibling::*[position()=1]/PostiDisp>0">
                    <xsl:choose>
                      <xsl:when test="following-sibling::*[position()=2]/Provincia=&apos;ProvinciaArrivo&apos; and
                                      following-sibling::*[position()=2]/PostiDisp>0" > <!-- FILTRO PERL -->
                        <xsl:call-template name="InfoPassaggio">
                          <xsl:with-param name="pos">2</xsl:with-param>
                          <xsl:with-param name="ProvPart"><xsl:value-of select="$ProvPart"/></xsl:with-param>
                          <xsl:with-param name="ComPart"><xsl:value-of select="$ComPart"/></xsl:with-param>
                          <xsl:with-param name="Data"><xsl:value-of select="$Data"/></xsl:with-param>
                          <xsl:with-param name="Ora"><xsl:value-of select="$Ora"/></xsl:with-param>
                        </xsl:call-template>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:if test="following-sibling::*[position()=2]/PostiDisp>0">
                          <xsl:choose>
                            <xsl:when test="following-sibling::*[position()=3]/Provincia=&apos;ProvinciaArrivo&apos; and
                                            following-sibling::*[position()=3]/PostiDisp>0" > <!-- FILTRO PERL -->
                              <xsl:call-template name="InfoPassaggio">
                                <xsl:with-param name="pos">3</xsl:with-param>
                                <xsl:with-param name="ProvPart"><xsl:value-of select="$ProvPart"/></xsl:with-param>
                                <xsl:with-param name="ComPart"><xsl:value-of select="$ComPart"/></xsl:with-param>
                                <xsl:with-param name="Data"><xsl:value-of select="$Data"/></xsl:with-param>
                                <xsl:with-param name="Ora"><xsl:value-of select="$Ora"/></xsl:with-param>
                              </xsl:call-template>
                            </xsl:when>
                            <xsl:otherwise>
                              <xsl:if test="following-sibling::*[position()=3]/PostiDisp>0">
                                <xsl:choose>
                                  <xsl:when test="following-sibling::*[position()=4]/Provincia=&apos;ProvinciaArrivo&apos; and
                                                  following-sibling::*[position()=4]/PostiDisp>0" >
                                    <xsl:call-template name="InfoPassaggio">
                                      <xsl:with-param name="pos">4</xsl:with-param>
                                      <xsl:with-param name="ProvPart"><xsl:value-of select="$ProvPart"/></xsl:with-param>
                                      <xsl:with-param name="ComPart"><xsl:value-of select="$ComPart"/></xsl:with-param>
                                      <xsl:with-param name="Data"><xsl:value-of select="$Data"/></xsl:with-param>
                                      <xsl:with-param name="Ora"><xsl:value-of select="$Ora"/></xsl:with-param>
                                    </xsl:call-template>
                                  </xsl:when>
                                </xsl:choose>
                              </xsl:if>
                            </xsl:otherwise>
                          </xsl:choose>
                        </xsl:if>
                      </xsl:otherwise>
                    </xsl:choose>
                  </xsl:if>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:if>
          </xsl:for-each>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>

  <xsl:template name="InfoPassaggio">
    <xsl:param name="pos"/>
    <xsl:param name="ProvPart"/>
    <xsl:param name="ComPart"/>
    <xsl:param name="Data"/>
    <xsl:param name="Ora"/>
    <div>
      <p><span class="lab"> ID Viaggio: </span> <xsl:value-of select="../../IDViaggio"/> </p>
      <p><span class="lab">Partenza: </span> <xsl:value-of select="$ProvPart" /> (<xsl:value-of select="$ComPart" />) <xsl:value-of select="$Data"/> - <xsl:value-of select="$Ora"/></p>
      <p><span class="lab">Arrivo: </span> <xsl:value-of select="following-sibling::*[position()=$pos]/Provincia" /> (<xsl:value-of select="following-sibling::*[position()=$pos]/Comune" />) <xsl:value-of select="following-sibling::*[position()=$pos]/Data" /> - <xsl:value-of select="following-sibling::*[position()=$pos]/Ora" /> </p>
      <p><span class="lab">Prezzo: </span> <xsl:value-of select="following-sibling::*[position()=$pos]/Prezzo" />     </p>
    </div>
  </xsl:template>
</xsl:stylesheet>
