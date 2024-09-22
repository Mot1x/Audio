import unittest
import additional_functions


class Test(unittest.TestCase):
    def test_correct_command_and_args(self):
        command, req_args = additional_functions.get_command_and_args("cut 1 20")
        self.assertEqual(command, "cut", "error get command")
        self.assertEqual(req_args, ["1", "20"], "error get args")

    def test_correct_command_and_args_with_quotes(self):
        command, req_args = additional_functions.get_command_and_args('overlay "C:\melody.wav"')
        self.assertEqual(command, "overlay", "error get command")
        self.assertEqual(req_args, ["C:\melody.wav"], "error get args")

    def test_correct_command_and_args_with_uncorrect_quotes(self):
        self.assertRaises(Exception, additional_functions.get_command_and_args, 'overlay ""C:\melody.wav"')


if __name__ == "__main__":
    unittest.main()