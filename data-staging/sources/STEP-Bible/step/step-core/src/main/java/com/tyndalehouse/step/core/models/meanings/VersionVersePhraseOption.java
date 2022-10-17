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
package com.tyndalehouse.step.core.models.meanings;

import java.util.List;

/**
 * Represents a portion of text that has alternatives.
 */
public class VersionVersePhraseOption {
    private final String matchingText;
    private final String context;
    private final List<VersionPhraseAlternative> phraseAlternatives;

    /**
     * Instantiates a new version verse phrase option.
     * 
     * @param matchingText the matching text
     * @param context the context to find the text within, usually preceding
     * @param phraseAlternatives the phrase alternatives
     */
    public VersionVersePhraseOption(final String matchingText, final String context,
            final List<VersionPhraseAlternative> phraseAlternatives) {
        this.matchingText = matchingText;
        this.context = context;
        this.phraseAlternatives = phraseAlternatives;
    }

    /**
     * Gets the matching text.
     * 
     * @return the matching text
     */
    public String getMatchingText() {
        return this.matchingText;
    }

    /**
     * Gets the phrase alternatives.
     * 
     * @return the phrase alternatives
     */
    public List<VersionPhraseAlternative> getPhraseAlternatives() {
        return this.phraseAlternatives;
    }

    /**
     * @return the context
     */
    public String getContext() {
        return this.context;
    }
}
