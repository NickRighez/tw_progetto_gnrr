<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >

  

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
    		<xsl:for-each select="TravelShare/SetPassaggi/Passaggio">
        <xsl:for-each select="Itinerario/*" >    <!-- select="Itinerario" non produce nessun risultato  -->
           <xsl:if test="Provincia = &apos;ProvinciaPartenza&apos; and PostiDisp>0" >
              <xsl:variable name="ProvPart"> <xsl:value-of select="Provincia" /> </xsl:variable>
              <xsl:variable name="ComPart">  <xsl:value-of select="Comune" /> </xsl:variable>
              <xsl:variable name="Data">  <xsl:value-of select="Data" /> </xsl:variable>
              <xsl:variable name="Ora">  <xsl:value-of select="Ora" /> </xsl:variable>                                     
              <xsl:choose>
                <xsl:when test="following-sibling::*[position()=1]/Provincia=&apos;ProvinciaArrivo&apos; and 
                                following-sibling::*[position()=1]/PostiDisp>0" >
                    <div>
                      <p><span class="lab"> ID Viaggio: </span> <xsl:value-of select="../../IDViaggio"/> </p>
                      <p><span class="lab">Partenza: </span> <xsl:value-of select="$ProvPart" /> (<xsl:value-of select="$ComPart"/>)  <xsl:value-of select="$Data"/> - <xsl:value-of select="$Ora"/></p>
                      <p><span class="lab">Arrivo: </span> <xsl:value-of select="following-sibling::*[position()=1]/Provincia" /> (<xsl:value-of select="following-sibling::*[position()=1]/Comune" />) <xsl:value-of select="following-sibling::*[position()=1]/Data" /> - <xsl:value-of select="following-sibling::*[position()=1]/Ora" /></p>
                      <p><span class="lab">Prezzo: </span> <xsl:value-of select="following-sibling::*[position()=1]/Prezzo" />     </p> 
                    </div> 
                </xsl:when>
                <xsl:otherwise>
                  <xsl:if test="following-sibling::*[position()=1]/PostiDisp>0">
                    <xsl:choose>
                      <xsl:when test="following-sibling::*[position()=2]/Provincia=&apos;ProvinciaArrivo&apos; and 
                                      following-sibling::*[position()=2]/PostiDisp>0" >
                        <div>
                          <p><span class="lab"> ID Viaggio: </span> <xsl:value-of select="../../IDViaggio"/> </p>
                          <p><span class="lab">Partenza: </span> <xsl:value-of select="$ProvPart" /> (<xsl:value-of select="$ComPart" />) <xsl:value-of select="$Data"/> - <xsl:value-of select="$Ora"/></p>
                          <p><span class="lab">Arrivo: </span> <xsl:value-of select="following-sibling::*[position()=2]/Provincia" /> (<xsl:value-of select="following-sibling::*[position()=2]/Comune" />) <xsl:value-of select="following-sibling::*[position()=2]/Data" /> - <xsl:value-of select="following-sibling::*[position()=2]/Ora" /> </p>
                          <p><span class="lab">Prezzo: </span> <xsl:value-of select="following-sibling::*[position()=2]/Prezzo" />     </p> 
                        </div>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:if test="following-sibling::*[position()=2]/PostiDisp>0">
                          <xsl:choose>
                            <xsl:when test="following-sibling::*[position()=3]/Provincia=&apos;ProvinciaArrivo&apos; and
                                            following-sibling::*[position()=3]/PostiDisp>0" >
                              <div>
                                <p><span class="lab"> ID Viaggio: </span> <xsl:value-of select="../../IDViaggio"/> </p>
                                <p><span class="lab">Partenza: </span> <xsl:value-of select="$ProvPart" /> (<xsl:value-of select="$ComPart" />) <xsl:value-of select="$Data"/> - <xsl:value-of select="$Ora"/></p>
                                <p><span class="lab">Arrivo: </span> <xsl:value-of select="following-sibling::*[position()=3]/Provincia" /> (<xsl:value-of select="following-sibling::*[position()=3]/Comune" />) <xsl:value-of select="following-sibling::*[position()=3]/Data" /> - <xsl:value-of select="following-sibling::*[position()=3]/Ora" /> </p>
                                <p><span class="lab">Prezzo: </span> <xsl:value-of select="following-sibling::*[position()=3]/Prezzo" />     </p> 
                              </div> 
                            </xsl:when>
                            <xsl:otherwise>
                              <xsl:if test="following-sibling::*[position()=3]/PostiDisp>0">
                                <xsl:choose>
                                  <xsl:when test="following-sibling::*[position()=4]/Provincia=&apos;ProvinciaArrivo&apos; and
                                                  following-sibling::*[position()=4]/PostiDisp>0" >" >
                                    <div>
                                      <p><span class="lab"> ID Viaggio: </span> <xsl:value-of select="../../IDViaggio"/> </p>
                                      <p><span class="lab">Partenza: </span> <xsl:value-of select="$ProvPart" /> (<xsl:value-of select="$ComPart" />) <xsl:value-of select="$Data"/> - <xsl:value-of select="$Ora"/></p>
                                      <p><span class="lab">Arrivo: </span> <xsl:value-of select="following-sibling::*[position()=4]/Provincia" /> (<xsl:value-of select="following-sibling::*[position()=4]/Comune" />) <xsl:value-of select="following-sibling::*[position()=4]/Data" /> - <xsl:value-of select="following-sibling::*[position()=4]/Ora" /> </p>
                                      <p><span class="lab">Prezzo: </span> <xsl:value-of select="following-sibling::*[position()=4]/Prezzo" />     </p> 
                                    </div> 
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
</xsl:stylesheet>

