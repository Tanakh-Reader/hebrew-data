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
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import com.tyndalehouse.step.core.service.VocabularyService;
import org.crosswire.common.util.Language;
import org.crosswire.jsword.book.Book;
import org.crosswire.jsword.passage.KeyFactory;
import org.crosswire.jsword.passage.NoSuchKeyException;
import org.crosswire.jsword.passage.PassageKeyFactory;
import org.crosswire.jsword.passage.VerseFactory;
import org.crosswire.jsword.versification.Versification;
import org.crosswire.jsword.versification.system.SystemKJV;
import org.crosswire.jsword.versification.system.Versifications;
import org.junit.Test;

/**
 * A simple test class to test to the provider
 * 
 * @author chrisburrell
 * 
 */
public class InterlinearProviderImplTest {
    /**
     * this checks that when keyed with strong, morph and verse number, we can retrieve the word. We should be
     * able to retrieve by (strong,morph), regardless of verse number. We should also be able to retrieve by
     * (strong,verse number)
     * 
     * @throws InvocationTargetException reflection exception which should fail the test
     * @throws IllegalAccessException reflection exception which should fail the test
     * @throws NoSuchMethodException reflect exception which should fail the test
     */
    @Test
    public void testInterlinearStrongMorphBased() throws NoSuchKeyException {
        final InterlinearProviderImpl interlinear = new InterlinearProviderImpl();
        final Book mock = mock(Book.class);
        final VocabularyService vocabularyService = mock(VocabularyService.class);
        interlinear.setCurrentBook(mock);
        interlinear.setVocabProvider(vocabularyService);
        when(mock.getLanguage()).thenReturn(new Language("fr"));


        // NOTE: because we don't want to expose a method called during initialisation as non-private (could
        // break
        // the initialisation, of the provider, we use reflection to open up its access for testing purposes!

        Versification NRSV = Versifications.instance().getVersification("NRSV");
        interlinear.addTextualInfo(VerseFactory.fromString(NRSV, "Gen.1.1"), "strong", "word", "");
        assertEquals(interlinear.getWord(PassageKeyFactory.instance().getKey(
                NRSV, "Gen.1.1"), "strong", false), "word");
        assertEquals(interlinear.getWord(PassageKeyFactory.instance().getKey(
                NRSV, "Gen.2.1"), "strong", false), "");
    }
}
