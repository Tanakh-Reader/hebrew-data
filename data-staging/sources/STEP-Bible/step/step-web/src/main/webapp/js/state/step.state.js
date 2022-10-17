/*******************************************************************************
 * Copyright (c) 2012, Directors of the Tyndale STEP Project All rights
 * reserved.
 * 
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer. Redistributions in binary
 * form must reproduce the above copyright notice, this list of conditions and
 * the following disclaimer in the documentation and/or other materials provided
 * with the distribution. Neither the name of the Tyndale House, Cambridge
 * (www.TyndaleHouse.com) nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 ******************************************************************************/
step.state = {
    responseLanguage : undefined,
    language : function(numParts) {
        if(this.responseLanguage != undefined) {
            return this.responseLanguage;
        }

        //first take from URL var
        var lang = $.getUrlVar("lang");

        if(lang == null) {
            //take from cookie
            lang = $.cookie("lang");
        }

        if(lang == null) {
            lang = window.navigator.userLanguage || window.navigator.language;
        }

        if(numParts == 1) {
            return lang.split("-")[0];
        } 
        return lang;
    },
    
    restore : function() {
        //restore active language
        this._restoreLanguage();
     },


    isLocal : function() {
        if(this.local == undefined) {
            this.local = $("meta[step-local]").attr("content") == "true";
        }
        return this.local;
    },
    getDomain : function() {
        if(this.domain == undefined) {
            this.domain = $("meta[step-domain]").attr("content");
        }
        return this.domain;
    },
    getIncompleteLanguage : function() {
        if(this.incomplete == undefined) {
            var incomplete = $("meta[step-incomplete-language]");
            this.incomplete = incomplete.attr("content") == "true";
        }
        return this.incomplete;
    },
    isLtR: function() {
        if(this.direction == undefined) {
            this.direction = $("meta[step-direction]").attr("content") == "true";
        }
        return this.direction;
    },
    getCurrentVersion : function() {
        if(this.version == undefined) {
            this.version = $("meta[name='step.version']").attr("content");
        }
        return this.version;
    }
};
