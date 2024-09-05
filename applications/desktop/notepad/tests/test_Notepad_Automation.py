from applications.desktop.notepad.pages.NotepadAutomation import NotepadAutomation
from core.utils.decorator import test


class TestNotepadAutomation:
    notepad = NotepadAutomation()

    @test(test_case_id="DES-0001", test_description="Test Undo Notepad Application.")
    def test_undo(self):
        self.notepad.write_text("12345")
        self.notepad.edit_menu.undo()

    @test(test_case_id="DES-0002", test_description="Test Cut Notepad Application.")
    def test_cut(self):
        self.notepad.write_text("67890")
        self.notepad.edit_menu.select_all()
        self.notepad.edit_menu.cut()
        self.notepad.verify_text("", "Text area should be empty")

    @test(test_case_id="DES-0003", test_description="Test Paste Notepad Application.")
    def test_paste(self):
        self.notepad.edit_menu.paste()
        self.notepad.verify_text("67890", "Text area should be '67890'")

    @test(test_case_id="DES-0004", test_description="Test Delete Notepad Application.")
    def test_delete(self):
        self.notepad.edit_menu.select_all()
        self.notepad.edit_menu.delete()
        self.notepad.verify_text("", "Text area should be empty")

    @test(test_case_id="DES-0005", test_description="Test Find Text Notepad Application.")
    def test_find_text(self):
        self.notepad.write_new_line_text("This is test automation script!")
        self.notepad.write_new_line_text("Running test with Appium Integration...")
        self.notepad.write_new_line_text("Because running automation is great!!")
        self.notepad.write_new_line_text("Automation scripts test reduce time execution.")
        self.notepad.edit_menu.find()
        self.notepad.find_dialog_box.find_what("automation") \
            .click_up() \
            .click_find_next() \
            .click_find_next() \
            .click_cancel()

    @test(test_case_id="DES-0006", test_description="Test Find Next Text Notepad Application.")
    def test_find_next(self):
        self.notepad.edit_menu.find_next()

    @test(test_case_id="DES-0007", test_description="Test Find Previous Text Notepad Application.")
    def test_find_previous(self):
        self.notepad.edit_menu.find_previous()

    @test(test_case_id="DES-0008", test_description="Test Replace Text Notepad Application.")
    def test_replace(self):
        self.notepad.edit_menu.replace()
        self.notepad.edit_menu.go_to()
        self.notepad.go_to_line_dialog_box.enter_line_number(1).click_go_to()
        self.notepad.replace_dialog_box.find_what("Appium").replace_with(
            "Appium Library").click_replace().click_cancel()

    @test(test_case_id="DES-0009", test_description="Test 'Save As...' Text Notepad Application.")
    def test_save_as(self):
        self.notepad.save_as_file("C:\\test\\test.txt")

    @test(test_case_id="DES-0010", test_description="Test About Dialog Box Text Notepad Application.")
    def test_help_menu_about_notepad(self):
        self.notepad.help_menu.about_notepad()
        self.notepad.about_dialog_box.click_ok()

    @test(test_case_id="DES-0011", test_description="Test Exit '(Close)' Text Notepad Application.")
    def test_close_application(self):
        self.notepad.file_menu.exit()
