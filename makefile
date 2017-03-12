PYTHON  = /usr/bin/python3
LATEX	= /usr/bin/xelatex
CONVERT = /usr/bin/convert
PANDOC  = /usr/bin/pandoc
MD5SUM  = /usr/bin/md5sum
WEBDIR  = bible

# Didn't want to delete these definitions as they
# might come in handy later

OLD     = genesis exodus leviticus numbers deuteronomy \
	joshua judges ruth 1samuel 2samuel 1kings 2kings \
	1chronicles 2chronicles ezra nehemiah esther job \
	psalms proverbs ecclesiastes songofsolomon isaiah \
	jeremiah lamentations ezekiel daniel hosea joel \
	amos obadiah jonah micah nahum habakkuk zephaniah \
	haggai zechariah malachi

NEW     = matthew mark luke john acts romans \
	1corinthians 2corinthians galatians ephesians \
	philippians colossians 1thessalonians 2thessalonians \
	1timothy 2timothy titus philemon hebrews james \
	1peter 2peter 1john 2john 3john jude revelation 

IMAGES  = ATypicalFridayNightOnCanalStreet \
	FlyLeaf GethsemeneWasANotoriousCruisingGround \
	GoodSamaritan LookItsTheLawScarper \
	MosesWithTablets SermonOnTheMount


Dictionaries := words.dict phrases.dict

bible :	md5sums bible.epub bible.pdf

%.png : %.xcf
	$(CONVERT) -flatten $< $@

%.epub : %.tex
	$(PANDOC) --toc-depth=2 -o $@ $<

bible.pkl : $(Dictionaries) PerformTranslation.py
	$(PYTHON) PerformTranslation.py

introduction.tex : introduction.txt CreateIntroductionTex.py
	$(PYTHON) CreateIntroductionTex.py $(Dictionaries)

bible.epub : bible.tex

rawhtml : bible.pkl
	$(PYTHON) PickleToRawHTML.py bible.pkl
	cp introduction.txt introduction.html

bible.pdf : bible.pkl dictionaries.pkl introduction.tex PickleToLaTeX.py $(IMAGES:=.png)
	rm -vf *.{aux,toc,pdf,tex}
	$(PYTHON) PickleToLaTeX.py bible.pkl
	$(LATEX) bible.tex
	$(LATEX) bible.tex

md5sums : bible.pdf bible.epub
	$(MD5SUM) bible.pdf bible.epub > md5sums

web: bible.pdf rawhtml
	mkdir -p $(WEBDIR)
	cp -v bible.pdf *.html *.css $(WEBDIR)

# The .SECONDARY directive stops the intermediate files being 
# cleaned up post-build. Commented out for the time being
# in an attempt to keep things clean.
#
# TGJ 12 June 2014
#.SECONDARY: %.pkl %.rhtml

.PHONY: clean
clean:
	rm -vrf *.log *.tmp *.tex *.png *.toc *.aux *.pyc *.ppk *.pkl *.html *.rhtml *.pdf $(WEBDIR) *~ 2> /dev/null
