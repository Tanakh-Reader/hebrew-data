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
package com.tyndalehouse.step.guice;

import com.tyndalehouse.step.core.utils.StringUtils;

import static com.tyndalehouse.step.core.utils.StringUtils.isBlank;

import java.io.IOException;

import javax.inject.Singleton;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

/**
 * Intercepts and works out whether JSword has been installed with modules...
 * 
 * @author chrisburrell
 * 
 */
@Singleton
public class HashBangFragmentFilter implements Filter {
    @Override
    public void init(final FilterConfig filterConfig) throws ServletException {
        // nothing to record
    }

    @Override
    public void doFilter(final ServletRequest request, final ServletResponse response, final FilterChain chain)
            throws IOException, ServletException {

        final String parameter = request.getParameter("_escaped_fragment_");
        if (isBlank(parameter)) {
            continueAsNormal(request, response, chain);
            return;
        }

        final String[] split = parameter.split("=");
        if (split.length < 1) {
            continueAsNormal(request, response, chain);
            return;
        }

        if ("lexicon".equals(split[0])) {
            request.getRequestDispatcher("snapshots/definition.jsp?strong=" + split[2]).forward(request,
                    response);
        } else if(parameter.indexOf("__/") != -1) {
            //then we're looking at a passage...
            String[] parts = parameter.split("__/");

            StringBuilder sb = new StringBuilder(128);

            int passageId = 0;
            sb.append("snapshots/passage.jsp?");
            for(int ii = 0; ii < parts.length; ii++) {
                String[] passageParts = parts[ii].split("/");
                if(StringUtils.isBlank(parts[ii]) || passageParts.length < 4) {
                    continue;
                }

                boolean wasPassage = appendPassageArgs( sb, passageId, passageParts);
                if(!wasPassage) {
                    appendSearchArgs(sb, passageId, passageParts);
                }

                if(ii < parts.length - 1) {
                    sb.append('&');
                }
                passageId++;
            }
            request.getRequestDispatcher(sb.toString()).forward(request, response);
        }

        continueAsNormal(request, response, chain);
    }

    /**
     *  Everything else is a search at the moment
     * @param sb the string builder
     * @param passageId the passage id
     * @param passageParts the passage parts
     */
    private void appendSearchArgs(final StringBuilder sb, final int passageId, final String[] passageParts) {
        if(passageParts.length < 5) {
            return;
        }

        sb.append("querySyntax");
        sb.append(passageId);
        sb.append('=');
        sb.append(passageParts[4]);

        sb.append('&');
        sb.append("context");
        sb.append(passageId);
        sb.append('=');
        sb.append(passageParts[5]);

        sb.append('&');
        sb.append("pageNumber");
        sb.append(passageId);
        sb.append('=');
        sb.append(passageParts[2]);

        sb.append('&');
        sb.append("pageSize");
        sb.append(passageId);
        sb.append('=');
        sb.append(passageParts[3]);
    }

    /**
     * Appends the argument to lookup a passage snapshot
     * @param sb the StringBuilder
     * @param passageId the passage Id
     * @param passageParts the passage parts
     */
    private boolean appendPassageArgs(final StringBuilder sb, final int passageId, final String[] passageParts) {
        if( !"passage".equals(passageParts[1])) {
            return false;
        }

        sb.append("version");
        sb.append(passageId);
        sb.append('=');
        sb.append(passageParts[3]);
        sb.append('&');
        sb.append("reference");
        sb.append(passageId);
        sb.append('=');
        sb.append(passageParts[4]);
        return true;
    }

    /**
     * Continute as normal.
     * 
     * @param request the request
     * @param response the response
     * @param chain the chain
     * @throws IOException Signals that an I/O exception has occurred.
     * @throws ServletException the servlet exception
     */
    private void continueAsNormal(final ServletRequest request, final ServletResponse response,
            final FilterChain chain) throws IOException, ServletException {
        // default, do nothing
        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {
        // nothing to destroy
    }
}
