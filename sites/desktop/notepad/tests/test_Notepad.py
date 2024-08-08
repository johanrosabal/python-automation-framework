import pytest

from sites.desktop.notepad.pages.NotepadPage import NotepadPage


class TestNotepad:

    def test_add_some_test(self):
        (
            NotepadPage.get_instance()
            .menu_edit()
            .edit_document("Test1")
            .edit_document("\nTest2")
            .edit_document("\nTest3")
            .close()
        )
