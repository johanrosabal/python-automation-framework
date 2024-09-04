from core.utils.decorator import test
from applications.desktop.notepad.pages.NotepadPage import NotepadPage


class TestNotepad:

    @test(test_case_id="API-0001", test_description="Test Notepad Windows Application.")
    def test_add_some_test(self):
        (
            NotepadPage.get_instance()
            .menu_edit()
            .edit_document("Test1")
            .edit_document("\nTest2")
            .edit_document("\nTest3")
            .close()
        )
