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
package com.tyndalehouse.step.models;

import java.io.IOException;
import java.io.InputStream;
import java.util.Locale;

import com.tyndalehouse.step.core.exceptions.StepInternalException;
import com.tyndalehouse.step.core.models.ClientSession;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.Part;

/**
 * A web session which wraps around the jsession id...
 * 
 * @author chrisburrell
 * 
 */
public class WebSessionImpl implements ClientSession {
    private String sessionId;
    private String ipAddress;
    private String language;
    private Locale locale;
    private HttpServletRequest request;

    /**
     * creates a web session
     *
     * @param id the id of the session
     * @param language the ISO 3-character long language name
     * @param ipAddress the user's IP address
     * @param locale the user's locale
     * @param request
     */
    public WebSessionImpl(final String id, final String language, final String ipAddress, final Locale locale, final HttpServletRequest request) {
        this.sessionId = id;
        this.language = language;
        this.ipAddress = ipAddress;
        this.locale = locale;
        this.request = request;
    }

    /**
     * @return the session
     */
    @Override
    public String getSessionId() {
        return this.sessionId;
    }

    /**
     * @param sessionId the session to set
     */
    public void setSessionId(final String sessionId) {
        this.sessionId = sessionId;
    }

    /**
     * @return the ipAddress
     */
    @Override
    public String getIpAddress() {
        return this.ipAddress;
    }

    /**
     * @param ipAddress the ipAddress to set
     */
    public void setIpAddress(final String ipAddress) {
        this.ipAddress = ipAddress;
    }

    @Override
    public String getLanguage() {
        return this.language;
    }

    /**
     * @param language the language to set
     */
    public void setLanguage(final String language) {
        this.language = language;
    }

    @Override
    public Locale getLocale() {
        return this.locale;
    }

    @Override
    public String getParam(String name) {
        return this.request.getParameter(name);
    }

    @Override
    public InputStream getAttachment(final String filePart) {
        try {
            final Part part = this.request.getPart(filePart);
            return part.getInputStream();
        } catch (ServletException e) {
            throw new StepInternalException("Unable to obtain part", e);
        } catch (IOException e) {
            throw new StepInternalException("Unable to obtain part", e);
        }
    }

    /**
     * @param locale the locale to set
     */
    public void setLocale(final Locale locale) {
        this.locale = locale;
    }
}
