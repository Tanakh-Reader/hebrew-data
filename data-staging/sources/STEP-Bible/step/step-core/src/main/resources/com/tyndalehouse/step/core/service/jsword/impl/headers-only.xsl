<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:jsword="http://xml.apache.org/xalan/java"
                extension-element-prefixes="jsword">
    <xsl:param name="VNum" select="'false'"/>
    <xsl:param name="CVNum" select="'false'"/>
    <xsl:param name="BCVNum" select="'false'"/>
    <xsl:param name="TinyVNum" select="'false'"/>
    <xsl:param name="v11n" select="'KJV'"/>
    <xsl:variable name="v11nf" select="jsword:org.crosswire.jsword.versification.system.Versifications.instance()"/>
    <xsl:variable name="versification" select="jsword:getVersification($v11nf, $v11n)"/>
    <xsl:variable name="shaper" select="jsword:org.crosswire.common.icu.NumberShaper.new()"/>
    <xsl:variable name="keyf" select="jsword:org.crosswire.jsword.passage.PassageKeyFactory.instance()"/>
    <xsl:variable name="tracker" select="jsword:java.util.concurrent.atomic.AtomicBoolean.new()"/>

    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="//row"><xsl:apply-templates select="//row"/></xsl:when>
            <xsl:otherwise>
                <xsl:for-each select="//verse">
                    <xsl:variable name="titleInCell"
                                  select="(.//title[not(starts-with(@type, 'x-'))])[1]"/>
                    <xsl:variable name="previousTitle"
                                  select="(./preceding-sibling::title[not(starts-with(@type, 'x-'))])[1]"/>

                    <xsl:choose>
                        <xsl:when test="$titleInCell">
                            <span>
                                <xsl:apply-templates select="."/>
                            </span>
                            <span class="subjectHeading">
                                <xsl:apply-templates select="$titleInCell"/>
                            </span>
                    </xsl:when>
                        <xsl:otherwise>
                            <span>
                                <xsl:apply-templates select="."/>
                            </span>
                            <span class="subjectHeading">
                                <xsl:apply-templates select="$previousTitle"/>
                            </span>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:for-each>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>


    <xsl:template match="row">
        <xsl:value-of select="jsword:set($tracker, false())"/>
        <xsl:if test=".//verse">
            <xsl:for-each select="./cell">
                <xsl:if test="jsword:get($tracker) = false()">
                    <xsl:variable name="titleInCell"
                                  select="(.//title[not(starts-with(@type, 'x-'))])[1]"/>
                    <xsl:variable name="previousTitle"
                                  select="(./preceding-sibling::title[not(starts-with(@type, 'x-'))])[1]"/>
                    <xsl:choose>
                        <xsl:when test="$titleInCell">
                            <span>
                                <xsl:apply-templates select=".//verse[1]"/>
                            </span>
                            <span class="subjectHeading">
                                <xsl:apply-templates select="$titleInCell"/>
                            </span>
                        </xsl:when><xsl:when test="$previousTitle">
                            <span>
                                <xsl:apply-templates select=".//verse[1]"/>
                            </span>
                            <span class="subjectHeading">
                                <xsl:apply-templates select="$previousTitle"/>
                            </span>
                        </xsl:when>
                        <xsl:otherwise>
                            <!-- we look for the previous cell and check whether it's got a pre-verse marker -->
                            <xsl:variable name="previousCell"
                                          select="../preceding-sibling::row/cell[position()]"/>
                            <xsl:choose>
                                <xsl:when test="$previousCell and $previousCell//*[@subType = 'x-preverse']">
                                    <span>
                                        <xsl:apply-templates select=".//verse[1]"/>
                                    </span>
                                    <span class="subjectHeading">
                                        <xsl:apply-templates select="($previousCell//title[not(starts-with(@type, 'x-'))])[1]"/>
                                    </span>
                                </xsl:when>
                                <xsl:otherwise></xsl:otherwise>
                            </xsl:choose>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:if>
            </xsl:for-each>
        </xsl:if>
    </xsl:template>

    <xsl:template match="note"><!-- Do not output notes --></xsl:template>
    <xsl:template match="title"><xsl:apply-templates /><xsl:value-of select="jsword:set($tracker, true())"/></xsl:template>
    <xsl:template match="divineName">
        <span class="small-caps">
            <xsl:apply-templates/>
        </span>
    </xsl:template>


    <xsl:template match="verse">
        <!-- we output version names not verse numbers for interleaved translations -->
        <!-- Are verse numbers wanted? -->
        <xsl:if test="$VNum = 'true'">
            <!-- An osisID can be a space separated list of them -->
            <xsl:variable name="firstOsisID" select="substring-before(concat(@osisID, ' '), ' ')"/>
            <xsl:variable name="book" select="substring-before($firstOsisID, '.')"/>
            <xsl:variable name="chapter"
                          select="jsword:shape($shaper, substring-before(substring-after($firstOsisID, '.'), '.'))"/>
            <!-- If n is present use it for the number -->
            <xsl:variable name="verse">
                <xsl:choose>
                    <xsl:when test="@n">
                        <xsl:value-of select="jsword:shape($shaper, string(@n))"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of
                                select="jsword:shape($shaper, substring-after(substring-after($firstOsisID, '.'), '.'))"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="versenum">
                <xsl:variable name="passage" select="jsword:getValidKey($keyf, $versification, @osisID)"/>
                <xsl:value-of select="jsword:getName($passage)"/>
            </xsl:variable>
            <!--
              == Surround versenum with dup
              -->
            <a name="{@osisID}">
                <span class="verseNumber"><xsl:value-of select="$versenum"/>&#160;
                </span>
            </a>
        </xsl:if>
    </xsl:template>



    <xsl:template match="q[@sID or @eID]">
        <xsl:choose>
            <xsl:when test="@marker"><xsl:value-of select="@marker"/></xsl:when>
            <!-- The chosen mark should be based on the work's author's locale. -->
            <xsl:otherwise>"</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="q[@type = 'blockquote']">
        <span class="q"><xsl:value-of select="@marker"/><xsl:apply-templates/><xsl:value-of select="@marker"/></span>
    </xsl:template>

    <xsl:template match="q[@type = 'citation']">
        <span class="q"><xsl:value-of select="@marker"/><xsl:apply-templates/><xsl:value-of select="@marker"/></span>
    </xsl:template>

    <xsl:template match="q[@type = 'embedded']">
        <xsl:choose>
            <xsl:when test="@marker">
                <xsl:value-of select="@marker"/><xsl:apply-templates/><xsl:value-of select="@marker"/>
            </xsl:when>
            <xsl:otherwise>
                <quote class="q"><xsl:apply-templates/></quote>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="q[@type = 'embedded']" mode="jesus">
        <xsl:choose>
            <xsl:when test="@marker">
                <xsl:value-of select="@marker"/><xsl:apply-templates mode="jesus"/><xsl:value-of select="@marker"/>
            </xsl:when>
            <xsl:otherwise>
                <quote class="q"><xsl:apply-templates/></quote>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>