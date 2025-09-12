<?xml version="1.0" encoding="utf-8"?>
<!--

# Pretty Atom Feed

Based on "Pretty RSS Feed": https://github.com/genmon/aboutfeeds/issues/26

Styles an Atom feed, making it friendly for humans viewers, and adds a link
to aboutfeeds.com for new user onboarding. See it in action:

https://nicolas-hoizey.com/feeds/all.xml

-->
<xsl:stylesheet
    version="3.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" version="4.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title><xsl:value-of select="atom:feed/atom:title"/></title>
        <link rel="stylesheet" href="/css/rss.css"/>
      </head>
      <body>
        <main class="container">
          <header>
            <h1>
              Web Feed Preview
            </h1>
            <h2><xsl:value-of select="atom:feed/atom:title"/></h2>
            <p><xsl:value-of select="atom:feed/atom:description"/></p>
            <p>This preview only shows titles, but the actual feed contains the full abstract or description if present.</p>
            <a>
              <!-- <xsl:attribute name="href">
                <xsl:value-of select="/atom:feed/atom:link[not(@rel)]/@href"/>
              </xsl:attribute> -->
              <a href="/">Return to the Homepage &#x2192;</a>
            </a>
          </header>
          <h2>Recent Items</h2>
          <ul>
            <xsl:apply-templates select="atom:feed/atom:entry" />
          </ul>
        </main>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="atom:feed/atom:entry">
    <li class="item">
      <h3>
        <a>
          <xsl:attribute name="href">
            <xsl:value-of select="atom:link/@href"/>
          </xsl:attribute>
          <xsl:value-of select="atom:title"/>
        </a>
        <p>
          <small>
            <xsl:value-of select="atom:summary"/>
          </small>
        </p>
      </h3>
      <small class="gray">
        Published: <xsl:value-of select="atom:updated" />
      </small>
    </li>
  </xsl:template>
</xsl:stylesheet>