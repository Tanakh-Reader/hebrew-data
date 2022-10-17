package com.tyndalehouse.step.core.data.filters;

import java.io.IOException;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.TermAttribute;

/**
 * Cleans up transliterations by removing any extra character
 * 
 * @author chrisburrell
 * 
 */
public class BetaTransliterationCleaningFilter extends TokenFilter {
    private final TermAttribute termAtt;

    /**
     * @param input the token stream
     */
    public BetaTransliterationCleaningFilter(final TokenStream input) {
        super(input);
        this.termAtt = addAttribute(TermAttribute.class);
    }

    @Override
    public boolean incrementToken() throws IOException {
        if (this.input.incrementToken()) {
            final char[] buffer = this.termAtt.termBuffer();

            final StringBuilder buf = new StringBuilder(buffer.length);

            char lastChar = 0x0;
            for (int i = 0; i < this.termAtt.termLength(); i++) {
                // skip two characters in a row
                final char currentChar = buffer[i];
                if (lastChar == currentChar) {
                    continue;
                }
                lastChar = currentChar;

                appendNonBetaSpecialChar(buffer, buf, i, currentChar);
            }

            if (buf.length() != buffer.length) {
                final char[] output = new char[buf.length()];
                buf.getChars(0, buf.length(), output, 0);
                this.termAtt.setTermBuffer(output, 0, output.length);
            }
            return true;
        } else {
            return false;
        }
    }

    /**
     * Appends a character if it does not form part of the BETA spec
     * 
     * @param buffer the word that is being transliterated
     * @param buf the builder we are using to build up the transliteration
     * @param i the current position
     * @param currentChar our current character
     */
    // CHECKSTYLE:OFF
    private void appendNonBetaSpecialChar(final char[] buffer, final StringBuilder buf, final int i,
            final char currentChar) {
        // CHECKSTYLE:ON
        // caters for the beta code as well
        switch (currentChar) {
            case '-':
            case '\'':
            case '/':
            case '\\':
            case ')':
            case '(':
            case '=':
            case '*':
            case '+':
            case '|':
            case '&':
                break;
            default:
                buf.append(buffer[i]);
        }
    }
}
