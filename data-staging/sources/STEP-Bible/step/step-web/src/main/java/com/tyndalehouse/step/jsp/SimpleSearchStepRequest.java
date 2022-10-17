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
package com.tyndalehouse.step.jsp;

import java.util.ResourceBundle;

import javax.servlet.http.HttpServletRequest;

import com.google.inject.Injector;
import com.tyndalehouse.step.core.models.ClientSession;

/**
 * A WebCookieRequest stores information from the request and the cookie for easy use in the jsp page.
 * 
 * @author chrisburrell
 */
// CHECKSTYLE:OFF
public class SimpleSearchStepRequest extends AbstractSearchStepRequest {
    final Object[][] firstLine = new Object[][] {
            { "<input type=\"text\" class=\"simpleTextTypePrimary drop _m\" source=\"step.defaults.search.textual.simpleTextTypes\" ro=\"true\" />" },
            { "<input type=\"text\" class=\"simpleTextCriteria _m\" />" },
            { "<input type=\"text\" class=\"simpleTextScope drop _m\" title=\"%1$s\" source=\"step.defaults.search.textual.availableRanges\" ro=\"false\" />",
                    "simple_text_search_scope_of_search_help" } };

    private final Object[][] secondLine = new Object[][] {
            { "<input type=\"text\" class=\"simpleTextInclude drop _m\" size=\"13\" source=\"step.defaults.search.textual.simpleTextIncludes\" ro=\"true\" />" },
            { "<input type=\"text\" class=\"simpleTextTypeSecondary simpleTextSecondaryTypes drop _m\" source=\"step.defaults.search.textual.simpleTextSecondaryTypes\" ro=\"true\" />" },
            { "<input type=\"text\" class=\"simpleTextSecondaryCriteria _m\" />" },
            { "<input type=\"text\" class=\"simpleTextProximity drop _m\" source=\"step.defaults.search.textual.simpleTextProximities\" ro=\"true\" />" } };

    private final Object[][] values = new Object[][] { { "simple_text_search_level_basic", this.firstLine },
            { "simple_text_search_level_intermediate", this.secondLine } };

    /**
     * Allows the generation of the search criteria HTML.
     * 
     * @param injector the injector for the application
     * @param request the servlet request
     */
    public SimpleSearchStepRequest(final Injector injector, final HttpServletRequest request) {
        super(injector, request);

        final ResourceBundle bundle = ResourceBundle.getBundle("HtmlBundle",
                injector.getInstance(ClientSession.class).getLocale());
        localize(bundle, this.firstLine);
        localize(bundle, this.secondLine);

    }

    @Override
    Object[][] getValues() {
        return this.values;
    }
}
