#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path


class StaticSiteBuilder:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.data_dir = self.root_dir / "data"
        self.pages_dir = self.root_dir / "pages"
        self.templates_dir = self.root_dir / "templates"
        self.build_dir = self.root_dir / "build"
    
    def clean_build_dir(self):
        if self.build_dir.exists():
            # Remove contents instead of the entire directory to avoid breaking the server
            for item in self.build_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            print(f"Cleaned build directory: {self.build_dir}")
        else:
            self.build_dir.mkdir(exist_ok=True)
            print(f"Created build directory: {self.build_dir}")
    
    def copy_data_files(self):
        if not self.data_dir.exists():
            print("No data directory found, skipping data files...")
            return
        
        for item in self.data_dir.rglob("*"):
            if item.is_file():
                # Calculate relative path from data dir
                rel_path = item.relative_to(self.data_dir)
                dest_path = self.build_dir / rel_path
                
                # Create parent directories if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(item, dest_path)
                print(f"Copied data file: {rel_path}")
    
    def extract_template_tag(self, content):
        # Look for TEMPLATE tag at the start of the file
        match = re.match(r'^\s*<!--\s*TEMPLATE:\s*(\w+)\s*-->\s*\n?', content)
        if match:
            template_name = match.group(1)
            # Remove the template tag from content
            content_without_tag = re.sub(r'^\s*<!--\s*TEMPLATE:\s*\w+\s*-->\s*\n?', '', content)
            return template_name, content_without_tag
        return None, content
    
    def load_template(self, template_name):
        template_path = self.templates_dir / f"{template_name}.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def process_page(self, page_path):
        page_name = page_path.stem
        
        # Read page content
        with open(page_path, 'r', encoding='utf-8') as f:
            page_content = f.read()
        
        # Extract template name and clean content
        template_name, clean_content = self.extract_template_tag(page_content)
        
        if not template_name:
            print(f"No TEMPLATE tag found in {page_path.name}, skipping...")
            return
        
        try:
            template_content = self.load_template(template_name)
            
            pretty_page_name = page_name.replace('-', ' ').capitalize()
            if pretty_page_name == 'Index': pretty_page_name = "Home"
            final_content = template_content.replace('<!-- TITLE -->', pretty_page_name)

            final_content = final_content.replace('<!-- CONTENT -->', clean_content)
            
            if page_name.lower() == 'index':
                # Index page goes to build root
                output_path = self.build_dir / "index.html"
            else:
                # Other pages go to their own folder
                page_folder = self.build_dir / page_name
                page_folder.mkdir(exist_ok=True)
                output_path = page_folder / "index.html"
            
            # Write final file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"Built page: {page_name} -> {output_path.relative_to(self.build_dir)}")
            
        except FileNotFoundError as e:
            print(f"Error processing {page_path.name}: {e}")
    
    def build_pages(self):
        if not self.pages_dir.exists():
            print("No pages directory found, skipping pages...")
            return
        
        html_files = list(self.pages_dir.glob("*.html"))
        if not html_files:
            print("No HTML files found in pages directory...")
            return
        
        for page_path in html_files:
            self.process_page(page_path)
    
    def build(self):
        print("Starting static site build...")
        
      # Check if required directories exist
        if not self.templates_dir.exists():
            print("Templates directory not found! Please create the 'templates' folder.")
            return False
        
        try:
            # Clean and create build directory
            self.clean_build_dir()
            
            # Copy data files
            self.copy_data_files()
            
            # Build pages
            self.build_pages()
            
            print("Build completed successfully!")
            return True
            
        except Exception as e:
            print(f"Build failed: {e}")
            return False

if __name__ == "__main__":
    builder = StaticSiteBuilder()
    success = builder.build()
    exit(0 if success else 1)