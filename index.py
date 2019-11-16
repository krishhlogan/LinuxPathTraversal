from cmd import Cmd

class Node:
    def __init__(self,data):
        """
        This constructor is to initialise the node object with data for the node and an empty dictionary denoting the
        children of the current node

        :param data: This accepts a string which will be the name of the directory
        """
        self.data=data
        self.children={}

    def insert(self,root=None,path=None,folder=None):
        """
        This method is to create a directory in the file system logically by inserting a node in the appropriate
        position in the Tree.

        :param root: The root of the tree which of type Node :param path: The path where
        insertion is to be made
        :param folder:The name of the directory or folder to be created
        :return: returns a
        boolean value True if creation is successful else False
        """
        keys=path.split("/")
        keys=list(filter(lambda x: x != "", keys))
        node=root
        for key in keys:
            try:
                node=node.children[key]
                self.print_children(node)
                if node.data!=key:
                    return False
            except KeyError as e:
                return False
        obj=Node(data=folder)
        if folder not in node.children.keys():
            node.children[folder]=obj
        else:
            print("ERR: DIRECTORY ALREADY EXISTS")
            return  False
        return True

    def remove(self,root=None,path=None,folder=None):
        """
        This method is used to remove a directory from the given path.

        :param root: The root of the tree which of type Node
        :param path: The path where deletion is to be made
        :param folder:The name of the directory or folder to be created
        :return: returns a boolean value True if creation is successful else False
        """
        keys = path.split("/")
        keys = list(filter(lambda x: x != "", keys))
        node = root
        for key in keys:
            try:
                node = node.children[key]
            except KeyError as e:
                print("Err Invalid Path")
                return False
        try:
            del node.children[folder]
            return True
        except KeyError as e:
            print("Invalid path")
            return False

    def list_dirs(self,path=None,root=None):
        """
        This method is used to list all directories within a given path

        :param path: The path where the directories are to be listed
        :param root: The root of the tree which of type Node
        :return: This method does not return any value. It only prints directories on current path
        """
        keys = path.split("/")
        keys = list(filter(lambda x: x != "", keys))
        node = root
        for key in keys:
            try:
                node = node.children[key]
            except KeyError as e:
                print("This path does not exist",e)
        print("DIRS: "," ".join(self.print_children(node)))

    def print_children(self,node):
        """
        This method is to get all the children of a node

        :param node: The node of the tree which of type Node
        :return: returns the children directory name of current node as a list
        """
        return [node.children[n].data for n in node.children]

    def check_valid(self,path=None,root=None):
        """
        This method is used to check the validity of a path within the file system and return suitable boolean values

        :param path: The path to be checked for validity or existence
        :param root: The root of the tree which of type Node
        :return: Returns a boolean value denoting the validity of the path provided
        """
        keys = path.split("/")
        keys = list(filter(lambda x: x != "", keys))
        node = root
        for key in keys:
            try:
                if key not in node.children.keys():
                    return False
                node=node.children[key]
            except KeyError as e:
                print("ERR: INVALID PATH")
                return False
        return True


class MyPrompt(Cmd):
    prompt = "$ "
    intro = "Application Started ..."

    def __init__(self):
        """
        Constructor of MyPrompt that initialises the method attributed pwd (denoting present working directory) and
        fat ( denoting the file allocation table ) which keeps track of all the directories.
        """
        self.pwd="/"
        self.fat=self.get_FAT(data=self.pwd)
        super(MyPrompt, self).__init__()

    def get_FAT(self,data):
        """
        This method is to create an object for the class Node.

        :param data: It accepts a string which it to be made as value for data attribute for the object of class Node
        :return: This returns the node object that is newly created
        """
        return Node(data=data)

    def do_exit(self, inp=None):
        """
        This method is used to exit the application

        :param inp: This is optional parameter
        :return: returns True which will exit the application
        """
        print("Bye")
        return True

    def help_exit(self):
        """
        This method is used to display help messages regarding exit command

        :return: This method does not return anything
        """
        print('exit the application. Shorthand: Ctrl-D.')

    def do_cd(self,inp):
        """
        This method is used to change the current directory to any valid place within the file system.

        :param inp: This parameter denotes the destination directory to change to . ".." is used to move to the
        previous directory. This accepts both relative and absolute path.
        :return: This function does not return anything
        """
        path=""
        if inp=="..":
            path = self.pwd.split("/")
            path=list(filter(lambda  x: x!="",path))
            path.pop(-1)
            try:
                if path[0]!="/":
                    path.insert(0,"/")
            except IndexError as e:
                pass
            path = "/".join(path)
        else:
            if inp=="/":
                path="/"
            else:
                if inp[0]=="/":
                    if inp[-1]!="/":
                        path=inp+"/"
                    else:
                        path=inp
                else:
                    if inp[-1] !="/":
                        path=self.pwd+inp+"/"
                    else:
                        path=self.pwd+inp
        status=self.fat.check_valid(path=path,root=self.fat)
        if status:
            if path =="":
                self.pwd="/"
            else:
                self.pwd=path
            print("SUCC: REACHED")
        else:
            print("ERR: INVALID PATH")

    def do_mkdir(self,inp):
        """
        This method is used to create a new directory inside any valid directory.

        :param inp: This denotes The directory that is to be created. This can be either relative or absolute path
        :return: This does not return anything
        """
        if inp[-1]=="/":
            inp=inp[:-1]
        if inp[0]=="/":
            folder = inp.split("/")[-1]
            path=inp.split("/")
            path.pop(-1)
            path="/".join(path)
        else:
            path=self.pwd
            folder=inp
        status=self.fat.insert(root=self.fat,path=path,folder=folder)
        if status:
            print("SUCC: CREATED")

    def do_rm(self,inp):
        """
        This method is to remove any directory in the logical file system created, provided the directory exists.

        :param inp: This denotes the directory that is to be removed. This can be either relative or absolute path
        :return: This does not return anything
        """
        path = ""
        folder = ""
        if inp[0] == "/":
            folder = inp.split("/")[-1]
            path = inp.split("/")
            path.pop(-1)
            path = "/".join(path)
        else:
            path = self.pwd
            folder = inp
        status = self.fat.remove(root=self.fat, path=path, folder=folder)
        if status:
            print("SUCC: DELETED")
        else:
            print("ERR: INVALID PATH")

    def do_pwd(self,inp=None):
        """
        This method is to get the present working directory

        :param inp: This is an optional parameter
        :return: This does not return anything
        """
        print("PATH: ",self.pwd)

    def do_ls(self,inp=None):
        """
        This method is used to list all directories in current working directory

        :param inp: This is an optional parameter
        :return: This does not return anything
        """
        self.fat.list_dirs(path=self.pwd+inp,root=self.fat)

    def do_session(self,inp):
        """
        This method is used to clear the session values like reseting the Tree maintaining the logical directory
        structure and changing present working directory to root (/)

        :param inp: This parameter takes only the value  "clear" as input.
        :return: This does not return anything
        """
        if inp!="clear":
            print(inp+" is not a valid option")
        self.pwd="/"
        self.fat=self.get_FAT(data="/")
        print("SUCC: CLEARED: RESET TO ROOT")

    def default(self, inp):
        """
        This method is used to handle all cases other than ls,pwd,cd,rm,mkdir

        :param inp: this input can be any string.
        :return: this does not return anything
        """
        print("ERR: CANNOT RECOGNIZE INPUT.")

    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    prompt=MyPrompt()
    prompt.cmdloop()