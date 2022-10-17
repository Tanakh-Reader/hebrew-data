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
package com.tyndalehouse.step.core.utils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Some IO Utils for use in the STEP application.
 * 
 * @author chrisburrell
 */
public final class IOUtils {
    private static final Logger LOG = LoggerFactory.getLogger(IOUtils.class);

    /** preventing instanciation */
    private IOUtils() {
        // hiding implementation
    }

    /**
     * Closes a @see Closeable properly.
     * 
     * @param c the closeable object
     */
    public static void closeQuietly(final java.io.Closeable c) {
        try {
            if (c != null) {
                c.close();
            }
        } catch (final IOException e) {
            // if exception thrown, do nothing
            LOG.warn("Failed to close reader or stream", e);
        }
    }

    /**
     * Read a classpath resource into a String
     * 
     * @param classpathResource the classpath resource
     * @return the string
     */
    public static String readEntireClasspathResource(final String classpathResource) {
        InputStream s = null;
        InputStreamReader in = null;
        BufferedReader reader = null;

        try {
            s = IOUtils.class.getResourceAsStream(classpathResource);
            if (s == null) {
                return "";
            }

            in = new InputStreamReader(s, "UTF-8");
            reader = new BufferedReader(in);
            final StringBuilder sb = new StringBuilder(64000);

            final char[] chars = new char[8192];
            int l = -1;
            while ((l = reader.read(chars)) != -1) {
                sb.append(chars, 0, l);
            }

            return sb.toString();
        } catch (final IOException e) {
            LOG.warn("Unable to read file for resource: " + classpathResource);
            return "";
        } finally {
            IOUtils.closeQuietly(in);
            IOUtils.closeQuietly(reader);
            IOUtils.closeQuietly(s);
        }
    }
}
