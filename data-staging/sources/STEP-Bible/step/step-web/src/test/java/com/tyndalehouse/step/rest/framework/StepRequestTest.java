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
package com.tyndalehouse.step.rest.framework;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;

import org.junit.Test;

/**
 * Tests that cache keys are constructed correctly
 * 
 * @author chrisburrell
 * 
 */
public class StepRequestTest {
    private static final String UTF_8_ENCODING = "UTF-8";
    private static final String[] TEST_ARGS = new String[] { "arg1", "arg2", "arg3" };
    private static final String TEST_CONTROLLER_NAME = "Controller";
    private static final String TEST_METHOD_NAME = "method";
    private static final String TEST_URI = "uri/ControllerController/method/arg1/arg2/arg3";

    /**
     * a method key should not contain arguments, but contain controller name and method name
     */
    @Test
    public void testMethodKey() {
        final StepRequest stepRequest = getTestStepRequest();
        final String methodKey = stepRequest.getCacheKey().getMethodKey();
        assertTrue(methodKey.contains(TEST_CONTROLLER_NAME));
        assertTrue(methodKey.contains(TEST_METHOD_NAME));
        for (final String s : TEST_ARGS) {
            assertFalse(methodKey.contains(s));
        }
    }

    /**
     * A result key should contain controller, method and arguments
     */
    @Test
    public void testResultKey() {
        final StepRequest stepRequest = getTestStepRequest();
        final String resultsKey = stepRequest.getCacheKey().getResultsKey();
        assertTrue(resultsKey.contains(TEST_CONTROLLER_NAME));
        assertTrue(resultsKey.contains(TEST_METHOD_NAME));
        for (final String s : TEST_ARGS) {
            assertTrue(resultsKey.contains(s));
        }

    }

    /**
     * testing simple parsing of arguments
     */
    @Test
    public void testParseArguments() {
        // index starts at ...........0123456789-123456789-123456
        final String stepRequest = "step-web/rest/bible/get/1K2/2K2/";
        final HttpServletRequest req = mock(HttpServletRequest.class);

        when(req.getRequestURI()).thenReturn(stepRequest);
        when(req.getServletPath()).thenReturn("step-web/");
        when(req.getContextPath()).thenReturn("rest/");

        // index starts at ...........0123456789-123456789-123456
        final StepRequest sr = new StepRequest(req, UTF_8_ENCODING);
        assertEquals(2, sr.getArgs().length);
        assertEquals("1K2", sr.getArgs()[0]);
        assertEquals("2K2", sr.getArgs()[1]);
    }

    /**
     * tests that parsing of request works if request finishes with a slash
     */
    @Test
    public void testGetArgsFinishingWithSlash() {
        // index starts at ...........0123456789-123456789-123456
        final String sampleRequest = "step-web/rest/bible/get/1K2/2K2/";
        final HttpServletRequest req = mock(HttpServletRequest.class);

        when(req.getRequestURI()).thenReturn(sampleRequest);
        when(req.getServletPath()).thenReturn("step-web/");
        when(req.getContextPath()).thenReturn("rest/");

        final StepRequest sr = new StepRequest(req, UTF_8_ENCODING);

        // then
        assertEquals(2, sr.getArgs().length);
        assertEquals("1K2", sr.getArgs()[0]);
        assertEquals("2K2", sr.getArgs()[1]);
    }

    /**
     * we check that the path is concatenated with the servlet path
     * 
     * @throws ServletException an uncaught exception
     * @throws InvocationTargetException an uncaught exception
     * @throws IllegalAccessException an uncaught exception
     * @throws NoSuchMethodException an uncaught exception
     */
    @Test
    public void testGetPath() throws ServletException, IllegalAccessException, InvocationTargetException,
            NoSuchMethodException {

        // length is: 1234567890123456789012345
        final String sampleRequest = "step-web/rest/bible/get/1K2/2K2/";
        final HttpServletRequest req = mock(HttpServletRequest.class);

        when(req.getRequestURI()).thenReturn(sampleRequest);
        when(req.getServletPath()).thenReturn("letters");
        when(req.getContextPath()).thenReturn("more");

        // then
        final StepRequest sr = new StepRequest(req, "UTF-8");
        final Method declaredMethod = sr.getClass().getDeclaredMethod("getPathLength",
                HttpServletRequest.class);
        declaredMethod.setAccessible(true);

        assertEquals(11, declaredMethod.invoke(sr, req));
    }

    /**
     * helper factory method
     * 
     * @return a step request
     */
    private StepRequest getTestStepRequest() {
        return new StepRequest(TEST_URI, TEST_CONTROLLER_NAME, TEST_METHOD_NAME, TEST_ARGS);
    }
}
