from uuid import uuid4
from os import path

class CcnFileCreator(object):
    def create_file_with_ccn(self, ccn, directory, filename=None, suffix=".java"):
        if filename is None:
            filename = "%s%s" % (str(uuid4()), suffix)
        fullpath = path.join(directory, filename)

        with open(fullpath, "w") as f:
            f.write("public class testClass {\n\n")
            f.write("  public void testFunc() {\n")
            f.write("    int x = 1;\n\n")
            for i in range(ccn - 1):
                line = "    if (x == %d) { System.out.println(\"x is %d\"); }\n\n"
                f.write(line % (i, i))
            f.write("  }\n")
            f.write("}\n")

