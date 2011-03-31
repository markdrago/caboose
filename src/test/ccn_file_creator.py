from uuid import uuid4
from os import path

class_start = "public class testClass {\n\n"
class_end = "}\n"
func_start = "  public void testFunc%d() {\n    int x = 1;\n\n"
func_end = "  }\n"
if_line = "    if (x == %d) { System.out.println(\"x is %d\"); }\n\n"

class CcnFileCreator(object):
    def _get_filename(self, directory, filename, suffix):
        if filename is None:
            filename = "%s%s" % (str(uuid4()), suffix)
        return path.join(directory, filename)
        
    def _get_class_with_funcs_with_ccns(self, ccns):
        output = class_start

        func_count = 0
        for ccn in ccns:
            output += func_start % (func_count)
            for i in range(ccn - 1):
                output += if_line % (i, i)
            output += func_end
        output += class_end
        return output

    def create_file_with_ccn(self, ccn, directory, filename=None, suffix=".java"):
        self.create_file_with_funcs_with_ccns(directory, [ccn], filename, suffix)

    def create_file_with_funcs_with_ccns(self, directory, ccns, filename=None, suffix="*.java"):
        fullpath = self._get_filename(directory, filename, suffix)
        
        with open(fullpath, "w") as f:
            f.write(self._get_class_with_funcs_with_ccns(ccns))

