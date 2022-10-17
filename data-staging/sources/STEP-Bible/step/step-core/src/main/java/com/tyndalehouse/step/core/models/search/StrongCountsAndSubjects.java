/*******************************************************************************
 * Copyright (c) 2012, Directors of the Tyndale STEP Project
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without 
 * modification, are permitted provided that the following conditions 
 * are met:
 * 
 * Redistributions of source code must retain the above copyright 
 * notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright 
 * notice, this list of conditions and the following disclaimer in 
 * the documentation and/or other materials provided with the 
 * distribution.
 * Neither the name of the Tyndale House, Cambridge (www.TyndaleHouse.com)  
 * nor the names of its contributors may be used to endorse or promote 
 * products derived from this software without specific prior written 
 * permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
 * IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
 * THE POSSIBILITY OF SUCH DAMAGE.
 ******************************************************************************/
package com.tyndalehouse.step.core.models.search;

import com.tyndalehouse.step.core.models.LexiconSuggestion;

import java.util.List;
import java.util.Map;
import java.util.SortedSet;

/**
 * A holder for counts of strongs in the bibles and the actual Strongs data
 */
public class StrongCountsAndSubjects {
    private Map<String, List<LexiconSuggestion>> strongData;
    private Map<String, BookAndBibleCount> counts;
    private boolean ot;
    private String verse;
    private boolean multipleVerses;

    /**
     * Sets the counts.
     * 
     * @param counts the counts
     */
    public void setCounts(final Map<String, BookAndBibleCount> counts) {
        this.counts = counts;
    }

    /**
     * Sets the strong data.
     * 
     * @param strongData the strong data
     */
    public void setStrongData(final Map<String, List<LexiconSuggestion>> strongData) {
        this.strongData = strongData;
    }

    /**
     * @return the strongData
     */
    public Map<String, List<LexiconSuggestion>> getStrongData() {
        return this.strongData;
    }

    /**
     * @return the counts
     */
    public Map<String, BookAndBibleCount> getCounts() {
        return this.counts;
    }

    /**
     * @return the ot
     */
    public boolean isOt() {
        return this.ot;
    }

    /**
     * @param otValue the ot to set
     */
    public void setOT(final boolean otValue) {
        this.ot = otValue;
    }

    public void setVerse(String verse) {
        this.verse = verse;
    }

    public String getVerse() {
        return verse;
    }

    public void setMultipleVerses(boolean multipleVerses) {
        this.multipleVerses = multipleVerses;
    }

    public boolean isMultipleVerses() {
        return multipleVerses;
    }
}
