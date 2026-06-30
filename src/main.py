from copystatic import copy_static_to_public
from generate_site import generate_site

def main():
    src_dir = "static"
    dst_dir = "public"
    copy_static_to_public(src_dir, dst_dir)
    from_path = "content"
    template_path = "template.html"
    dest_path = "public"
    generate_site(from_path, template_path, dest_path)

if __name__=="__main__":
    main()