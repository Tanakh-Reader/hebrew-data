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
package com.tyndalehouse.step.guice.providers;

import static com.tyndalehouse.step.core.utils.StringUtils.isNotBlank;

import java.util.Locale;
import java.util.MissingResourceException;

import javax.inject.Provider;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import com.google.inject.Inject;
import com.google.inject.servlet.RequestScoped;
import com.tyndalehouse.step.core.models.ClientSession;
import com.tyndalehouse.step.core.utils.language.ContemporaryLanguageUtils;
import com.tyndalehouse.step.models.WebSessionImpl;

/**
 * This object is request-scoped, meaning it is new for every request. It is a way to return the jsessionId at
 * runtime
 * 
 * @author chrisburrell
 * 
 */
@RequestScoped
public class ClientSessionProvider implements Provider<ClientSession> {
    private static final String COOKIE_REQUEST_PARAM = "lang";
    private final HttpSession session;
    private final HttpServletRequest request;

    /**
     * We inject the HttpSession in so that we can reference the jSessionId in the cookie
     * 
     * @param request the http request
     * @param session the http session containing the jSessionId
     */
    @Inject
    public ClientSessionProvider(final HttpServletRequest request, final HttpSession session) {
        this.request = request;
        this.session = session;
    }

    @Override
    public ClientSession get() {
        final Locale locale = getLocale();
        final String remoteAddr = this.request.getRemoteAddr();
        final String id = this.session.getId();
        try {
            return new WebSessionImpl(id, locale.getISO3Language(), remoteAddr, locale, this.request);
        } catch(MissingResourceException ex) {
            //attemping to set to unsupported Locale... So let's instead set to english
            return new WebSessionImpl(id, Locale.ENGLISH.getISO3Language(), remoteAddr, Locale.ENGLISH, this.request);
        }
    }

    /**
     * Gets the locale.
     * 
     * @return the locale
     */
    private Locale getLocale() {
        if (isNotBlank(this.request.getParameter(COOKIE_REQUEST_PARAM))) {
            return ContemporaryLanguageUtils
                    .getLocaleFromTag(this.request.getParameter(COOKIE_REQUEST_PARAM));
        }

        // take from session next
        if (this.session != null) {
            final Cookie[] cookies = this.request.getCookies();
            if (cookies != null) {
                for (final Cookie c : cookies) {
                    if (COOKIE_REQUEST_PARAM.equals(c.getName())) {
                        return ContemporaryLanguageUtils.getLocaleFromTag(c.getValue());
                    }
                }
            }
        }

        return this.request.getLocale();
    }
}
