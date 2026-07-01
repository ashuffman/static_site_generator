from copystatic import copy_static_to_public
from generate_site import generate_site
import sys



def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    src_dir = "./static"
    dst_dir = "./docs"
    copy_static_to_public(src_dir, dst_dir)
    from_path = "./content"
    template_path = "./template.html"
    dest_path = "./docs"
    generate_site(basepath, from_path, template_path, dest_path)

if __name__=="__main__":
    main()