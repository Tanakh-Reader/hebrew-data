package com.tyndalehouse.step.core.models;

import com.tyndalehouse.step.core.models.search.PopularSuggestion;
import org.codehaus.jackson.annotate.JsonIgnore;
import org.crosswire.jsword.versification.BibleBook;

import java.io.Serializable;

/**
 * Gives info on a book name (short and long names)
 *
 * @author chrisburrell
 */
public class BookName implements Serializable, PopularSuggestion {
    private static final long serialVersionUID = 2406197083965523605L;
    private final Section sectionType;
    private String shortName;
    private String fullName;

    @JsonIgnore
    private BibleBook bibleBook;
    /* indicates a whole book, OR a book that should be treated like a chapter */
    private boolean wholeBook;
    private boolean isPassage;
    private String osisID;

    /**
     * wraps around a book name, giving the abbreviation and the full name
     *
     * @param shortName   the short name
     * @param fullName    the full name
     * @param isWholeBook true to indicate the option refers to a whole book
     * @param osisID
     */
    public BookName(final String shortName, final String fullName,
                    final Section sectionType,
                    final boolean isWholeBook,
                    final String osisID
    ) {
        this(shortName, fullName, sectionType, isWholeBook, null, osisID);
    }


    /**
     * wraps around a book name, giving the abbreviation and the full name
     *
     * @param shortName   the short name
     * @param fullName    the full name
     * @param isWholeBook true to indicate the option refers to a whole book
     * @param bibleBook   the bible book that originates this model
     * @param isPassage   true to indicate we're looking at a passage/chapter
     * @param osisID      the OSIS ID that names this version.
     */
    public BookName(final String shortName,
                    final String fullName,
                    final Section sectionType,
                    final boolean isWholeBook, final BibleBook bibleBook,
                    boolean isPassage,
                    final String osisID) {
        this.shortName = shortName;
        this.fullName = fullName;
        this.sectionType = sectionType;
        this.wholeBook = isWholeBook;
        this.bibleBook = bibleBook;
        this.isPassage = isPassage;
        this.osisID = osisID;
    }

    /**
     * wraps around a book name, giving the abbreviation and the full name
     *
     * @param shortName   the short name
     * @param fullName    the full name
     * @param isWholeBook true to indicate the option refers to a whole book
     * @param bibleBook   the bible book that originates this model
     * @param osisID      the OSIS ID that names this version.
     */
    public BookName(final String shortName, final String fullName,
                    final Section sectionType,
                    final boolean isWholeBook, final BibleBook bibleBook,
                    final String osisID) {
        this(shortName, fullName, sectionType, isWholeBook, bibleBook, false, osisID);
    }

    /**
     * @return the shortName
     */
    public String getShortName() {
        return this.shortName;
    }

    /**
     * @param shortName the shortName to set
     */
    public void setShortName(final String shortName) {
        this.shortName = shortName;
    }

    /**
     * @return the fulllName
     */
    public String getFullName() {
        return this.fullName;
    }

    /**
     * @param fulllName the fulllName to set
     */
    public void setFullName(final String fulllName) {
        this.fullName = fulllName;
    }

    /**
     * @return the isWholeBook
     */
    public boolean isWholeBook() {
        return this.wholeBook;
    }

    /**
     * @param isWholeBook the isWholeBook to set
     */
    public void setWholeBook(final boolean isWholeBook) {
        this.wholeBook = isWholeBook;
    }

    @JsonIgnore
    public BibleBook getBibleBook() {
        return bibleBook;
    }

    public void setBibleBook(final BibleBook bibleBook) {
        this.bibleBook = bibleBook;
    }

    public boolean isPassage() {
        return isPassage;
    }

    public void setPassage(final boolean isPassage) {
        this.isPassage = isPassage;
    }

    public Section getSectionType() {
        return sectionType;
    }

    public String getOsisID() {
        return osisID;
    }

    public void setOsisID(final String osisID) {
        this.osisID = osisID;
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        final BookName bookName = (BookName) o;

        if (fullName != null ? !fullName.equals(bookName.fullName) : bookName.fullName != null) return false;

        return true;
    }

    @Override
    public int hashCode() {
        return fullName != null ? fullName.hashCode() : 0;
    }

    public enum Section {
        BIBLE_BOOK,
        APOCRYPHA,
        PASSAGE,
        OTHER_NON_BIBLICAL,
        BIBLE_SECTION
    }

}
