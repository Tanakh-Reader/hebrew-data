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

import static com.tyndalehouse.step.core.utils.StringUtils.isBlank;

import javax.inject.Inject;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.tyndalehouse.step.core.data.EntityDoc;
import com.tyndalehouse.step.core.data.EntityIndexReader;
import com.tyndalehouse.step.core.data.EntityManager;

/**
 * A utility to provide colors to an xsl spreadsheet. This is a non-static utility since later on we may wish
 * to provide configuration to vary the colours, etc.
 * 
 * We use American spelling for Color because we then avoid various spellings across the code base.
 * 
 * The rules for colour coding are:
 * <p>
 * Green for anything that finishes -1S -2S -3S SM SN or SF (indicates Singular)
 * <p>
 * Red for anything that finishes -1P -2P -3P PM PN or PF (indicates Plural)
 * <p>
 * <p>
 * Depending on other characteristics we vary the shade of the colour
 * <p>
 * <p>
 * Darkest for verbs and Nominative (ie the person who is doing it),
 * <p>
 * ie anything ending -1S -2S -3S NSM NSN NSF NPM NPN or NPF
 * <p>
 * Lighter for Vocative and Objective (ie a person being addressed, or the person/thing which is being acted
 * on)
 * <p>
 * ie anything ending VSM VSN VSF VPM VPN VPF OSM OSN OSF OPM OPN or OPF
 * <p>
 * Pale for Genative or Dative (ie the person/thing owning another thing or doing to/by/from a thing)
 * <p>
 * ie anything ending GSM GSN GSF GPM GPN or GPF or DSM DSN DSF DPM DPN or DPF
 * 
 * 
 * @author chrisburrell
 */
public class ColorCoderProviderImpl {
    private static final Logger LOGGER = LoggerFactory.getLogger(ColorCoderProviderImpl.class);
    private static final String ROBINSON_PREFIX_LC = "robinson:";
    private static final String ROBINSON_PREFIX_UC = "ROBINSON:";
    private static final int MINIMUM_MORPH_LENGTH = ROBINSON_PREFIX_UC.length() + 2;

    // css classes
    private final EntityIndexReader morphology;

    /**
     * @param manager the manager from which to obtain an index reader for morphology information
     */
    @Inject
    public ColorCoderProviderImpl(final EntityManager manager) {
        this.morphology = manager.getReader("morphology");
    }

    /**
     * @param morph the robinson morphology
     * @return the classname
     */
    public String getColorClass(final String morph) {
        if (morph == null || morph.length() < MINIMUM_MORPH_LENGTH) {
            return "";
        }

        String classes = null;
        if (morph.startsWith(ROBINSON_PREFIX_LC) || morph.startsWith(ROBINSON_PREFIX_UC)) {
            // we're in business and we know we have at least 3 characters
            LOGGER.debug("Identifying grammar for [{}]", morph);

            final int length = ROBINSON_PREFIX_LC.length();
            final int firstSpace = morph.indexOf(' ', length);
            String code;
            if (firstSpace != -1) {
                code = morph.substring(length, firstSpace);
            } else {
                code = morph.substring(length);
            }

            final EntityDoc[] results = this.morphology.searchExactTermBySingleField("code", 1, code);
            if (results.length > 0) {
                classes = results[0].get("cssClasses");
                // Added on Feb 27, 2018 to annotate verbs
				String funct;
				try {
					funct = results[0].get("function").toLowerCase();
				}
				catch (NullPointerException e) {
					funct = "";
				}
                if (funct.equals("verb")) {					
                	String tense, voice, mood;
					try {
						tense = results[0].get("tense").toLowerCase();
						voice = results[0].get("voice").toLowerCase();
						mood = results[0].get("mood").toLowerCase();
					}
					catch (NullPointerException e) {
						tense = voice = mood = "";
					}
					if (!tense.isEmpty() && !mood.isEmpty()) {
						// Annotate 2nd Aorist as Aorist, 2nd Future as Future, 2nd Perfect as Perfect, 2nd Pluperfect ...
						if (tense.startsWith("2nd ")) {
							tense = tense.substring(4);
						} else if (tense.equals("indefinite tense")) {
							tense = "indefinite";
						}
						if ( (voice.equals("passive")) || (voice.equals("either middle or passive")) ) {
							voice = "p";
						}
						else if (voice.equals("middle") ) {
							voice = "m";
						}
						else if ((voice.indexOf("active") > -1) || (voice.indexOf("deponent") > -1) || (voice.indexOf("indefinite") > -1) ) {
							voice = "a";
						}
						else {
							LOGGER.warn("cannot identify voice [{}]", voice);
							voice = "a";
						}
						classes = classes + " v" + getShortCodeTense(tense) + voice + getShortCodeMood(mood);
					}
                }
            }
            /* Added this section for the Chinese Bible which has the morphology on verbs */
            else if (code.length() > 4) {
            	if (code.substring(0,1).equalsIgnoreCase("v")) {
            		String tense = code.substring(2,3).toLowerCase();
					String voice = code.substring(3,4).toLowerCase();
            		String mood = code.substring(4,5).toLowerCase();
            		if (tense.equals("2")) {
                		tense = code.substring(3,4).toLowerCase();
						voice = code.substring(4,5).toLowerCase();
                		mood = code.substring(5,6).toLowerCase();
            		}
					if (voice.equals("e")) {
						voice = "p";
					}
					else if ( (!(voice.equals("p"))) && (!(voice.equals("m"))) ) {
						String voice_displayed_as_active = "adnoqx"; // active, middle deponent, middle or passive deponent, passive deponent, impersonal active, indefinite
						if (voice_displayed_as_active.indexOf(voice) == -1)  {
							LOGGER.warn("cannot identify morphology for [{}]", code);
						}
						voice = "a";
					}
					classes = "v" + tense + voice + mood;

            		if (classes == null) {
                        LOGGER.warn("cannot identify morphology for [{}]", code);
            		}
            	}
            	else {
					LOGGER.warn("other than verb [{}]", code);
				}
            }

            if (isBlank(classes) && firstSpace != -1) {
                // redo the same process, but with less of the string,
                return getColorClass(morph.substring(firstSpace + 1));
            }
        }
        return classes != null ? classes : "";
    }

	public String getShortCodeTense(final String tense) {
		if (tense.equals("aorist")) return "a";
		else if (tense.equals("present")) return "p";
		else if (tense.equals("perfect")) return "r";
		else if (tense.equals("pluperfect")) return "l";
		else if (tense.equals("future")) return "f";
		else if (tense.equals("imperfect")) return "i";
		else if (tense.equals("indefinite")) return "x";
		else {
			LOGGER.warn("cannot identify tense for [{}]", tense);
			return "";
		}
	}

	public String getShortCodeMood(final String mood) {
		if (mood.equals("indicative")) return "i";
		else if (mood.equals("imperative")) return "m";
		else if (mood.equals("participle")) return "p";
		else if (mood.equals("infinitive")) return "n";
		else if (mood.equals("subjunctive")) return "s";
		else if (mood.equals("optative")) return "o";
		else {
			LOGGER.warn("cannot identify mood for [{}]", mood);
			return "";
		}
	}

}
