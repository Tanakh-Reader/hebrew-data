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
package com.tyndalehouse.step.core.service.jsword;

import java.util.List;

import com.tyndalehouse.step.core.models.BibleInstaller;
import org.crosswire.jsword.book.Book;
import org.crosswire.jsword.book.BookCategory;
import org.crosswire.jsword.book.install.Installer;

/**
 * The service providing access to JSword. All JSword calls should preferably be placed in this service
 *
 * @author chrisburrell
 */
public interface JSwordModuleService {
    /**
     * looks up any installed module
     *
     * @param bibleCategory the categories of the modules to be returned
     * @return a list of bible books
     */
    List<Book> getInstalledModules(BookCategory... bibleCategory);

    /**
     * looks up any installed module
     *
     * @param bibleCategory the categories of the modules to be returned
     * @param allVersions   indicates all versions of the bible
     * @param locale        specifies a particular language of interest + defaults
     * @return a list of bible books
     */
    List<Book> getInstalledModules(boolean allVersions, String locale, BookCategory... bibleCategory);

    /**
     * Using module initials, checks whether the module has been installed
     *
     * @param moduleInitials the initials of the modules to check for installation state
     * @return true if the module is installed
     */
    boolean isInstalled(String... moduleInitials);

    /**
     * Kicks of a process to install this version
     *
     * @param installerIndex the index of the installer to use
     * @param version        version to be installs
     */
    void installBook(int installerIndex, String version);

    /**
     * Kicks of a process to install this version
     *
     * @param version version to be installs
     */
    void installBook(String version);

    /**
     * assesses the progress made on an installation
     *
     * @param bookName the book name
     * @return the percentage of completion (0 - 1.0)
     */
    double getProgressOnInstallation(String bookName);

    /**
     * assesses the progress made on an indexing operation
     *
     * @param bookName the book name
     * @return the percentage of completion (0 - 1.0)
     */
    double getProgressOnIndexing(String bookName);

    /**
     * retrieves all modules that have been installed
     *
     * @param bookCategory   the list of categories to be included
     * @param installerIndex the index of the installer to use
     * @return all modules whether installed or not
     */
    List<Book> getAllModules(int installerIndex, BookCategory... bookCategory);

    /**
     * reloads all installers TODO - user should be warned <b>USERS SHOULD BE WARNED ABOUT THIS AS IT LOOKS UP
     * INFORMATION ON THE INTERNET</b>
     */
    void reloadInstallers();

    /**
     * indexes a book
     *
     * @param initials the initials of the book to index
     */
    void index(String initials);

    /**
     * re-indexes a book
     *
     * @param initials the initials of the book to index
     */
    void reIndex(String initials);

    /**
     * Checks whether a module is indexed
     *
     * @param versions version to be indexed
     * @return true if the module has been indexed
     */
    boolean isIndexed(String versions);

    /**
     * This method is deliberately placed at the top of the file to raise awareness that sensitive countries
     * may not wish to access the internet.
     * <p/>
     * If the installation is set to "offline", then only return the offline installers.
     *
     * @return a set of installers
     */
    List<Installer> getInstallers();

    /**
     * @param offline true to set the installation to be off-line only.
     */
    void setOffline(boolean offline);

    /**
     * Removes a module
     *
     * @param initials initials of the module to remove, e.g. 'WEB'
     */
    void removeModule(String initials);

    /**
     * Provides a way of waiting for indexes to be created
     *
     * @param versions versions to be waited upon
     */
    void waitForIndexes(String... versions);

    /**
     * Creates and returns a directory installer
     *
     * @param directoryPath installs modules from a directory
     * @return the directory installer index
     */
    BibleInstaller addDirectoryInstaller(String directoryPath);
}
