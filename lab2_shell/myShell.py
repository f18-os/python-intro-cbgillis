import os
import sys
import re
import subprocess

while(1):
    sys.stdout.write(os.curdir+'*')
    args = input('').split(' ') # split arguments by spaces
    if 'quit' == args[0]:
        break
    #if '>' in args:
    #if '<' in args:

    pid = os.getpid()
    #begin piped arguments
    if '|'in args:
        dex = args.index('|')
        pipedArgs = args[dex-1 : ]
        print(pipedArgs)

        os.write(1, ("About to fork for pipe (pid=%d)\n" % pid).encode())
        rc = os.fork()
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            os.write(1, ("Piped Child: My pid=%d. Parent pid=%d\n" % (os.getpid(), pid)).encode())
            os.close(1)
            sys.stdout = open("forkedOut.txt", "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd, True) #makes the file descriptor from the child inheritable to the parent
            os.write(2, ("Piped Child: opened fd=%d for writing\n" % fd).encode())
            pipedArgs.remove('|')
            heldArg = pipedArgs[0]
            pipedArgs.remove(pipedArgs[0])
            pipedArgs.append(heldArg)
            if '/' in pipedArgs[0]:
                try:
                    os.execve(pipedArgs[0], pipedArgs, os.environ)
                except:
                    pass
            else:
                for dir in re.split(":", os.environ['PATH']):
                    prgm = "%s/%s" % (dir, pipedArgs[0])
                    try:
                        rtrn = os.execve(prgm, pipedArgs, os.environ)
                        for i in pipedArgs:
                            args.remove(i)
                        args.remove('|')
                        args.add(rtrn)
                    except FileNotFoundError:
                        pass

            os.write(2, ("Piped Child: ERROR: Unable to exec program %s\n" % pipedArgs[0]).encode())
            sys.exit(1)

        else:
            os.write(1, ("Parent: My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())

#resume
    pid = os.getpid()

    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:
        os.write(1, ("Child: My pid==%d. Parent's pid=%d\n" % (os.getpid(), pid)).encode())

        os.close(1)
        sys.stdout = open("output.txt", "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

        if '/' in args[0]:
            try:
                os.execve(args[0], args, os.environ)
            except:
                pass
        else:
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass

        os.write(2, ("Child: ERROR: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)

    else:
        os.write(1, ("Parent: My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())
