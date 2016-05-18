<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method='html' encoding='UTF-8' indent='yes'
		omit-xml-declaration="yes"
              doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
              doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />
  <xsl:template match="/" >
  	<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
  		<head>
  			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  			<title>Esempio stupido su libri</title>
  			<meta name="title" content="Esempio stupido su libri" />
  			<style>
  				.blocco{border-style: solid;}
  				span{padding-right:30px;padding-left:10px;}
  			</style>
    	</head>
    	<body>
    		<!-- select="/child::lista/child::libro[[% FILTRO1 %]]" -->
    		<h1>Libri</h1>
    		<p><huge>FUNZIONA!!!!!!!!!!!!!!!!!!!!!</huge></p>

    	</body>
    </html>
  </xsl:template>
</xsl:stylesheet>
