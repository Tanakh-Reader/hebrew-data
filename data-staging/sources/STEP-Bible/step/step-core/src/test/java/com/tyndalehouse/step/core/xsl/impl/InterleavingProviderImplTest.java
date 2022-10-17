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
package com.tyndalehouse.step.core.xsl.impl;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.crosswire.jsword.book.Book;
import org.crosswire.jsword.book.Books;
import org.junit.Test;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;

import com.tyndalehouse.step.core.service.jsword.JSwordVersificationService;

/**
 * A simple test class to test to the provider
 * 
 * @author chrisburrell
 * 
 */
public class InterleavingProviderImplTest {

    /**
     * check that comparing adds the right set of versions
     */
    @Test
    public void testInterleavingCompare() {
        final JSwordVersificationService versification = mock(JSwordVersificationService.class);

        when(versification.getBookFromVersion(anyString())).thenAnswer(new Answer<Book>() {

            @Override
            public Book answer(final InvocationOnMock invocation) {
                return Books.installed().getBook((String) invocation.getArguments()[0]);
            }
        });

        final InterleavingProviderImpl interleavingProviderImpl = new InterleavingProviderImpl(versification,
                new String[] { "KJV", "ESV_th", "NETfree", "Byz", "Tisch", "YLT", "ASV", "Montgomery",
                        "FreCrampon" }, true);

        final String[] expected = new String[] { "KJV", "ESV_th", "KJV", "NETfree", "KJV", "YLT", "KJV", "ASV",
                "KJV", "Montgomery", };
        assertEqualVersions(expected, interleavingProviderImpl);
    }

    /**
     * Tests that the main version obliterates the presence of the same version within the list.
     */
    @Test
    public void testInterleavingCompareWithSameVersion() {
        final JSwordVersificationService versification = mock(JSwordVersificationService.class);

        when(versification.getBookFromVersion(anyString())).thenAnswer(new Answer<Book>() {

            @Override
            public Book answer(final InvocationOnMock invocation) {
                return Books.installed().getBook((String) invocation.getArguments()[0]);
            }
        });

        final InterleavingProviderImpl interleavingProviderImpl = new InterleavingProviderImpl(versification,
                new String[] { "KJV", "ESV_th", "KJV", "ESV_th"}, true);

        assertEqualVersions(new String[] { "KJV", "ESV_th", "KJV", "ESV_th"}, interleavingProviderImpl);
    }



    /**
     * check that comparing adds the right set of versions
     */
    @Test
    public void testInterleavingNoCompare() {
        final InterleavingProviderImpl interleavingProviderImpl = new InterleavingProviderImpl(null,
                new String[] { "ESV_th", "SBLGNT" }, false);

        final String[] expected = new String[] { "ESV_th", "SBLGNT" };
        assertEqualVersions(expected, interleavingProviderImpl);
    }

    /**
     *
     * @param expected the expected versions
     * @param interleavingProviderImpl the provider of versions
     */
    private void assertEqualVersions(final String[] expected, final InterleavingProviderImpl interleavingProviderImpl) {
        for (int ii = 0; ii < expected.length; ii++) {
            assertEquals(expected[ii], interleavingProviderImpl.getVersions()[ii]);
        }
    }
}
