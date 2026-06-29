from copystatic import copy_static_to_public

def main():
    src_dir = "static"
    dst_dir = "public"
    copy_static_to_public(src_dir, dst_dir)

if __name__=="__main__":
    main()