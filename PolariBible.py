""" General definitions for the Polari Bible including the classes used throughout.
Copyright (c)  2004-2015 Tim Greening-Jackson """

import re
import itertools

class Verse:
    """ Class which holds a verse of the bible """
    def __init__(self, index, text):
        self.index = index
        self.text = text

    def __repr__(self):
        return '[{n}] {v}\n'.format(n=self.index, v=self.text)
        
class Chapter:
    """ Class which holds a chapter of the Bible - i.e. mostly consists of verses """
    def __init__(self, index):
        self.index    = index
        self.verses   = []

    def __repr__(self):
        return '{n} ({v} verses)'.format(n=self.index, v=len(self.verses))
        
class Book:
    """ Class which holds a book of the Bible - mostly Chapters """
    def __init__(self, index, title):
        self.title = title
        assert index > 0 and index < 67
        self.index = index
        self.testament = 'Old' if index < 40 else 'New'
        self.chapters = []
        self.stem = title.replace(' ','').lower()
        self.psalms = False if self.index != 19 else True
        
    def __repr__(self):
        return '"{name}" (#{index}) {testament} testament. {chapters} chapters'.format(name=self.title, index=self.index, testament=self.testament, chapters = len(self.chapters))

    def AddChapter(self, chapter):
        self.chapters.append(chapter)


class Translation:
    """ Class to hold translation details"""
    _ids = itertools.count(0)

    def __init__(self, english, polari, case=True):
        self.english = english # English text e.g. "good"
        self.polari  = polari  # Polari equivalent e.g. "bona"
        self.regexp  = re.compile(r'\b{s}\b'.format(s=english))
        self.index   = next(self._ids)

    def __repr__(self):
        return '#{}: "{}" -> "{}"\n'.format(self.index, self.english, self.polari)
